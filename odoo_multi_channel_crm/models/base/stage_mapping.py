# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import api, fields, models


class StageMapping(models.Model):
	_name = 'channel.stage.mapping'
	_description = 'Channel Stage Mapping'

	connection_id = fields.Many2one('channel.connection','Connection',required=True)
	name = fields.Char('CRM Stage Name', readonly=True, required=True)
	remote_id = fields.Char('CRM Stage', readonly=True, required=True)
	local_id = fields.Many2one(
		comodel_name='crm.stage',
		string='Stage',
	)
	lost = fields.Boolean()

	_sql_constraints = [
		(
			'connection_stage_uniq',
			'unique (connection_id,remote_id)',
			'Each stage must be unique per connection.',
		)
	]
