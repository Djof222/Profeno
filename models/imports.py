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

class Imports(models.Model):
    _inherit = 'channel.connection'

    def _import_contact(self, **kw):
        remote, feeds = [], []
        isDone = True
        next_page = kw.get("next_page",0)
        offset = 100*next_page
        api_url =f"{self.vt_base_url}/webservice.php"
        connection = self._vtiger_login()
        if connection.get("status"):
            query = """SELECT id, firstname, lastname, account_id, email, mobile, phone, mailingstreet, mailingcity,
                    mailingstate, mailingcountry, mailingzip FROM Contacts """
            if kw.get("vtiger_filter")=="id":
                vtiger_id = kw.get("vtiger_id")
                query+=f"WHERE id={vtiger_id};"
            else:
                query+=f"LIMIT {offset},100;"
            params = {
                "operation": "query",
                "sessionName": connection.get("sessionName"),
                "query": query
            }
            resp = self.env["vtiger.sync"].callVtigerApi(api_url, "get", params=params)
            if resp.get("status"):
                result = resp.get("result")
                for contact in result:
                    state = False
                    country = self.env["res.country"].search([("code","=",contact.get("mailingcountry"))])
                    if country:
                        state = self.env["res.country.state"].search(
                            [("country_id","=",country.id),("name","=",contact.get("mailingstate"))],limit=1).id
                    feedData = {
                        "name": contact.get("firstname")+" "+contact.get("lastname"),
                        "email": contact.get("email"),
                        "mobile": contact.get("mobile"),
                        "phone": contact.get("phone"),
                        "street": contact.get("mailingstreet"),
                        "city": contact.get("mailingcity"),
                        "state_id": state,
                        "country_id": country.id,
                        "zip": contact.get("mailingzip"),
                        "is_company": False,
                        "parent_id": contact.get("account_id")
                    }
                    feeds.append({
                        "connection_id": self.id,
                        "type": "contact",
                        "remote_id": contact.get("id"),
                        "data": json.dumps(feedData)
                    })
                    remote.append(contact.get("id"))
                if len(result)==100:
                    kw["next_page"] = next_page+1
                    isDone = False
            self._vtiger_logout(connection.get("sessionName"))
        kw["done"] = isDone
        return remote, feeds, kw
    
    def _import_company(self, **kw):
        remote, feeds = [], []
        isDone = True
        next_page = kw.get("next_page",0)
        offset = 100*next_page
        api_url =f"{self.vt_base_url}/webservice.php"
        connection = self._vtiger_login()
        if connection.get("status"):
            query = """SELECT id, accountname, email1, phone, website, industry, bill_street, bill_city, bill_state,
                    bill_country, bill_code FROM Accounts """
            if kw.get("vtiger_filter")=="id":
                vtiger_id = kw.get("vtiger_id")
                query+=f"WHERE id={vtiger_id};"
            else:
                query+=f"LIMIT {offset},100;"
            params = {
                "operation": "query",
                "sessionName": connection.get("sessionName"),
                "query": query
            }
            resp = self.env["vtiger.sync"].callVtigerApi(api_url, "get", params=params)
            if resp.get("status"):
                result = resp.get("result")
                for company in result:
                    state = False
                    country = self.env["res.country"].search([("code","=",company.get("bill_country"))],limit=1)
                    if country:
                        state = self.env["res.country.state"].search(
                            [("country_id","=",country.id),("name","=",company.get("bill_state"))],limit=1).id
                    feedData = {
                        "name": company.get("accountname"),
                        "email": company.get("email1"),
                        "phone": company.get("phone"),
                        "website": company.get("website"),
                        "category": company.get("industry"),
                        "is_company": True,
                        "street": company.get("bill_street"),
                        "city": company.get("bill_city"),
                        "zip": company.get("bill_code"),
                        "country_id": country.id,
                        "state_id": state
                    }
                    feeds.append({
                        "connection_id": self.id,
                        "type": "company",
                        "remote_id": company.get("id"),
                        "data": json.dumps(feedData)
                    })
                    remote.append(company.get("id"))
                if len(result)==100:
                    kw["next_page"] = next_page+1
                    isDone = False
            self._vtiger_logout(connection.get("sessionName"))
        kw["done"] = isDone
        return remote, feeds, kw
    
    def _import_deal(self, **kw):
        remote, feeds = [], []
        isDone = True
        next_page = kw.get("next_page",0)
        offset = 100*next_page
        api_url =f"{self.vt_base_url}/webservice.php"
        connection = self._vtiger_login()
        if connection.get("status"):
            query = """SELECT id, potentialname, probability, forcast_amount, closingdate, leadsource, description,
                    lost_reason, pipeline, sales_stage, leadsource, assigned_user_id FROM Potentials """
            if kw.get("vtiger_filter")=="id":
                vtiger_id = kw.get("vtiger_id")
                query+=f"WHERE id={vtiger_id};"
            else:
                query+=f"LIMIT {offset},100;"
            params = {
                "operation": "query",
                "sessionName": connection.get("sessionName"),
                "query": query
            }
            resp = self.env["vtiger.sync"].callVtigerApi(api_url, "get", params=params)
            if resp.get("status"):
                result = resp.get("result")
                for deal in result:
                    lost_reason = self.env["crm.lost.reason"].search([("name","=",deal.get("lost_reason"))])
                    pipeline = self.env["crm.pipeline.mapping"].search(
                        [("connection_id","=",self.id),("remote_id","=",deal.get("pipeline"))])
                    source = self.env["utm.source"].search([("name","=",deal.get("leadsource"))])
                    feedData = {
                        "name": deal.get("potentialname"),
                        "probability": deal.get("probability"),
                        "expected_revenue": deal.get("forcast_amount"),
                        "date_deadline": deal.get("closingdate"),
                        "description": deal.get("description"),
                        "lost_reason": lost_reason.id,
                        "pipeline_id": pipeline.local_id.id,
                        "stage": deal.get("sales_stage"),
                        "source_id": source.id,
                        "user_id": deal.get("assigned_user_id")
                    }
                    feeds.append({
                        "connection_id": self.id,
                        "type": "deal",
                        "remote_id": deal.get("id"),
                        "data": json.dumps(feedData)
                    })
                    remote.append(deal.get("id"))
                if len(result)==100:
                    kw["next_page"] = next_page+1
                    isDone = False
            self._vtiger_logout(connection.get("sessionName"))
        kw["done"] = isDone
        return remote, feeds, kw
    
    def _import_product(self, **kw):
        remote, feeds = [], []
        isDone = True
        next_page = kw.get("next_page",0)
        offset = 100*next_page
        api_url =f"{self.vt_base_url}/webservice.php"
        connection = self._vtiger_login()
        if connection.get("status"):
            query = """SELECT id, productname, productcode, discontinued, productcategory, description, item_barcode,
                    unit_price, purchase_cost, qtyinstock FROM Products """
            if kw.get("vtiger_filter")=="id":
                vtiger_id = kw.get("vtiger_id")
                query+=f"WHERE id={vtiger_id};"
            else:
                query+=f"LIMIT {offset},100;"
            params = {
                "operation": "query",
                "sessionName": connection.get("sessionName"),
                "query": query
            }
            resp = self.env["vtiger.sync"].callVtigerApi(api_url, "get", params=params)
            if resp.get("status"):
                result = resp.get("result")
                for product in result:
                    if product.get("productcategory"):
                        category = self.env["product.category"].search([("name","=",product.get("productcategory"))])
                        if not category:
                            category = self.env["product.category"].create({"name":product.get("productcategory")})
                    else:
                        category = self.default_category_id
                    feedData = {
                        "name": product.get("productname"),
                        "default_code": product.get("productcode"),
                        "sale_ok": product.get("discontinued"),
                        "description": product.get("description"),
                        "barcode": product.get("item_barcode"),
                        "list_price": product.get("unit_price"),
                        "standard_price": product.get("purchase_cost"),
                        "categ_id": category.id,
                    }
                    feeds.append({
                        "connection_id": self.id,
                        "type": "product",
                        "remote_id": product.get("id"),
                        "data": json.dumps(feedData)
                    })
                    remote.append(product.get("id"))
                if len(result)==100:
                    kw["next_page"] = next_page+1
                    isDone = False
            self._vtiger_logout(connection.get("sessionName"))
        kw["done"] = isDone
        return remote, feeds, kw

    def _import_user(self, **kw):
        remote, feeds = [], []
        isDone = True
        next_page = kw.get("next_page",0)
        offset = 100*next_page
        api_url =f"{self.vt_base_url}/webservice.php"
        connection = self._vtiger_login()
        if connection.get("status"):
            query = """SELECT id, user_name, first_name, last_name, email1, phone_work, phone_mobile, is_admin,
                address_street, address_city, address_state, address_country, address_postalcode FROM Users """
            if kw.get("vtiger_filter")=="id":
                vtiger_id = kw.get("vtiger_id")
                query+=f"WHERE id={vtiger_id};"
            else:
                query+=f"LIMIT {offset},100;"
            params = {
                "operation": "query",
                "sessionName": connection.get("sessionName"),
                "query": query
            }
            resp = self.env["vtiger.sync"].callVtigerApi(api_url, "get", params=params)
            if resp.get("status"):
                result = resp.get("result")
                for user in result:
                    country = self.env["res.country"].search([("code","=",user.get("address_country"))])
                    domain = [("country_id","=",country.id),("name","=",user.get("address_state"))]
                    state = self.env["res.country.state"].search(domain, limit=1)
                    feedData = {
                        "name": user.get("first_name")+" "+user.get("last_name"),
                        "login": user.get("user_name"),
                        "email": user.get("email1"),
                        "phone": user.get("phone_work"),
                        "mobile": user.get("phone_mobile"),
                        "street": user.get("address_street"),
                        "city": user.get("address_city"),
                        "state_id": state.id,
                        "country_id": country.id,
                        "zip": user.get("address_postalcode"),
                    }
                    feeds.append({
                        "connection_id": self.id,
                        "type": "user",
                        "remote_id": user.get("id"),
                        "data": json.dumps(feedData)
                    })
                    remote.append(user.get("id"))
                if len(result)==100:
                    kw["next_page"] = next_page+1
                    isDone = False
            self._vtiger_logout(connection.get("sessionName"))
        kw["done"] = isDone
        return remote, feeds, kw
