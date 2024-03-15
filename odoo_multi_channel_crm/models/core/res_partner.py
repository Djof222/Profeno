# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    mapping_ids = fields.One2many('res.partner.mapping','local_id','Mappings')
   
    @api.model
    def create(self,vals):
        res = super(ResPartner,self).create(vals)
        cxt = self.env.context
        if res and cxt.get('type')!='import':
            channel_realtime_syn_on = self.env['channel.connection'].search([('connected','=',True)])
            for channel_realtime_sync in channel_realtime_syn_on:
                if channel_realtime_sync.realtime_data_sync==True:
                    model ="res.partner" 
                    channel_data_sync = getattr(channel_realtime_sync, f'{channel_realtime_sync.channel}_export_data',None)
                    data = channel_data_sync(model,res)
        return res

    def write(self,vals):
        self.mapping_ids.write({'is_modified': True})
        cxt = self.env.context
        res = super(ResPartner,self).write(vals)
        if res and cxt.get('type')!='import':
           if 'update_contact' not in cxt:
                check_realtime_syn_on = self.env['channel.connection'].search([('connected','=',True)])
                for channel_realtime_sync in check_realtime_syn_on:
                    if channel_realtime_sync.realtime_data_sync==True:
                        model ="res.partner"
                        mapping_id = self.env['res.partner.mapping'].search([('local_id','in',self.ids)])
                        channel_data_sync = getattr(channel_realtime_sync, f'{channel_realtime_sync.channel}_update_data',None)
                        data = channel_data_sync(model,mapping_id)
        return res
    
    def unlink(self):
        mapping_data = self.env['res.partner.mapping'].search([('local_id','in',self.ids)])
        channels = self.env['channel.connection'].search([('connected','=',True)])
        cxt = self.env.context
        if (cxt.get('type')!='import' or cxt.get('type') is None):
            for channel in channels:
                if channel.realtime_delete == True:
                    channel_delete_data = getattr(channel, f'{channel.channel}_delete_data',None)
                    resp=channel_delete_data(self._name,mapping_data)

        res=super().unlink()
        return res
