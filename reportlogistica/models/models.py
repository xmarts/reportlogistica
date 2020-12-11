# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import date
import datetime
import dateutil.parser

class ReportCompra(models.Model):
	_inherit = "product.template"

	fecha_previs = fields.Datetime(string="Fecha prevista", store=True, compute="ComputeReport")
	fecha_pedido_compra = fields.Datetime(string="Fecha compra", store=True, compute="ComputeReport")
	dias_retraso = fields.Integer(string="Dias de retraso", store=True, compute="DiasRetraso")
	dias_invent = fields.Float(string="Dias inventario", store=True, compute="DiasInventario")
	cant_compr_confirm = fields.Integer(string="Cant compras confirmadas", store=True, compute="TotalComprasConfirm")
	# pedido_compra = fields.Date()
	@api.one
	def ComputeReport(self):
		product = self.env['product.product'].search([('product_tmpl_id','=',self.id)])
		busquedad = self.env['stock.move'].search([('product_id','=',product.id), ('state', '!=', 'cancel')], order='id desc', limit=1)
		self.fecha_previs = busquedad.date_expected
		busquedad = self.env['stock.move'].search([('product_id','=',product.id)], order='id desc', limit=1)
		self.fecha_previs = busquedad.date
		self.fecha_pedido_compra = busquedad.purchase_line_id.order_id.date_order
		print('jjjjjjjjjjjjjjjjjjjjjjjjj', self.fecha_pedido_compra)

	@api.one
	def DiasRetraso(self):
		if self.fecha_previs:
			fecha_prevista_str = str(self.fecha_previs)
			fecha_prev = dateutil.parser.parse(fecha_prevista_str).date()
			dia_fecha_previ = fecha_prev.strftime('%d')
			mes_fecha_previ = fecha_prev.strftime('%m')
			ano_fecha_previ = fecha_prev.strftime('%Y')
			fecha_retrazo = date(int(ano_fecha_previ),int(mes_fecha_previ),int(dia_fecha_previ))

			# f_com_str = str(self.fecha_pedido_compra)
			# fecha_c = dateutil.parser.parse(f_com_str).date()
			# fecha_c_mes = fecha_c.strftime('%d')
			# fecha_c_anio = fecha_c.strftime('%m')
			# fecha_c_dia = fecha_c.strftime('%Y')
			# compra_fech = date(int(fecha_c_dia),int(fecha_c_mes),int(fecha_c_anio))

			# self.pedido_compra = compra_fech

			dia_actual = datetime.datetime.now().strftime('%d')
			mes_actual = datetime.datetime.now().strftime('%m')
			ano_actual = datetime.datetime.now().strftime('%Y')
			fecha_actual = date(int(ano_actual),int(mes_actual),int(dia_actual))
			dias = abs(fecha_actual - fecha_retrazo).days
			self.dias_retraso = dias
			# print ("%s dias de diferencia entre %s y el %s" % (dias, fecha_retrazo, fecha_actual))
			# print ("%s años de diferencia entre %s y el %s" % (int(dias/365), fecha_retrazo, fecha_actual))
	def user_log(self):
		login  = self.env['res.users'].search([('id','=',self.env.user.id)])
		for rec in login:
			usuario = rec.name
		return usuario

	@api.one
	def DiasInventario(self):
		if self.dias_retraso > 0:
			self.dias_invent = self.qty_available / self.dias_retraso

	@api.one
	def TotalComprasConfirm(self):
		self.cant_compr_confirm = 0
		for rec in self:
			print('EEEEEEO')
			product = self.env['product.product'].search([('product_tmpl_id','=',rec.id)])
			print(product.name)
			# stock_move = self.env['stock.move'].search([('product_id','=',product.id), ('picking_id.state','in',('confirmed','assigned')), ('picking_id.picking_type_code','=',"incoming")], order='id desc')
			purchase_order = self.env['purchase.order'].search([('product_id','=',product.id), ('state','=','purchase')], order='id desc')

			for x in purchase_order:
				for z in x.order_line:
					print("EEEEEEEEEEOOOOOOOOOOOOO")
					if z.product_id.id == product.id:
						print('OHHHHH RIGHT',z.product_qty)
						rec.cant_compr_confirm += (z.product_qty - z.qty_received)

class InheritPayment(models.Model):
	_inherit = 'account.payment'

	retenido = fields.Boolean(string='¿Esta retenido?')

	def user_log(self):
		login  = self.env['res.users'].search([('id','=',self.env.user.id)])
		for rec in login:
			usuario = rec.name
		return usuario