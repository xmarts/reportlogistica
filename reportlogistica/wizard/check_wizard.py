from odoo import models, fields, api

class ReportWizard(models.TransientModel):
	_name = 'report.check.wizard'

	filter_date = fields.Selection([
		('all','Mostrar todo los registros'),
		('dates','Filtrar por Fecha'),
		('diario','Filtrar por Diario'),
		('fe_di','Filtrar por Fecha y Diario')], string="Filtro")
	cuenta = fields.Many2one('account.journal',string="Diario", domain=[('type','in',('bank','cash'))])
	date_from = fields.Date(string='De')
	date_to = fields.Date(string='Hasta')

	def filter(self):
		self.ensure_one()
		tree_view_id = self.env.ref('reportlogistica.view_informe_cheques').id
		
		if self.filter_date == 'all':
			action = {
				'type': 'ir.actions.act_window',
				'views': [(tree_view_id, 'tree')],
				'view_mode': 'form,tree',
				'name':'Reporte de cheques',
				'res_model': 'account.payment',
				'domain' : [('payment_method_id','=',4)],
				#'context':{'dato': 'all'},
			}
			return action
		if self.filter_date == 'dates':
			action = {
				'type': 'ir.actions.act_window',
				'views': [(tree_view_id, 'tree')],
				'view_mode': 'form,tree',
				'name':'Reporte de cheques',
				'res_model': 'account.payment',
				'domain': [('payment_date','>=',self.date_from),
				('payment_date','<=',self.date_to),
				('payment_method_id','=',4)],
			}
			return action
		if self.filter_date == 'diario':
			action = {
				'type': 'ir.actions.act_window',
				'views': [(tree_view_id, 'tree')],
				'view_mode': 'form,tree',
				'name':'Reporte de cheques',
				'res_model': 'account.payment',
				'domain': [('payment_method_id','=',4),('journal_id','=',self.cuenta.id)],
			}
			print('DIARIOOOOOOOOO',self.cuenta)
			return action
		if self.filter_date == 'fe_di':
			action = {
				'type': 'ir.actions.act_window',
				'views': [(tree_view_id, 'tree')],
				'view_mode': 'form,tree',
				'name':'Reporte de cheques',
				'res_model': 'account.payment',
				'domain': [('payment_date','>=',self.date_from),
				('payment_date','<=',self.date_to),
				('payment_method_id','=',4),
				('journal_id','=',self.cuenta.id)],
			}

class inherit_account_pay(models.Model):
	_inherit = 'account.payment'

	#solo fechas
	def fechas(self):
		lista = []
		cr = self.env.cr
		cr.execute('select max(id) from report_check_wizard')
		id_returned = cr.fetchone()
		dato = self.env['report.check.wizard'].search([('id','=',id_returned)])
		for rec in dato:
			if dato.date_from != 'False' and dato.date_to != 'False':
				file = {
				'fecha1':str(dato.date_from),
				'fecha2':str(dato.date_to)
				}
				lista.append(file)
		return lista
	#diarios
	def diarios(self):
		lista = []
		cr = self.env.cr
		cr.execute('select max(id) from report_check_wizard')
		id_returned = cr.fetchone()
		dato = self.env['report.check.wizard'].search([('id','=',id_returned)])
		for rec in dato:
			if dato.cuenta:
				file = {
				'diario':dato.cuenta.name
				}
				lista.append(file)
		return lista


class WizzardMateroaPrima(models.Model):
	_name = 'wizard.materia.prima'

	rango = fields.Selection([
		('all', 'Mostrar todos los registros'),
		('pur', 'Puede ser Comprado')], default="all", string="Filtrar")
	date_from = fields.Datetime(string='De')
	date_to = fields.Datetime(string='Hasta')
	dias = fields.Integer(string="Dias", required=True,)



	def filter(self):
		self.ensure_one()
		tree_view_id = self.env.ref('reportlogistica.view_informe_compra').id

		if self.rango == 'all':
			total_com = self.env['product.template'].search([('id','!=', 0)])
			for rec in total_com:
				rec.TotalComprasConfirm()
				rec.ComputeReport()
				rec.DiasRetraso()
				rec.DiasInventario(self.dias)
			action = {
				'type': 'ir.actions.act_window',
				'views': [(tree_view_id, 'tree')],
				'view_mode': 'form,tree',
				'name': 'Materia Prima',
				'res_model': 'product.template',
				#'context':{'dato': 'all'},
			}
			return action
		if self.rango == 'pur':
			total_com = self.env['product.template'].search([('purchase_ok','=', True)])
			for rec in total_com:
				rec.TotalComprasConfirm()
				rec.ComputeReport()
				rec.DiasRetraso()
				rec.DiasInventario(self.dias)

			action = {
				'type': 'ir.actions.act_window',
				'views': [(tree_view_id, 'tree')],
				'view_mode': 'form,tree',
				'name': 'Materia Prima',
				'res_model': 'product.template',
			}
			return action


class InheritProductTemplate(models.Model):
	_inherit = 'product.template'

	def fechas(self):
		lista = []
		cr = self.env.cr
		cr.execute('select max(id) from wizard_materia_prima')
		id_returned = cr.fetchone()
		dato = self.env['wizard.materia.prima'].search([('id', '=', id_returned)])
		for rec in dato:
			print('forrrrrrrrrrrrr')
			if dato.date_from != 'False' and dato.date_to != 'False':
				file = {
					'fecha1': dato.date_from,
					'fecha2': dato.date_to
				}
				lista.append(file)
		return lista
