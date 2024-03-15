# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import fields, models


class ResUsers(models.Model):
	_inherit = 'res.users'

	mapping_ids = fields.One2many('res.users.mapping','local_id','Mappings')
 
   
	def write(self,vals):
		self.mapping_ids.write({'is_modified': True})
		return super().write(vals)
