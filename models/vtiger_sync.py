# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

import requests
import json

from odoo import models
from odoo.http import request
from logging import getLogger

_logger = getLogger(__name__)

class VtigerSync(models.TransientModel):
    _name = "vtiger.sync"
    _description = "Vtiger Synchronization"

    def callVtigerApi(self, url, method, data={}, params={}):
        status = True
        headers = {}
        try:
            user_agent = request.httprequest.environ.get('HTTP_USER_AGENT', '')
            headers.update({'User-Agent': user_agent})
        except Exception as e:
            _logger.debug("## USER_AGENT Error: %r",e)
        if method == 'get' :
            response = requests.get(
                url, headers=headers, params=params, verify=False)
        elif method == 'post' :
            response = requests.post(
                url, headers=headers, data=data, params=params, verify=False)
        
        response_data = json.loads(response.text)
        if response_data.get('success'):
            result = response_data.get('result')
            return {'status': True, 'result': result, 'message':''}
        else:
            err_msg = response_data.get('error',{}).get('message','')
            return {'status': False, 'result': '', 'message': err_msg}
