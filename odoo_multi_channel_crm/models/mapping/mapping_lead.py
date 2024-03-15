# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import fields, models


class LeadMapping(models.Model):
	_name = 'crm.lead.mapping'
	_inherit = 'base.mapping'
	_description = 'Lead Mapping'

	local_id = fields.Many2one('crm.lead','Record',required=True)
	log_ids = fields.One2many('mail.message.mapping','parent_id', 'Logs')


class LogMapping(models.Model):
	_name = 'mail.message.mapping'
	_description = 'Lead Log Mapping'
	_rec_name = 'remote_id'

	parent_id = fields.Many2one('crm.lead.mapping','Deal Mapping', required=True, ondelete='cascade')
	remote_id = fields.Char('Store ID', required=True)
	local_id = fields.Many2one('mail.message','Record', required=True, ondelete='cascade')
