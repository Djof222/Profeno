# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from . import controllers
from . import models
from . import wizard
from odoo import exceptions

def pre_init_check(cr):
    from odoo.service import common
    # from odoo.exceptions import Warning
    version_info = common.exp_version()
    server_serie = version_info.get('server_serie')
    if not 16 < float(server_serie) <= 17:
        raise exceptions.Warning(
            'Module support Odoo series 17.0 found {}.'.format(server_serie))
