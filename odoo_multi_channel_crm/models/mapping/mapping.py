# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import fields, models


class Mapping(models.AbstractModel):
	_name = 'base.mapping'
	_description = 'Mapping'

	connection_id = fields.Many2one('channel.connection','Connection',required=True)
	channel = fields.Selection(related='connection_id.channel')
	remote_id = fields.Char('Store ID',required=True)
	imported = fields.Boolean('Imported')
	is_modified = fields.Boolean('Modified')

	_sql_constraints = [
		(
			'connection_remote_id_uniq',
			'unique (connection_id,remote_id)',
			'Each Store ID must be unique per connection.',
		)
	]
