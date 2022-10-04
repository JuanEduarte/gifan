import base64
import os
import csv
import tempfile
from odoo.exceptions import UserError
from odoo import api, fields, models, _
from datetime import datetime, timedelta, date


class GifImportMasivePayment(models.Model):
    _name = "import.payment.order"
    _description ='Creacion depagos masivos'

    file_data = fields.Binary('Archivo', required=True,)
    file_name = fields.Char('nombre del archivo')
    nombre = fields.Char(string='nombre')
    gif_masive_payment_line = fields.One2many(comodel_name='gif.masive.payment.line', inverse_name='gif_masive_payment', string='a')    
    gif_journal             = fields.Many2one(comodel_name='account.journal', string='Diario')
    payment_method          = fields.Many2one(comodel_name='l10n_mx_edi.payment.method', string='Metodo de pago')
    partner_account = fields.Char(string='Cuenta bancaria de la empresa', compute='files_data')

    def files_data(self):
            file_path = tempfile.gettempdir()+'/file.csv'
            data = self.file_data
            f = open(file_path,'wb')
            f.write(base64.b64decode(data))
            f.close() 
            archive = csv.DictReader(open(file_path))

            limit = 0
            customer = []
            for l in archive:
                customer.append(l)
                p=customer[0]['Cliente']
                res=self.env['res.partner'].search([('name', '=', p)])
                if self.gif_journal:
                    print( res.bank_ids.display_name)
                print( res.name)
                print( res.bank_ids.display_name)
                print( res.bank_ids.journal_id)
                limit += 1
                if limit > 0:
                    break 


            archive_lines = []
            for line in archive:
                archive_lines.append(line)
                #print(archive_lines[0]['Cliente'])
            for line in archive_lines:
                    #print(line['Cliente'], line['Factura de venta'], line['Importe'])
                    cliente = line['Cliente']
                    for record in self:
                        if cliente:
                                rel = self.env['gif.masive.payment.line'].create([{
                                    'gif_masive_payment':record.id,
                                    'client'            :line['Cliente'],
                                    'invoice_id'        :line['Factura de venta'],
                                    'amount'            :line['Importe'],
                                    'partner'           :res.bank_ids.display_name,
                                }])
                        else:
                            pass


    @api.model
    def csv_validator(self, xml_name):
        extension = os.path.splitext(xml_name)
        return True if extension == '.csv' else False


class GifMasivePaymentLine(models.Model):
  _name = 'gif.masive.payment.line'
  _description = 'Linea de pago masivo'

  client               = fields.Char    (string='Cliente')
  invoice_id           = fields.Char    (string='Factura')
  amount               = fields.Char    (string='Importe')
  partner              = fields.Char    (string='Partner')


  gif_masive_payment    = fields.Many2one(comodel_name='import.payment.order')


