# -*- coding: utf-8 -*-
# from odoo import http


# class SyndicomEvents(http.Controller):
#     @http.route('/syndicom_events/syndicom_events', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/syndicom_events/syndicom_events/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('syndicom_events.listing', {
#             'root': '/syndicom_events/syndicom_events',
#             'objects': http.request.env['syndicom_events.syndicom_events'].search([]),
#         })

#     @http.route('/syndicom_events/syndicom_events/objects/<model("syndicom_events.syndicom_events"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('syndicom_events.object', {
#             'object': obj
#         })
