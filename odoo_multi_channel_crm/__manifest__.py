# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
	'name'    : 'Odoo Multi CRM Solution',
	'category': 'CRM',
	'version' : '1.3.4',
	'sequence': 1,
	'author'  : 'Webkul Software Pvt. Ltd.',
	'license' : 'Other proprietary',

	'summary'    : 'Odoo Multi-CRM Solution helps you to connect multiple customer relationship management solutions to your Odoo. ',
	'description': '''
		Odoo Multi CRM Solution
		Odoo Multiple CRM Connector
		Multi CRM Connector
		CRM Connector
		CRM Connector Base
		Multi CRM Base Connector
	''',

	'website': 'webkul.com',
	# 'live_test_url': '',

	'depends': [
		'crm',
		'product',
		'wk_wizard_messages',
	],
	'data': [
		'security/security.xml',
		'security/ir.model.access.csv',

		'wizard/channel_export.xml',
		'wizard/channel_import.xml',

		'views/menus.xml',
		'views/base/connection.xml',
		'views/base/log.xml',
		'views/feed.xml',
		'views/mapping/mapping_lead.xml',
		'views/mapping/mapping_partner.xml',
		'views/mapping/mapping_product.xml',
		'views/mapping/mapping_user.xml',
		'views/core/crm_lead.xml',
		'views/core/crm_stage.xml',
		'views/core/product_template.xml',
		'views/core/res_partner.xml',
		'views/core/res_users.xml',

		'data/cron.xml',
	],
	'assets': {
		'web.assets_backend': [
			'odoo_multi_channel_crm/static/src/css/dashboard.css',
			'odoo_multi_channel_crm/static/src/js/dashboard.js',
			'odoo_multi_channel_crm/static/src/xml/connections_dashboard.xml',
			'odoo_multi_channel_crm/static/src/xml/connection_dashboard.xml',
		],
	},

	'images'       : ['static/description/banner.png'],
	'application'  : True,
	'price'        : 99,
	'currency'     : 'USD',
	'pre_init_hook': 'pre_init_check',
}
