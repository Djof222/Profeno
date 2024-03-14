# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import fields, models

class Pipeline(models.Model):
    _name = "crm.pipeline"
    _description = "Pipelines"

    name = fields.Char("Name", required=True)
    stage_ids = fields.Many2many(
        "crm.stage",
        string="Stages")
