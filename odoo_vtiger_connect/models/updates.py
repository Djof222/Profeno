# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

import json

from odoo import fields, models
from logging import getLogger

_logger = getLogger(__name__)

class Updates(models.Model):
    _inherit = 'channel.connection'

    def _update_contact(self, mappings):
        api_url = f"{self.vt_base_url}/webservice.php"
        connection = self._vtiger_login()
        success, failure, log_line_data = [], [], []
        if connection.get("status"):
            for mapping in mappings:
                log_data = {}
                parent_id = False
                contact = mapping.local_id
                udomain = [("connection_id","=",self.id),("local_id","=",contact.user_id.id)]
                user_mapping = self.env["res.users.mapping"].search(udomain, limit=1)
                if not user_mapping:
                    continue
                if contact.parent_id:
                    domain = [("connection_id","=",self.id),("is_company","=",True),("local_id","=",contact.parent_id.id)]
                    parent_id = self.env["res.partner.mapping"].search(domain, limit=1).remote_id
                name = contact.name.split()
                firstname = name[0]
                lastname = " ".join(name[1:])
                data = {
                    "id": mapping.remote_id,
                    "firstname": firstname,
                    "lastname": lastname,
                    "email": contact.email,
                    "mobile": contact.mobile,
                    "phone": contact.phone,
                    "mailingcountry": contact.country_id.code,
                    "mailingstate": contact.state_id.name,
                    "mailingcity": contact.city,
                    "mailingstreet": contact.street,
                    "mailingzip": contact.zip,
                    "contacttype": "Customer",
                    "assigned_user_id": user_mapping.remote_id,
                    "account_id": parent_id
                }
                postData = {
                    "operation": "update",
                    "sessionName": connection.get("sessionName"),
                    "element": json.dumps(data),
                    "elementType": "Contacts",
                }
                res = self.env["vtiger.sync"].callVtigerApi(api_url, "post", data=postData)
                if res.get("status"):
                    success.append(str(contact.id))
                    result = res.get("result")
                    log_data.update(
                        remote_id = result.get("id"),
                        local_id = contact.id,
                        success = True,
                        error = "Successfully updated"
                    )
                else:
                    failure.append(str(contact.id))
                    log_data.update(
                        local_id = contact.id,
                        success = False,
                        error = res.get("message")
                    )
                log_line_data.append((0,0,log_data))
            self._vtiger_logout(connection.get("sessionName"))
        return success, failure, log_line_data
    
    def _update_lead(self, mappings):
        api_url = f"{self.vt_base_url}/webservice.php"
        connection = self._vtiger_login()
        success, failure, log_line_data = [], [], []
        if connection.get("status"):
            for mapping in mappings:
                log_data = {}
                lead = mapping.local_id
                remote_company = remote_contact = False
                udomain = [("connection_id","=",self.id),("local_id","=",lead.user_id.id)]
                user_mapping = self.env["res.users.mapping"].search(udomain, limit=1)
                if not user_mapping:
                    continue
                if lead.partner_name:
                    company = self.env["res.partner"].search([("is_company","=",True),("name","=",lead.partner_name)])
                    cdomain = [("connection_id","=",self.id),("is_company","=",True),("local_id","=",company.id)]
                    remote_company = self.env["res.partner.mapping"].search(cdomain, limit=1).remote_id
                if lead.partner_id:
                    pdomain = [("connection_id","=",self.id),("is_company","=",False),("local_id","=",lead.partner_id.id)]
                    remote_contact = self.env["res.partner.mapping"].search(pdomain, limit=1).remote_id
                pipeline_mapping = self.env["crm.pipeline.mapping"].search(
                    [("connection_id","=",self.id),("local_id","=",lead.pipeline_id.id)], limit=1
                )
                stage_mapping = self.env["channel.stage.mapping"].search(
                    [("connection_id","=",self.id),("local_id","=",lead.stage_id.id)], limit=1
                )
                data = {
                    "id": mapping.remote_id,
                    "potentialname": lead.name,
                    "probability": lead.probability,
                    "forcast_amount": lead.expected_revenue,
                    "is_closed": True if lead.probability == 0 else False,
                    "closingdate": str(lead.date_deadline),
                    "description": lead.description,
                    "lost_reason": lead.lost_reason.name,
                    "pipeline": pipeline_mapping.remote_id,
                    "sales_stage": stage_mapping.remote_id,
                    "leadsource": lead.source_id.name,
                    "assigned_user_id": user_mapping.remote_id,
                    "related_to": remote_company,
                    "contact_id": remote_contact
                }
                postData = {
                    "operation": "update",
                    "sessionName": connection.get("sessionName"),
                    "element": json.dumps(data),
                    "elementType": "Potentials",
                }
                res = self.env["vtiger.sync"].callVtigerApi(api_url, "post", data=postData)
                if res.get("status"):
                    success.append(str(lead.id))
                    result = res.get("result")
                    log_data.update(
                        remote_id = result.get("id"),
                        local_id = lead.id,
                        success = True,
                        error = "Successfully updated"
                    )
                else:
                    failure.append(str(lead.id))
                    log_data.update(
                        local_id = lead.id,
                        success = False,
                        error = res.get("message")
                    )
                log_line_data.append((0,0,log_data))
            self._vtiger_logout(connection.get("sessionName"))
        return success, failure, log_line_data
    
    def _update_product(self, mappings):
        api_url = f"{self.vt_base_url}/webservice.php"
        connection = self._vtiger_login()
        success, failure, log_line_data = [], [], []
        if connection.get("status"):
            for mapping in mappings:
                log_data = {}
                product = mapping.local_id
                udomain = [("connection_id","=",self.id),("local_id","=",product.user_id.id)]
                user_mapping = self.env["res.users.mapping"].search(udomain, limit=1)
                if not user_mapping:
                    continue
                data = {
                    "id": mapping.remote_id,
                    "productname": product.name,
                    "productcode": product.default_code,
                    "discontinued": product.sale_ok,
                    "description": product.description,
                    "productcategory": product.categ_id.name,
                    "item_barcode": product.barcode,
                    "unit_price": product.list_price,
                    "purchase_cost": product.standard_price,
                    "qtyinstock": product.qty_available,
                    "assigned_user_id": user_mapping.remote_id
                }
                postData = {
                    "operation": "update",
                    "sessionName": connection.get("sessionName"),
                    "element": json.dumps(data),
                    "elementType": "Products",
                }
                res = self.env["vtiger.sync"].callVtigerApi(api_url, "post", data=postData)
                if res.get("status"):
                    success.append(str(product.id))
                    result = res.get("result")
                    log_data.update(
                        remote_id = result.get("id"),
                        local_id = product.id,
                        success = True,
                        error = "Successfully updated"
                    )
                else:
                    failure.append(str(product.id))
                    log_data.update(
                        local_id = product.id,
                        success = False,
                        error = res.get("message")
                    )
                log_line_data.append((0,0,log_data))
            self._vtiger_logout(connection.get("sessionName"))
        return success, failure, log_line_data
    
    def _update_company(self, mappings):
        api_url = f"{self.vt_base_url}/webservice.php"
        connection = self._vtiger_login()
        success, failure, log_line_data = [], [], []
        if connection.get("status"):
            for mapping in mappings:
                log_data = {}
                company = mapping.local_id
                udomain = [("connection_id","=",self.id),("local_id","=",company.user_id.id)]
                user_mapping = self.env["res.users.mapping"].search(udomain, limit=1)
                if not user_mapping:
                    continue
                data = {
                    "id": mapping.remote_id,
                    "accountname": company.name,
                    "accounttype": "Customer",
                    "email1": company.email,
                    "website": company.website,
                    "phone": company.phone,
                    "industry": company.category_id.name,
                    "assigned_user_id": user_mapping.remote_id,
                    "bill_street": company.street,
                    "ship_street": company.street,
                    "bill_city": company.city,
                    "ship_city": company.city,
                    "bill_state": company.state_id.name,
                    "ship_state": company.state_id.name,
                    "bill_country": company.country_id.code,
                    "ship_country":company.country_id.code,
                    "bill_code": company.zip,
                    "ship_code": company.zip
                }
                postData = {
                    "operation": "update",
                    "sessionName": connection.get("sessionName"),
                    "element": json.dumps(data),
                    "elementType": "Accounts",
                }
                res = self.env["vtiger.sync"].callVtigerApi(api_url, "post", data=postData)
                if res.get("status"):
                    success.append(str(company.id))
                    result = res.get("result")
                    log_data.update(
                        remote_id = result.get("id"),
                        local_id = company.id,
                        success = True,
                        error = "Successfully updated"
                    )
                else:
                    failure.append(str(company.id))
                    log_data.update(
                        local_id = company.id,
                        success = False,
                        error = res.get("message")
                    )
                log_line_data.append((0,0,log_data))
            self._vtiger_logout(connection.get("sessionName"))
        return success, failure, log_line_data
