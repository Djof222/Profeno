# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import fields, models


class ProductMapping(models.Model):
	_name = 'product.template.mapping'
	_inherit = 'base.mapping'
	_description = 'Product Mapping'

	local_id = fields.Many2one('product.template','Record',required=True, ondelete='cascade')
