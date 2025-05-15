from odoo import models, fields, api  # type: ignore

class GestorDeProjectes(models.Model):
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

    @api.onchange('end_date')
    def _check_expiration(self):
        if self.end_date and self.end_date < fields.Date.today():
            self.state = 'expired'

    @api.model
    def create(self, vals):

        if 'creation_date' not in vals or not vals['creation_date']:
            vals['creation_date'] = fields.Date.today()
        # Set default state if not provided
        if 'state' not in vals:
            vals['state'] = 'notStarted'

        # Call the super method to create the record
        record = super(GestorDeProjectes, self).create(vals)

        # Custom logic after record creation (if needed)
        # Example: Log a message
        self.env['ir.logging'].create({
            'name': 'Gestor Projectes',
            'type': 'server',
            'level': 'info',
            'message': f"Nou projecte creat amb ID {record.id}",
            'path': 'models/_gestorProjectes_.py',
            'line': 'create',
            'func': 'create',
        })

        return record
    
    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'completed':
            self.end_date = fields.Date.today()
            # Perform some action when the state is changed to completed
            # Example: Log a message
            self.env['ir.logging'].create({
                'name': 'Gestor Projectes',
                'type': 'server',
                'level': 'info',
                'message': f"Projecte amb ID {self.id} marcat com completat.",
                'path': 'models/_gestorProjectes_.py',
                'line': '_onchange_state',
                'func': '_onchange_state',
            })
        elif self.state == 'inProgress':
            self.start_date = fields.Date.today()

