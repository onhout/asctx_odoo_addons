# -*- coding: utf-8 -*-
from odoo import http

# class AscRdtd(http.Controller):
#     @http.route('/asc_rdtd/asc_rdtd/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asc_rdtd/asc_rdtd/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asc_rdtd.listing', {
#             'root': '/asc_rdtd/asc_rdtd',
#             'objects': http.request.env['asc_rdtd.asc_rdtd'].search([]),
#         })

#     @http.route('/asc_rdtd/asc_rdtd/objects/<model("asc_rdtd.asc_rdtd"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asc_rdtd.object', {
#             'object': obj
#         })