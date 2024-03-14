# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
	"name"                 : "Vtiger Odoo Connector",
	"summary"              : """""",
	"category"             : "CRM",
	"version"              : "2.0.0",
	"sequence"             : 1,
	"author"               : "Webkul Software Pvt. Ltd.",
	"license"              : "Other proprietary",
	"website"              : "webkul.com",
	"description"          : """""",
	"depends"              : [
		'odoo_multi_channel_crm',
	],
	"data"                 : [
		"security/ir.model.access.csv",
		
		"wizard/channel_import.xml",
        "data/connection.xml",
		"views/connection.xml",
		"views/pipeline_view.xml",
		"views/crm_lead_view.xml",
		"views/mapping_pipeline_view.xml",
		"views/stage_mapping_view.xml",
	],

	"images"       : ['static/description/banner.png'],
	"application"  : True,
	"price"		   : 100,
	"currency"     : "USD",
	"pre_init_hook": "pre_init_check",
}
