import string
from odoo import models, fields, api

class QualityAlert(models.Model):
    _inherit = 'quality.alert'

    saleorder_id = fields.Many2one('sale.order', string='Orden de Venta', 
    domain=['&', ('state', '!=', 'draft'), ('state', '!=', 'cancel')])
    account_move_id = fields.Many2one('account.move', string='Factura de Venta')
    purchorder_id = fields.Many2one('purchase.order', string='Orden de Compra', 
    domain=['&', ('state', '!=', 'draft'), ('state', '!=', 'cancel')])
    account_purchase_id = fields.Many2one('account.move', string='Factura de Compra')

    def read(self, fields=None, load='_classic_read'):
        for record in self:
            print('Purchase#########',record.purchorder_id)
            print('Sales#########',record.account_move_id)
        res = super(QualityAlert,self).read(fields, load)
        return res
    
    @api.onchange('saleorder_id')
    def get_sales(self):
        if self.saleorder_id.name != False:
            self.ensure_one()
            res = {}
            print(self.saleorder_id.name)
            invoices_all = self.env['account.move']
            invoices = invoices_all.search([('invoice_origin', 'ilike', self.saleorder_id.name)])
            print(invoices)
            invoices_ids = []
            for invoice in invoices:
                invoices_ids.append(invoice.id)
            res['domain'] = {'account_move_id': [('id', '=', invoices_ids)]}
            return res

    @api.onchange('purchorder_id')
    def get_purchase(self):
        if self.purchorder_id.name != False:
            self.ensure_one()
            res = {}
            print(self.purchorder_id.name)
            invoices_all = self.env['account.move']
            invoices = invoices_all.search([('invoice_origin', 'ilike', self.purchorder_id.name)])
            print(invoices)
            invoices_ids = []
            for invoice in invoices:
                invoices_ids.append(invoice.id)
            res['domain'] = {'account_purchase_id': [('id', '=', invoices_ids)]}
            return res