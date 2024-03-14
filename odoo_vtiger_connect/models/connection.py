# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

import requests
import json

from odoo import fields, models
from odoo.http import request
from hashlib import md5
from logging import getLogger

_logger = getLogger(__name__)

class ChannelConnection(models.Model):
    _inherit = 'channel.connection'
    
    vt_base_url = fields.Char("Base Url")
    channel = fields.Selection(
        selection_add=[('vtiger', 'Vtiger')],
        ondelete={'vtiger': 'cascade'})
    vt_access_key = fields.Char('Access Key')
    vt_username = fields.Char('Username')
    
    default_category_id = fields.Many2one(
        'product.category', 'Default Category')
    pipeline_ids = fields.One2many(
        'crm.pipeline.mapping',
        'connection_id',
        'Pipelines'
    )

    def vtiger_connect(self):
        resp = self._vtiger_login()
        if resp.get("status"):
            sessionName = resp.get("sessionName")
            self._get_vtiger_pipeline_stages(sessionName)
            self._vtiger_logout(sessionName)
            return True, resp.get("message")
        else:
            return False, resp.get("message")

    def _vtiger_login(self):
        status, sessionName, msg= False, '', ''
        url = f"{self.vt_base_url}/webservice.php"
        params = {
            "operation": "getchallenge",
            "username": self.vt_username,
        }
        headers = {}
        try:
            user_agent = request.httprequest.environ.get('HTTP_USER_AGENT', '')
            headers["User-Agent"] = user_agent
        except Exception as e:
            _logger.debug("### User-Agent Exception - %r ",e)
        resp = requests.get(url, headers=headers, params=params, verify=False)
        respData = json.loads(resp.text)
        if respData.get("success"):
            result = respData.get("result")
            token = result.get("token")
            accessKey = str(token) + self.vt_access_key
            logindata = {
                "operation": "login",
                "username": self.vt_username,
                "accessKey": md5(accessKey.encode('utf-8')).hexdigest(),
            }
            resp = requests.post(url, headers=headers, data=logindata, verify=False)
            resData = json.loads(resp.text)
            if resData.get("success"):
                result = resData.get("result")
                sessionName = result.get("sessionName")
                status = True
                _logger.info(">>> Successfully login to vtiger. <<<")
                return {"status": status, "sessionName": sessionName, "message": "Successfully connected to Vtiger."}
            else:
                error = resData.get("error")
                return {"status": status, "sessionName": sessionName, "message": error.get("message")}
        else:
            error = respData.get("error")
            return {"status": status, "sessionName": sessionName, "message": error.get("message")}

    def _vtiger_logout(self, sessionName):
        if sessionName:
            url = f"{self.vt_base_url}/webservice.php"
            logoutdata = {
                "operation": "logout",
                "sessionName": sessionName,
            }
            headers = {}
            try:
                user_agent = request.httprequest.environ.get('HTTP_USER_AGENT', '')
                headers["User-Agent"] = user_agent
            except Exception as e:
                _logger.debug("### User-Agent Exception - %r ",e)

            resp = requests.post(url, headers=headers, data=logoutdata, verify=False)
            logoutresp = json.loads(resp.text)
            if logoutresp.get("success"):
                _logger.info(">>> Successfully logout from vtiger. <<<")
            else:
                err = logoutresp.get("error",{}).get("message")
                _logger.info(">>> Error while vtiger logout - %r <<<",err)
        return True
    
    def _get_vtiger_pipeline_stages(self, sessionName):
        api_url = f"{self.vt_base_url}/webservice.php"
        params = {
            "operation": "describe",
            "sessionName": sessionName,
            "elementType": "Potentials"
        }
        resp = self.env["vtiger.sync"].callVtigerApi(api_url, "get", params=params)
        if resp.get("status"):
            result = resp.get("result")
            pipelines = [field["type"]["picklistValues"] for field in result.get("fields") if field["name"] == "pipeline"]
            stages = [field["type"]["picklistValues"] for field in result.get("fields") if field["name"] == "sales_stage"]
            for pipeline in pipelines[0]:
                pipeline_mapping = self.env["crm.pipeline.mapping"].search(
                    [("connection_id","=",self.id),("remote_id","=",pipeline.get("value"))]
                )
                if not pipeline_mapping:
                    self.env["crm.pipeline.mapping"].create(
                        {
                            "connection_id": self.id,
                            "name": pipeline.get("label"),
                            "remote_id": pipeline.get("value")
                        }
                    )
            for stage in stages[0]:
                stage_mapping = self.env["channel.stage.mapping"].search(
                    [("connection_id","=",self.id),("remote_id","=",stage.get("value"))]
                )
                if not stage_mapping:
                    self.env["channel.stage.mapping"].create(
                        {
                            "connection_id": self.id,
                            "name": stage.get("label"),
                            "remote_id": stage.get("value")
                        }
                    )
        return True

    def vtiger_export_data(self, model, records):
        resp = [[],[],[]]
        if model=="res.partner":
            contacts = records.filtered(lambda x: x.is_company == False)
            companies = records.filtered(lambda x: x.is_company == True)
            resp = self._export_company(companies)
            resp1 = self._export_contact(contacts)
            resp[0].extend(resp1[0])
            resp[1].extend(resp1[1])
            resp[2].extend(resp1[2])
        elif model=="crm.lead":
            resp = self._export_lead(records)
        elif model=="product.template":
            resp = self._export_product(records)
        return resp[0], resp[1], resp[2]

    def _create_mapping(self, model, data):
        obj = self.env[model].create(data)
        return obj.id

    def vtiger_update_data(self, model, records):
        resp = [[],[],[]]
        if model=="res.partner":
            contacts = records.filtered(lambda x: x.is_company == False)
            companies = records.filtered(lambda x: x.is_company == True)
            resp = self._update_company(companies)
            resp1 = self._update_contact(contacts)
            resp[0].extend(resp1[0])
            resp[1].extend(resp1[1])
            resp[2].extend(resp1[2])
        elif model=="crm.lead":
            resp = self._update_lead(records)
        elif model=="product.template":
            resp = self._update_product(records)
        return resp[0], resp[1], resp[2]

    def vtiger_import_data(self, object_type, **kw):
        if object_type=="contact":
            resp = self._import_contact(**kw)
        elif object_type=="company":
            resp = self._import_company(**kw)
        elif object_type=="deal":
            resp = self._import_deal(**kw)
        elif object_type=="product":
            resp = self._import_product(**kw)
        elif object_type=="user":
            resp = self._import_user(**kw)
        else:
            raise NotImplementedError("Not implemented - %s"%object_type)
        return resp
