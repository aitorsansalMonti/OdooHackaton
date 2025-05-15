from odoo import models, fields, api

class gestor_projectes(models.Model):
    _name = 'gestor.projectes'
    _description = 'Gestor de Projectes'

    tipus = fields.Selection([])
    description = fields.Text('Descripció de la Promoció')
    creation_date = fields.Date('Data de creació')
    start_date = fields.Date('Data d\'Inici')
    end_date = fields.Date('Data de Fi')
    state = fields.Selection([
        ('notStarted', 'No Iniciat'),
        ('inProgress', 'En Progrés'),
        ('completed', 'Completat')
    ], string='Estat', required=True)
    observations = fields.Text('Observacions')
    worksDone = fields.Text('Obres Realitzades')
    hoursWorked = fields.Float('Hores Treballades')

    @api.model
    def create(self, vals):
        if 'creation_date' not in vals or not vals['creation_date']:
            vals['creation_date'] = fields.Date.today()
        # Set default state if not provided
        if 'state' not in vals:
            vals['state'] = 'notStarted'

        # Call the super method to create the record
        record = super(gestor_projectes, self).create(vals)

        return record
    
    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'completed':
            self.end_date = fields.Date.today()
        elif self.state == 'inProgress':
            self.start_date = fields.Date.today()

