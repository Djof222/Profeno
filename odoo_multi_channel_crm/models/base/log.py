# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import fields, models


class ChannelLog(models.Model):
	_name = 'channel.log'
	_description = 'Channel Log'
	_order = 'create_date desc'

	user_id = fields.Many2one('res.users','User',default=lambda self: self._uid,required=True)
	connection_id = fields.Many2one('channel.connection','Connection',required=True)
	channel = fields.Selection(related='connection_id.channel')
	operation = fields.Selection(
		selection=[
			('import','Import'),
			('export','Export'),
			('update','Update'),
		],
		string='Operation',
		required=True,
	)
	name = fields.Selection(
		selection=[
			('company','Company'),
			('contact','Contact'),
			('partner','Company/Contact'),
			('deal','Deal'),
			('product','Product'),
			('user','User'),
		],
		string='Name',
		required=True,
	)
	feed_ids = fields.One2many('channel.feed','log_id','Feeds')
	line_ids = fields.One2many('channel.log.line','log_id','Lines')


class ChannelLogLine(models.Model):
	_name = 'channel.log.line'
	_description = 'Channel Log Line'

	log_id = fields.Many2one('channel.log','Log',required=True,ondelete='cascade')
	local_id = fields.Integer('Record ID',required=True)
	remote_id = fields.Char('Store ID')
	success = fields.Boolean('Success')
	error = fields.Char('Error')
