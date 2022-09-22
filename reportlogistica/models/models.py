# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import timedelta, date
import datetime
import dateutil.parser

class ReportCompra(models.Model):
    _inherit = "product.template"
    
    fecha_previs = fields.Datetime(string="Fecha prevista", store=True, compute="ComputeReport")
    fecha_pedido_compra = fields.Datetime(string="Fecha compra", store=True, compute="ComputeReport")
    dias_retraso = fields.Integer(string="Dias de retraso", store=True, compute="DiasRetraso")
    dias_invent = fields.Float(string="Dias inventario", store=True, compute="DiasInventarios")
    cant_compr_confirm = fields.Integer(string="Cant compras confirmadas", store=True, compute="TotalComprasConfirm")
    disponible_qty = fields.Float(string="Cantidad Disponible")
    # pedido_compra = fields.Date()
    
    #@api.multi
    def TotalComprasConfirm(self):
        for rec in self:
            rec.cant_compr_confirm = 0
            rec.disponible_qty = 0 
            rec.fecha_previs =''
            rec.fecha_pedido_compra =''
            product = self.env['product.product'].search([('product_tmpl_id','=',rec.id)])
            purchase_order = self.env['purchase.order'].search([('product_id','=',product.id), ('state','=','purchase')], order='id desc')
            for x in purchase_order:
                for z in x.order_line:
                    if z.product_id.id == product.id:
                        rec.cant_compr_confirm += (z.product_qty - z.qty_received)
                        if z.qty_received == 0:
                            rec.fecha_previs = ''
                            rec.fecha_pedido_compra = ''
                            rec.fecha_pedido_compra = x.date_order
                            rec.fecha_previs = z.date_planned
            rec.disponible_qty = rec.qty_available + rec.cant_compr_confirm
    
    #@api.one
    def ComputeReport(self):
        for rec in self:
            product = self.env['product.product'].search([('product_tmpl_id','=',rec.id)])
            busquedad = self.env['purchase.order.line'].search([('product_id','=',product.id)], order='id desc')
            reci = 0
            for rec in busquedad:
                reci += rec.qty_received

                # if rec.qty_received == 0:
                #     rec.fecha_previs = rec.date_planned
                # else:
                #     rec.fecha_previs = ''

    #@api.one
    def DiasRetraso(self):
        for rec in self:
            rec.dias_retraso = 0
            if rec.fecha_previs:
                fecha_prevista_str = str(rec.fecha_previs)
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
                rec.dias_retraso = ''
                if rec.cant_compr_confirm > 0:
                    rec.dias_retraso = dias
                # print ("%s dias de diferencia entre %s y el %s" % (dias, fecha_retrazo, fecha_actual))
                # print ("%s años de diferencia entre %s y el %s" % (int(dias/365), fecha_retrazo, fecha_actual))
    def user_log(self):
        login  = self.env['res.users'].search([('id','=',self.env.user.id)])
        for rec in login:
            usuario = rec.name
        return usuario

    #@api.multi

    def DiasInventarios(self):
        for rec in self:
            rec.dias_invent = 0
            fecha_anterior = ""
            fecha_actual = ""
            dias = 0
            if dias:
                dia_actual = datetime.datetime.now().strftime('%d')
                mes_actual = datetime.datetime.now().strftime('%m')
                ano_actual = datetime.datetime.now().strftime('%Y')
                fecha_actual = date(int(ano_actual),int(mes_actual),int(dia_actual))
                fecha_anterior = date(int(ano_actual),int(mes_actual),int(dia_actual)) + timedelta(days=-dias)
            if dias:
                print(dias)
                if dias > 0:
                    product = self.env['product.product'].search([('product_tmpl_id','=',rec.id)])
                    move_line = self.env['stock.move.line'].search([('product_id','=', product.id)])
                    consumo_diario_total = 0
                    for rec in move_line:
                        rec.dias_invent = 0
                        if rec.date.date() <= fecha_actual and rec.date.date() >= fecha_anterior:
                            # print(fecha_anterior, '------------' ,rec.date.date(),  '-------------', fecha_actual)
                            if rec.location_dest_id.check_location == True:
                                print(rec.qty_done)
                                consumo_diario_total += rec.qty_done
                    # print('aaaaaaaaaaaaaaaaaaa', consumo_diario_total, product.name)
                    consumo_diario = consumo_diario_total / dias
                    rec.dias_invent = 0
                    if consumo_diario > 0 and rec.qty_available > 0: 
                        rec.dias_invent =  rec.qty_available / consumo_diario

    def DiasInventario(self, dias):
        for rec in self:
            rec.dias_invent = 0
            fecha_anterior = ""
            fecha_actual = ""
            if dias:
                dia_actual = datetime.datetime.now().strftime('%d')
                mes_actual = datetime.datetime.now().strftime('%m')
                ano_actual = datetime.datetime.now().strftime('%Y')
                fecha_actual = date(int(ano_actual),int(mes_actual),int(dia_actual))
                fecha_anterior = date(int(ano_actual),int(mes_actual),int(dia_actual)) + timedelta(days=-dias)
            if dias:
                print(dias)
                if dias > 0:
                    product = self.env['product.product'].search([('product_tmpl_id','=',rec.id)])
                    move_line = self.env['stock.move.line'].search([('product_id','=', product.id)])
                    consumo_diario_total = 0
                    for rec in move_line:
                        rec.dias_invent = 0
                        if rec.date.date() <= fecha_actual and rec.date.date() >= fecha_anterior:
                            # print(fecha_anterior, '------------' ,rec.date.date(),  '-------------', fecha_actual)
                            if rec.location_dest_id.check_location == True:
                                print(rec.qty_done)
                                consumo_diario_total += rec.qty_done
                    # print('aaaaaaaaaaaaaaaaaaa', consumo_diario_total, product.name)
                    consumo_diario = consumo_diario_total / dias
                    rec.dias_invent = 0
                    if consumo_diario > 0 and rec.qty_available > 0: 
                        rec.dias_invent =  rec.qty_available / consumo_diario


class InheritPayment(models.Model):
    _inherit = 'account.payment'

    retenido = fields.Boolean(string='¿Esta retenido?')

    def user_log(self):
        login  = self.env['res.users'].search([('id','=',self.env.user.id)])
        for rec in login:
            usuario = rec.name
        return usuario


class StockLocation(models.Model):
    _inherit = 'stock.location'

    check_location = fields.Boolean(string="Virtual Locations", default=False)