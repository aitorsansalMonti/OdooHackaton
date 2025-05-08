from odoo import models, fields, api

class PromocionsIOfertes(models.Model):
    _name = 'promocions.i.ofertes'
    _description = 'Promocions i Ofertes Especials'

    name = fields.Char('Nom de la Promoció', required=True)
    description = fields.Text('Descripció de la Promoció')
    product_id = fields.Many2one('product.product', string='Producte', required=True)
    start_date = fields.Date('Data d\'Inici', required=True)
    end_date = fields.Date('Data de Fi', required=True)
    discount = fields.Float('Descompte (%)', required=True)
    state = fields.Selection([
        ('draft', 'Esborrany'),
        ('active', 'Activa'),
        ('expired', 'Expirada')
    ], string='Estat', required=True)

    @api.onchange('end_date')
    def _check_expiration(self):
        if self.end_date and self.end_date < fields.Date.today():
            self.state = 'expired'
