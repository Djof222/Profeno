# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
import json
from odoo import api, fields, models


class Feed(models.Model):
    _name = 'channel.feed'
    _description = 'Channel Feed'

    connection_id = fields.Many2one('channel.connection','Connection',required=True)
    channel = fields.Selection(related='connection_id.channel')
    remote_id = fields.Char('Store ID',required=True)
    name = fields.Char('Name', readonly=True)
    data = fields.Text('Data',inverse='_set_feed_name')
    type = fields.Selection(
        selection=[
            ('company','Company'),
            ('contact','Contact'),
            ('deal','Deal'),
            ('product','Product'),
            ('user','User'),
        ],
        required=True,
    )
    state = fields.Selection(
        selection=[
            ('draft','Draft'),
            ('done','Done'),
            ('error','Failed'),
        ],
        default='draft',
        required=True,
        readonly=True,
    )
    log_id = fields.Many2one('channel.log','Log',readonly=True)
    log_text = fields.Html('Log Text',default='')

    @api.model
    def create(self,vals):
        res = self.env['channel.feed'].search(
            [
                ('connection_id','=',self._context['default_connection_id']),
                ('remote_id','=',vals['remote_id']),
                ('state','=','draft'),
                ('type','=',vals['type']),
            ]
        )
        if res:
            res.write(vals)
            return res
        else:
            res = super(Feed, self).create(vals)
            return res

    def write(self, vals):
        if 'data' in vals:
            vals['state'] = 'draft'
        return super(Feed, self).write(vals)

    def log(self, text):
        self.log_text = f"{text}<br>{self.log_text}"

    def get_data(self,field=None):
        self.ensure_one()
        data = json.loads(self.data)
        if field:
            return data.get(field, False)
        return data

    def set_data(self, data):
        self.ensure_one()
        self.data = json.dumps(data, indent=4, sort_keys=True)

    def _set_feed_name(self):
        for rec in self:
            rec.name = rec.get_data('name')

    def evaluate_button(self):
        message = ''
        success_ids, error_ids = self.evaluate()
        if success_ids:
            message += f"""
                <div class='alert alert-success' role='alert'>
                    <span class='font-weight-bold'>
                       {self[0].type.capitalize()} Successfully evaluated. {','.join(success_ids)}
                    </span>
                </div>
                <hr>
            """
        if error_ids:
            message += f"""
                <div class='alert alert-danger' role='alert'>
                    <span class='font-weight-bold'>
                        Failed to evaluate. {','.join(error_ids)}
                    </span>
                </div>
                <hr>
            """
        return self.env['wk.wizard.message'].genrated_message(message)

    def evaluate(self):
        success_ids = []
        error_ids = []
        for rec in self:
            try:
                data = rec.get_data()
                if rec.type == 'contact':
                    rec.evaluate_contact(data)
                elif rec.type == 'company':
                    rec.evaluate_company(data)
                elif rec.type == 'deal':
                    rec.evaluate_deal(data)
                elif rec.type == 'product':
                    rec.evaluate_product(data)
                elif rec.type == 'user':
                    rec.evaluate_user(data)
                else:
                    raise NotImplementedError('Not Implemented')
                rec.state = 'done'
                success_ids.append(rec.remote_id)
            except Exception as e:
                rec.state = 'error'
                error_ids.append(rec.remote_id)
                rec.log(
                    f"""
                        <div class='alert alert-danger' role='alert'>
                            <span class='font-weight-bold'>
                                {e}
                            </span>
                        </div>
                    """
                )
            else:
                rec.log(
                    f"""
                        <div class='alert alert-success' role='alert'>
                            <span class='font-weight-bold'>
                                Evaluated.
                            </span>
                        </div>
                    """
                )
        return success_ids, error_ids

    def evaluate_company(self, data):
        data['is_company'] = True
        category = data.pop('category',False)
        if category:
            category_id = self.env['res.partner.category'].search([('name','=ilike',category)])
            if category_id:
                data['category_id'] = category_id.ids
            else:
                category_id = category_id.create({'name': category})
                data['category_id'] = category_id.ids
        mapping = self.env['res.partner.mapping'].search(
            [
                ('connection_id','=',self.connection_id.id),
                ('is_company','=',True),
                ('remote_id','=',self.remote_id),
            ]
        )
        if mapping:
            mapping.local_id.write(data)
            mapping.is_modified = False
        else:
            partner_id = self.env['res.partner'].create(data)
            mapping = mapping.create(
                {
                    'connection_id': self.connection_id.id,
                    'local_id': partner_id.id,
                    'remote_id': self.remote_id,
                    'imported': True,
                }
            )
        
        return mapping

    def evaluate_contact(self, data):
        data['is_company'] = False
        if 'parent_id' in data:
            company_mapping = self.env['res.partner.mapping'].search(
                [
                    ('connection_id','=',self.connection_id.id),
                    ('is_company','=',True),
                    ('remote_id','=',data['parent_id'])
                ]
            )
            if company_mapping:
                data['parent_id'] = company_mapping.local_id.id
            else:
                raise ValueError(f"Company {data['parent_id']} is not mapped.")
        mapping = self.env['res.partner.mapping'].search(
            [
                ('connection_id','=',self.connection_id.id),
                ('is_company','=',False),
                ('remote_id','=',self.remote_id),
            ]
        )
        if mapping:
            mapping.local_id.write(data)
            mapping.is_modified = False
        else:
            partner_id = self.env['res.partner'].create(data)
            mapping = mapping.create(
                {
                    'connection_id': self.connection_id.id,
                    'local_id': partner_id.id,
                    'remote_id': self.remote_id,
                    'imported': True,
                }
            )
            
        return mapping

    def evaluate_deal(self, data):
        logs = data.pop('logs',False)
        partner_id = data.pop('partner_id',False)
        
        if partner_id:
            partner_mapping = self.env['res.partner.mapping'].search(
                [
                    ('connection_id','=',self.connection_id.id),
                    ('remote_id','=',partner_id)
                ]
            )
            if partner_mapping:
                if len(partner_mapping) > 1:
                    partner_mapping = partner_mapping.filtered(lambda x: not x.is_company)
                data.update(
                    partner_id=partner_mapping.local_id.id,
                    email_from=partner_mapping.local_id.email,
                    phone=partner_mapping.local_id.phone,
                )
            else:
                raise ValueError(f'Customer {partner_id} is not mapped.')
        user_id = self.connection_id.default_user_id or False
        if user_id:
            data['user_id'] = user_id.id
        else:
            user_id = data.pop('user_id',False)
            if user_id:
                user_mapping = self.env['res.users.mapping'].search(
                    [
                        ('connection_id','=',self.connection_id.id),
                        ('remote_id','=',user_id)
                    ]
                )
                if user_mapping:
                    data['user_id'] = user_mapping.local_id.id
                else:
                    raise ValueError(f'User {user_id} is not mapped.')
        
        stage_id = data.pop('stage',False)
        stage_mapping_id = self.connection_id.stage_ids.filtered_domain(
            [('remote_id','=',str(stage_id))]
        )
        if not stage_mapping_id:
            raise ValueError(f'Stage {stage_id} is not mapped.')
        stage_id = stage_mapping_id.local_id
        data['stage_id'] = stage_id.id
        mapping = self.env['crm.lead.mapping'].search(
            [
                ('connection_id','=',self.connection_id.id),
                ('remote_id','=',self.remote_id),
            ]
        )
        if mapping:
            lead_id = mapping.local_id
            lead_id.write(data)
            mapping.is_modified = False
        else:
            lead_id = self.env['crm.lead'].create(data)
            mapping = mapping.create(
                {
                    'connection_id': self.connection_id.id,
                    'local_id': lead_id.id,
                    'remote_id': self.remote_id,
                    'imported': True,
                }
            )
        if logs:
            mapped_log_remote_ids = mapping.log_ids.mapped('remote_id')
            for log in logs:
                if log['id'] not in mapped_log_remote_ids:
                    message_data = {'message_type': 'comment'}
                    user_id = self.connection_id.default_user_id
                    if user_id:
                        message_data['author_id'] = user_id.partner_id.id
                    else:
                        user_remote_id = log['user_id']
                        user_mapping = self.env['res.users.mapping'].search([('remote_id','=',user_remote_id)])
                        if user_mapping:
                            message_data['author_id'] = user_mapping.local_id.partner_id.id
                        else:
                            self.log(
                                f"""
                                    <div class='alert alert-danger' role='alert'>
                                        <span class='font-weight-bold'>
                                            User {user_remote_id} not mapped for log {log['id']}
                                        </span>
                                    </div>
                                """
                            )
                        if log['type'] == 'note':
                            message_data.update(
                                body = log['body'],
                                subtype_xmlid = 'mail.mt_note',
                            )
                        elif log['type'] == 'email':
                            message_data.update(
                                body = f"{log['body']}</br><i>Subject: {log['subject']}</i>",
                                subtype_xmlid = 'mail.mt_comment',
                            )
                        subject = log.get('subject')
                        if subject:
                            message_data.update(subject=subject)
                        message = lead_id.message_post(**message_data)
                        self.env['mail.message.mapping'].create(
                            {
                                'remote_id': log['id'],
                                'local_id': message.id,
                                'parent_id': mapping.id,
                            }
                        )
        if stage_mapping_id.lost:
            lead_id.action_set_lost()
        return mapping

    def evaluate_product(self, data):
        mapping = self.env['product.template.mapping'].search(
            [
                ('connection_id','=',self.connection_id.id),
                ('remote_id','=',self.remote_id),
            ]
        )
        if mapping:
            mapping.local_id.write(data)
            mapping.is_modified = False
        else:
            product_id = self.env['product.template'].create(data)
            mapping = mapping.create(
                {
                    'connection_id': self.connection_id.id,
                    'local_id': product_id.id,
                    'remote_id': self.remote_id,
                    'imported': True,
                }
            )
        
        return mapping

    def evaluate_user(self, data):
        data['login'] = data['email']
        data['sel_groups_1_9_10'] = '10'
        mapping = self.env['res.users.mapping'].search(
            [
                ('connection_id','=',self.connection_id.id),
                ('remote_id','=',self.remote_id),
            ]
        )
        if mapping:
            mapping.local_id.write(data)
            mapping.is_modified = False
        else:
            user_id = self.env['res.users'].create(data)
            mapping = mapping.create(
                {
                    'connection_id': self.connection_id.id,
                    'local_id': user_id.id,
                    'remote_id': self.remote_id,
                    'imported': True,
                }
            )
        return mapping


