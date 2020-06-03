# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import date
import datetime
import dateutil.parser

class ReportCompra(models.Model):
	_inherit = "product.template"

	fecha_previs = fields.Datetime(string="Fecha prevista", compute="ComputeReport")
	fecha_pedido_compra = fields.Datetime(string="Fecha compra", compute="ComputeReport")
	dias_retraso = fields.Integer(string="Dias de retraso", compute="DiasRetraso")
	dias_invent = fields.Float(string="Dias inventario", compute="DiasInventario")
	cant_compr_confirm = fields.Integer(string="Cant compras confirmadas", compute="TotalComprasConfirm")

	@api.one
	def ComputeReport(self):			
		product = self.env['product.product'].search([('product_tmpl_id','=',self.id)])
		busquedad = self.env['stock.move'].search([('product_id','=',product.id)], order='id desc', limit=1)
		self.fecha_previs = busquedad.date_expected
		self.fecha_pedido_compra = busquedad.purchase_line_id.order_id.date_order

	@api.one
	def DiasRetraso(self):
		if self.fecha_previs:
			fecha_prevista_str = str(self.fecha_previs)
			fecha_prev = dateutil.parser.parse(fecha_prevista_str).date()
			dia_fecha_previ = fecha_prev.strftime('%d')
			mes_fecha_previ = fecha_prev.strftime('%m')
			ano_fecha_previ = fecha_prev.strftime('%Y')
			fecha_retrazo = date(int(ano_fecha_previ),int(mes_fecha_previ),int(dia_fecha_previ))

			dia_actual = datetime.datetime.now().strftime('%d')
			mes_actual = datetime.datetime.now().strftime('%m')
			ano_actual = datetime.datetime.now().strftime('%Y')
			fecha_actual = date(int(ano_actual),int(mes_actual),int(dia_actual))
			dias = abs(fecha_actual - fecha_retrazo).days
			self.dias_retraso = dias
			# print ("%s dias de diferencia entre %s y el %s" % (dias, fecha_retrazo, fecha_actual))
			# print ("%s años de diferencia entre %s y el %s" % (int(dias/365), fecha_retrazo, fecha_actual))

	@api.one
	def DiasInventario(self):
		if self.dias_retraso > 0:
			self.dias_invent = self.qty_available / self.dias_retraso

	@api.one
	def TotalComprasConfirm(self):
		product = self.env['product.product'].search([('product_tmpl_id','=',self.id)])
		stock_move = self.env['stock.move'].search([('product_id','=',product.id), ('picking_id.state','in',('confirmed','assigned')), ('picking_id.picking_type_code','=',"incoming")], order='id desc')

		for x in stock_move:
			self.cant_compr_confirm += x.purchase_line_id.product_qty

class InheritPayment(models.Model):
	_inherit = 'account.payment'

	retenido = fields.Boolean(string='¿Esta retenido?')
