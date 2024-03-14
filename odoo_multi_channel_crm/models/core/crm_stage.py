# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from random import randint
from odoo import fields, models


class CRMStage(models.Model):
	_inherit = 'crm.stage'

	color = fields.Integer('Color', default=randint(1, 11))
