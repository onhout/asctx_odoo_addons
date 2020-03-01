# -*- coding: utf-8 -*-
from odoo import http

# class TawktoChat(http.Controller):
#     @http.route('/tawkto_chat/tawkto_chat/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tawkto_chat/tawkto_chat/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tawkto_chat.listing', {
#             'root': '/tawkto_chat/tawkto_chat',
#             'objects': http.request.env['tawkto_chat.tawkto_chat'].search([]),
#         })

#     @http.route('/tawkto_chat/tawkto_chat/objects/<model("tawkto_chat.tawkto_chat"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tawkto_chat.object', {
#             'object': obj
#         })