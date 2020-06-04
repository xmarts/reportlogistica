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
			d1 = dato.date_from
			d2 = dato.date_to
			if d1 != 'False' and d1 != 'False' and dato.cuenta:
				file = {
				'fecha1':d1,
				'fecha2':d2,
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