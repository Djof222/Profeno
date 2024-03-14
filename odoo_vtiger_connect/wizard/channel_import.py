# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import fields, models

class ImportWizard(models.TransientModel):
    _inherit = 'channel.import'

    vt_filter = fields.Selection(
        selection=[('all','All'),('id','By Id')],
        string='Filter'
    )
    vtiger_id = fields.Char("Vtiger Id")

    def vtiger_get_filter(self):
        fltr = self.vt_filter
        kw = {"vtiger_filter":fltr}
        if fltr=="id":
            kw["vtiger_id"]=self.vtiger_id
        return kw
