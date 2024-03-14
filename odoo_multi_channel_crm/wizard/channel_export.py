# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import fields, models

dic = {'res.partner':'Partner', 'product.template':'Product','crm.lead':'Lead'}

class ExportWizard(models.TransientModel):
    _name = 'channel.export'
    
    _description = 'Export Wizard'

    def _default_object_type(self):
        return self._context.get('active_model')

    def _default_local_ids(self):
        return self._context.get('active_ids')

    connection_id = fields.Many2one(
        comodel_name='channel.connection',
        string='Connection',
        domain=[('connected','=',True)],
        required=True,
    )
    channel = fields.Selection(related='connection_id.channel')
    operation = fields.Selection(
        selection=[
            ('export','Export'),
            ('update','Update'),
        ],
        default='update',
        required=True,
    )
    object_type = fields.Selection(
        selection=[
            ('res.partner','Company/Contact'),
            ('crm.lead','Deal'),
            ('product.template','Product'),
        ],
        default=_default_object_type,
        required=True,
        readonly=True,
    )
    local_ids = fields.Char('Object IDs',default=_default_local_ids,required=True,readonly=True)

    def export_button(self):
        message=''
        try:
            res = self.connection_id.export_data(self.object_type,eval(self.local_ids),self.operation)
            
        except Exception as e:
            message = f"""
                <div class='alert alert-danger' role='alert'>
                    <span class='font-weight-bold'>
                        {e.args[0]}
                    </span>
                </div>
            """
        else:
            if res:
                success_ids, error_ids = res
                if success_ids:
                    message+=f"""
                            <div class='alert alert-success' role='alert'>
                                <span class='font-weight-bold'>
                                    {dic[self.object_type]} Successfully {self.operation.capitalize()} Ids. {','.join(success_ids)}
                                </span>
                            </div>
                        """
                    if error_ids:
                        message+='<hr>'
                if error_ids:
                    message+=f"""
                            <div class='alert alert-danger' role='alert'>
                                <span class='font-weight-bold'>
                                   Somthing went wrong. {','.join(error_ids)}
                                </span>
                            </div>
                        """
            else:
                if self.operation=='export':
                    message = f"""
                        <div class='alert alert-danger' role='alert'>
                            <span class='font-weight-bold'>
                                Selected records are already exported.
                            </span>
                        </div>
                    """
                elif self.operation=='update':
                    message = f"""
                        <div class='alert alert-danger' role='alert'>
                            <span class='font-weight-bold'>
                                Selected records are not mapped.
                            </span>
                        </div>
                    """
        return self.env['wk.wizard.message'].genrated_message(message)
