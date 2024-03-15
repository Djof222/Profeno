# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
import calendar
from datetime import date

from odoo import fields, http
from odoo.http import request


INDEX_COLORS = [
    '#9365b8', '#35979c', '#f4a460',
    '#f7cd1f', '#6cc1ed', '#814968',
    '#eb7e7f', '#2c8397', '#475577',
    '#d6145f', '#30c381', '#9365b8',
]

class WebsiteBackend(http.Controller):
    @http.route('/multichannel_crm/fetch_connection_data',type='json',auth='user')
    def fetch_connections_data(self):
        request._cr.execute('''
            SELECT count(id) as count, connection_id
                FROM crm_lead_mapping
            GROUP BY connection_id
        ''')
        lead_count = {d['connection_id']: d['count'] for d in request._cr.dictfetchall()}

        request._cr.execute('''
            SELECT count(local_id) as count, connection_id
                FROM res_partner_mapping
            INNER JOIN res_partner
                ON local_id=res_partner.id
            WHERE is_company=True
            GROUP BY connection_id
        ''')
        company_count = {d['connection_id']: d['count'] for d in request._cr.dictfetchall()}

        request._cr.execute('''
            SELECT count(local_id) as count, connection_id
                FROM res_partner_mapping
            INNER JOIN res_partner
                ON local_id=res_partner.id
            WHERE is_company=False
            GROUP BY connection_id
        ''')
        contact_count = {d['connection_id']: d['count'] for d in request._cr.dictfetchall()}

        request._cr.execute('''
            SELECT count(id) as count, connection_id
                FROM res_users_mapping
            GROUP BY connection_id
        ''')
        user_count = {d['connection_id']: d['count'] for d in request._cr.dictfetchall()}

        connections = []
        for connection in request.env['channel.connection'].search([]):
            connection_id = connection.id
            image = connection.image
            if image:
                image = f"data:image/jpeg;charset=utf-8;base64,{image.decode('utf-8')}"
            else:
                image=''

            connections.append({
                'id'           : connection_id,
                'name'         : connection.name,
                'channel'      : connection.channel,
                'image'        : image,
                'color'        : connection.color,
                'blog'         : connection.blog_url,
                'lead_count'   : lead_count.get(connection_id,0),
                'company_count': company_count.get(connection_id,0),
                'contact_count': contact_count.get(connection_id,0),
                'user_count'   : user_count.get(connection_id,0),
            })
        return connections

    @http.route('/multichannel_crm/fetch_recent_lead_data',type='json',auth='user')
    def fetch_recent_lead_data(self, period='monthly'):
        if period=='monthly':
            request._cr.execute(f'''
                SELECT to_char(crm_lead.create_date,'mm') as m, count(local_id) as count
                    FROM crm_lead_mapping
                LEFT JOIN crm_lead
                    ON crm_lead_mapping.local_id = crm_lead.id
                WHERE crm_lead.create_date > date_trunc('month', CURRENT_DATE) - INTERVAL '1 year'
                GROUP BY 1
            ''')
            data = {int(r['m']): r['count'] for r in request._cr.dictfetchall()}

            current_month = date.today().month
            months = [1,2,3,4,5,6,7,8,9,10,11,12]
            months = months[current_month:]+months[:current_month]
            recent_data = [
                {
                    'label': calendar.month_name[i],
                    'count': data.get(i, 0)
                } for i in months
            ]
        elif period=='daily':
            request._cr.execute(f'''
                SELECT to_char(crm_lead.create_date,'D') as d, count(local_id) as count
                    FROM crm_lead_mapping
                LEFT JOIN crm_lead
                    ON crm_lead_mapping.local_id = crm_lead.id
                WHERE crm_lead.create_date > date_trunc('day', CURRENT_DATE) - INTERVAL '1 week'
                GROUP BY 1
            ''')
            data = {int(r['d']): r['count'] for r in request._cr.dictfetchall()}

            weekday = date.today().weekday()+1
            days = [0,1,2,3,4,5,6]
            days = days[weekday:]+days[:weekday]
            recent_data = [
                {
                    'label': calendar.day_name[i],
                    'count': data.get(i, 0)
                } for i in days
            ]
        return recent_data

    @http.route('/multichannel_crm/fetch_total_lead_data',type='json',auth='user')
    def fetch_total_lead_data(self):
        request._cr.execute(f'''
            SELECT crm_stage.name, crm_stage.color, count(crm_lead.id)
                FROM crm_lead
            INNER JOIN crm_lead_mapping
                ON crm_lead.id=local_id
            INNER JOIN crm_stage
                ON crm_lead.stage_id=crm_stage.id
            GROUP BY 1,2
        ''')
        data = request._cr.dictfetchall()
        for d ,c in zip(data,INDEX_COLORS):
            d['color'] = c
        return data

    @http.route('/multichannel_crm/fetch_connection_data/<int:connection_id>',type='json',auth='user')
    def fetch_connection_data(self, connection_id):
        connection = request.env['channel.connection'].browse(connection_id)
        image = connection.image
        if image:
            image = f"data:image/jpeg;charset=utf-8;base64,{image.decode('utf-8')}"
        else:
            image = ''
        return {
            'id'       : connection_id,
            'name'     : connection.name,
            'blog'     : connection.blog_url,
            'channel'  : connection.channel,
            'connected': connection.connected,
            'image'    : image,
        }

    @http.route('/multichannel_crm/fetch_recent_lead_data/<int:connection_id>',type='json',auth='user')
    def fetch_connection_recent_lead_data(self, connection_id, period='monthly'):
        request._cr.execute(f'SELECT color FROM channel_connection WHERE id={connection_id}')
        color = request._cr.fetchall()[0][0]
        if period=='monthly':
            request._cr.execute(f'''
                SELECT to_char(crm_lead.create_date,'mm') as m, count(local_id) as count
                    FROM crm_lead_mapping
                LEFT JOIN crm_lead
                    ON crm_lead_mapping.local_id = crm_lead.id
                WHERE connection_id={connection_id}
                    AND crm_lead.create_date > date_trunc('month', CURRENT_DATE) - INTERVAL '1 year'
                GROUP BY 1
            ''')
            data = {int(r['m']): r['count'] for r in request._cr.dictfetchall()}

            current_month = date.today().month
            months = [1,2,3,4,5,6,7,8,9,10,11,12]
            months = months[current_month:]+months[:current_month]
            recent_data=[
                {
                    'label': calendar.month_name[i],
                    'count': data.get(i, 0)
                } for i in months
            ]
        elif period=='daily':
            request._cr.execute(f'''
                SELECT to_char(crm_lead.create_date,'D') as d, count(local_id) as count
                    FROM crm_lead_mapping
                LEFT JOIN crm_lead
                    ON crm_lead_mapping.local_id = crm_lead.id
                WHERE connection_id={connection_id}
                    AND crm_lead.create_date > date_trunc('day', CURRENT_DATE) - INTERVAL '1 week'
                GROUP BY 1
            ''')
            data = {int(r['d']): r['count'] for r in request._cr.dictfetchall()}

            weekday = date.today().weekday()+1
            days = [0,1,2,3,4,5,6]
            days = days[weekday:]+days[:weekday]
            recent_data = [
                {
                    'label': calendar.day_name[i],
                    'count': data.get(i, 0)
                } for i in days
            ]
        return {'data': recent_data, 'color': color}

    @http.route('/multichannel_crm/fetch_total_lead_data/<int:connection_id>',type='json',auth='user')
    def fetch_connection_total_lead_data(self, connection_id):
        request._cr.execute(f'''
            SELECT crm_stage.name, crm_stage.color, count(crm_lead.id)
                FROM crm_lead
            INNER JOIN crm_lead_mapping
                ON crm_lead.id=local_id
            INNER JOIN crm_stage
                ON crm_lead.stage_id=crm_stage.id
            WHERE connection_id={connection_id}
            GROUP BY 1,2
        ''')
        data = request._cr.dictfetchall()
        for d in data:
            d['color'] = INDEX_COLORS[d['color']]
        return data

    @http.route('/multichannel_crm/fetch_top_user_data/<int:connection_id>',type='json',auth='user')
    def fetch_connection_top_user_data(self, connection_id):
        request._cr.execute('''
            SELECT id, name, color
                FROM crm_stage
            ORDER BY 1
        ''')
        stages = request._cr.dictfetchall()
        colors = {stage['name']['en_US']:INDEX_COLORS[stage['color']] for stage in stages}

        request._cr.execute(f'''
            SELECT res_users.id as uid, res_partner.name as user, count(crm_lead.id)
                FROM crm_lead
            INNER JOIN crm_lead_mapping
                ON crm_lead.id=local_id
            INNER JOIN res_users
                ON crm_lead.user_id=res_users.id
            INNER JOIN res_partner
                On res_users.partner_id=res_partner.id
            WHERE crm_lead_mapping.connection_id={connection_id}
            GROUP BY 1,2
            ORDER BY count DESC
            LIMIT 10
        ''')
        users = []
        user_ids = []
        user_list = request._cr.dictfetchall()
        for user in user_list:
            uid = user['uid']
            users.append({'id': uid, 'name': user['user']})
            user_ids.append(str(uid))
        data = {stage['name']['en_US']:{int(uid):0 for uid in user_ids} for stage in stages}

        if users:
            request._cr.execute(f'''
                SELECT res_users.id as uid, crm_stage.name as stage, count(crm_lead.id)
                    FROM crm_lead
                INNER JOIN crm_lead_mapping
                    ON crm_lead.id=local_id
                INNER JOIN crm_stage
                    ON crm_lead.stage_id=crm_stage.id
                INNER JOIN res_users
                    ON crm_lead.user_id=res_users.id
                INNER JOIN res_partner
                    On res_users.partner_id=res_partner.id
                WHERE crm_lead_mapping.connection_id={connection_id}
                    AND res_users.id IN ({','.join(user_ids)})
                GROUP BY 1,2
            ''')
            for d in request._cr.dictfetchall():
                data[d['stage']['en_US']][d['uid']] = d['count']
        return {
            'users': users,
            'data': data,
            'colors': colors,
        }
