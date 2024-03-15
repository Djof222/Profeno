# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import fields, models


class PartnerMapping(models.Model):
    _name = 'res.partner.mapping'
    _inherit = 'base.mapping'
    _description = 'Partner Mapping'

    local_id = fields.Many2one('res.partner','Record',required=True, ondelete='cascade')
    is_company = fields.Boolean('Is a Company',related='local_id.is_company', ondelete='cascade')

    _sql_constraints = [
        (
            'connection_remote_id_uniq',
            'unique(connection_id,remote_id,is_company)',
            'Each Store ID must be unique per connection.',
        )
    ]
   
   
