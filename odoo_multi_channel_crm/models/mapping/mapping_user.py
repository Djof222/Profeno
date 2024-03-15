# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import fields, models


class UserMapping(models.Model):
	_name = 'res.users.mapping'
	_inherit = 'base.mapping'
	_description = 'User Mapping'

	local_id = fields.Many2one('res.users','Record',required=True, ondelete='cascade')
