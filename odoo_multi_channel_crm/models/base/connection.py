# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import fields, models


class ChannelConnection(models.Model):
    _name = 'channel.connection'
    _description = 'Channel Connection'

    def _inverse_channel(self):
        for rec in self:
            rec._set_info()

    def _set_info(self):
        self.blog_url = '#'

    name = fields.Char('Connection Name',required=True)
    image = fields.Image('Image',max_width=128,max_height=128)
    color = fields.Char(default='#000000',required=True)
    blog_url = fields.Char('Blog Link')

    channel = fields.Selection([],'Channel',required=True,inverse=_inverse_channel)
    connected = fields.Boolean('Connected')
    evaluate = fields.Boolean('Auto Evaluate')
    api_limit = fields.Integer('API Limit Per Page',default=100,required=True)
    stage_ids = fields.One2many('channel.stage.mapping','connection_id','Pipelines Stages')
    default_user_id = fields.Many2one(
        comodel_name='res.users',
        string='Default Sales Person',
        help='If selected, selected user will be assigned to deals on odoo.',
    )
    realtime_delete = fields.Boolean(string="Realtime delete")
    realtime_data_sync = fields.Boolean(string="Realtime data sync")
   
    
    partner_mapping_ids = fields.One2many('res.partner.mapping','connection_id','Partner Mappings')
    lead_mapping_ids = fields.One2many('crm.lead.mapping','connection_id','Lead Mappings')
    product_mapping_ids = fields.One2many('product.template.mapping','connection_id','Product Mappings')
    feed_ids = fields.One2many('channel.feed','connection_id','Feeds')

    cron_company = fields.Boolean('Company')
    cron_contact = fields.Boolean('Contact')
    cron_deal = fields.Boolean('Deal')
    cron_product = fields.Boolean('Product')
    cron_contact_next_page = fields.Char('Contact Next Page')
    cron_company_next_page = fields.Char('Company Next Page')
    cron_deal_next_page = fields.Char('Deal Next Page')
    cron_product_next_page = fields.Char('Product Next Page')

    def connect(self):
        self.ensure_one()
        self = self.sudo()
        message = ''
        channel_connect = getattr(self, f'{self.channel}_connect',None)
        assert channel_connect
        status, msg = channel_connect()
        self.connected = status
        if status:
            message=f"""
                <div class='alert alert-success' role='alert'>
                    <span class='font-weight-bold'>
                        {msg}
                    </span>
                </div>
            """
        else:
            message=f"""
                <div class='alert alert-danger' role='alert'>
                    <span class='font-weight-bold'>
                        Connection failed {msg}.
                    </span>
                </div>
            """
        return self.env['wk.wizard.message'].genrated_message(message)

    def disconnect(self):
        self.ensure_one()
        self.sudo().write({'connected': False})

    def import_data(self, object_type, **kw):
        self = self.sudo()
        remote_ids = []
        feed_ids = self.env['channel.feed']
        kw['api_limit'] = self.api_limit
        while True:
            res = self.import_page(object_type, **kw)
            remote_ids.extend(res[0])
            feed_ids+=res[1]
            kw = res[2]
            if kw.get('done'):
                break
        return remote_ids, feed_ids

    def import_page(self, object_type, **kw):
        channel_import_data = getattr(self, f'{self.channel}_import_data',None)
        assert channel_import_data
        remote_ids, data_list, kw = channel_import_data(object_type,**kw)
        feed_ids = self.env['channel.feed'].sudo().create(data_list)
        if remote_ids:
            self.env['channel.log'].sudo().create(
                {
                    'connection_id': self.id,
                    'feed_ids': feed_ids.ids,
                    'operation': 'import',
                    'name': object_type,
                }
            )
            self._cr.commit()
        return remote_ids, feed_ids, kw

    def export_data(self, model, local_ids, operation):
        self = self.sudo()
        if model == 'res.partner':
            object_type = 'partner'
        elif model == 'crm.lead':
            object_type = 'deal'
        elif model == 'product.template':
            object_type = 'product'
        else:
            raise NotImplementedError('Not Implemented')
        mappings = self.env[f'{model}.mapping'].search(
            [
                ('connection_id','=',self.id),
                ('local_id','in',local_ids),
            ]
        )
        if operation == 'export':
            local_ids = set(local_ids) - set(mappings.mapped('local_id').ids)
            records = self.env[model].search([('id','in',list(local_ids))])
            if not records:
                return
            channel_export_data = getattr(self, f'{self.channel}_export_data',None)
            assert channel_export_data
            success_ids, error_ids, log_lines_data = channel_export_data(model, records)
        elif operation == 'update':
            if not mappings:
                return
            channel_update_data = getattr(self, f'{self.channel}_update_data',None)
            assert channel_update_data
            success_ids, error_ids, log_lines_data = channel_update_data(model, mappings)
        self.env['channel.log'].sudo().create(
            {
                'connection_id': self.id,
                'operation': operation,
                'name': object_type,
                'line_ids': log_lines_data
            }
        )
        return success_ids, error_ids

    def cron_evaluate(self):
        feeds = self.env['channel.feed'].search([('state','=','draft')])
        feeds.evaluate()

    def cron_import_company(self):
        connections = self.search([('cron_company','=',True)])
        for connection in connections:
            kw = {
                'api_limit': connection.api_limit,
                'next_page': int(connection.cron_company_next_page),
            }
            while True:
                *_, kw = connection.with_context(
                    default_connection_id=connection.id).import_page('company',**kw)
                next_page = kw.get('next_page')
                connection.cron_company_next_page = next_page
                if kw.get('done'):
                    break

    def cron_import_contact(self):
        connections = self.search([('cron_contact','=',True)])
        for connection in connections:
            kw = {
                'api_limit': connection.api_limit,
                'next_page': int(connection.cron_contact_next_page),
            }
            while True:
                *_, kw = connection.with_context(
                    default_connection_id=connection.id).import_page('contact',**kw)
                next_page = kw.get('next_page')
                connection.cron_contact_next_page = next_page
                if kw.get('done'):
                    break

    def cron_import_deal(self):
        connections = self.search([('cron_deal','=',True)])
        for connection in connections:
            kw = {
                'api_limit': connection.api_limit,
                'next_page': int(connection.cron_deal_next_page),
            }
            while True:
                *_, kw = connection.with_context(
                    default_connection_id=connection.id).import_page('deal',**kw)
                next_page = kw.get('next_page')
                connection.cron_deal_next_page = next_page
                if kw.get('done'):
                    break

    def cron_import_product(self):
        connections = self.search([('cron_product','=',True)])
        for connection in connections:
            kw = {
                'api_limit': connection.api_limit,
                'next_page': int(connection.cron_product_next_page),
            }
            while True:
                *_, kw = connection.with_context(
                    default_connection_id=connection.id).import_page('product',**kw)
                next_page = kw.get('next_page')
                connection.cron_product_next_page = next_page
                if kw.get('done'):
                    break
