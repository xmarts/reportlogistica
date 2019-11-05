# -*- coding: utf-8 -*-
from odoo import http

# class Reporte(http.Controller):
#     @http.route('/reporte/reporte/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/reporte/reporte/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('reporte.listing', {
#             'root': '/reporte/reporte',
#             'objects': http.request.env['reporte.reporte'].search([]),
#         })

#     @http.route('/reporte/reporte/objects/<model("reporte.reporte"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('reporte.object', {
#             'object': obj
#         })