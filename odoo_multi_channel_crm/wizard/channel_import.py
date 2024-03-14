# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import fields, models


class ImportWizard(models.TransientModel):
    _name = 'channel.import'
    _description = 'Import Wizard'

    connection_id = fields.Many2one(
        comodel_name='channel.connection',
        string='Connection',
        domain=[('connected','=',True)],
        required=True,
        readonly=True,
    )
    channel = fields.Selection(related='connection_id.channel')
    object_type = fields.Selection(
        selection=[
            ('company','Company'),
            ('contact','Contact'),
            ('deal','Deal'),
            ('product','Product'),
            ('user','User'),
        ],
        string='Object',
        required=True,
    )

    def import_button(self):
     
        kw = {}
        feed_ids = None
        try:
            channel_get_filter = getattr(self, f'{self.channel}_get_filter',None)
            assert channel_get_filter
            kw = channel_get_filter()
            remote_ids, feed_ids = self.connection_id.import_data(
                self.object_type,
                **kw
            )
        except Exception as e:
            message=f"""
                <div class='alert alert-danger' role='alert'>
                    <span class='font-weight-bold'>
                        Error occurred. {e}
                    </span>
                </div>
            """
        else:
            message=f"""
                <div class='alert alert-success' role='alert'>
                    <span class='font-weight-bold'>
                       {self.object_type} Successfully imported. {','.join(remote_ids)}
                    </span>
                </div>
            """
        if feed_ids and self.connection_id.evaluate:
            success_ids, error_ids = feed_ids.evaluate()
            self._cr.commit()
            if success_ids:
                message += f"""
                    <hr>
                    <div class='alert alert-success' role='alert'>
                        <span class='font-weight-bold'>
                           {self.object_type.capitalize()} Successfully Evaluated. {','.join(success_ids)}
                        </span>
                    </div>
                """
            if error_ids:
                message += f"""
                    <hr>
                    <div class='alert alert-danger' role='alert'>
                        <span class='font-weight-bold'>
                            Failed to evaluate. {','.join(error_ids)}
                        </span>
                    </div>
                """
        return self.env['wk.wizard.message'].genrated_message(message)
