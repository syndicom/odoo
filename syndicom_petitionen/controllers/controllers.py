# -*- coding: utf-8 -*-
# from odoo import http


# class SyndicomPetitionen(http.Controller):
#     @http.route('/syndicom_petitionen/syndicom_petitionen', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/syndicom_petitionen/syndicom_petitionen/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('syndicom_petitionen.listing', {
#             'root': '/syndicom_petitionen/syndicom_petitionen',
#             'objects': http.request.env['syndicom_petitionen.syndicom_petitionen'].search([]),
#         })

#     @http.route('/syndicom_petitionen/syndicom_petitionen/objects/<model("syndicom_petitionen.syndicom_petitionen"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('syndicom_petitionen.object', {
#             'object': obj
#         })
