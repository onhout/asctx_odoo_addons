# -*- coding: utf-8 -*-
from odoo import http

# class AscTherapeuticsCustomize(http.Controller):
#     @http.route('/asc_therapeutics_customize/asc_therapeutics_customize/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asc_therapeutics_customize/asc_therapeutics_customize/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asc_therapeutics_customize.listing', {
#             'root': '/asc_therapeutics_customize/asc_therapeutics_customize',
#             'objects': http.request.env['asc_therapeutics_customize.asc_therapeutics_customize'].search([]),
#         })

#     @http.route('/asc_therapeutics_customize/asc_therapeutics_customize/objects/<model("asc_therapeutics_customize.asc_therapeutics_customize"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asc_therapeutics_customize.object', {
#             'object': obj
#         })