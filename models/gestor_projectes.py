from odoo import models, fields, api

class gestor_projectes(models.Model):
    _name = 'gestor.projectes'
    _description = 'Gestor de Projectes'

    tipus = fields.Selection([
        ('xapa', 'Xapa'),
        ('pintura', 'Pintura'),
        ('mecanica', 'Mecanica'),
        ('electrica', 'Electrica'),
        ('manteniment', 'Manteniment'),
        ('altres', 'Altres')
    ])
    description = fields.Text('Descripció del problema')
    creation_date = fields.Date('Data de creació')
    start_date = fields.Date('Data d\'Inici')
    end_date = fields.Date('Data de Fi')
    state = fields.Selection([
        ('notStarted', 'No Iniciat'),
        ('inProgress', 'En Progrés'),
        ('completed', 'Completat')
    ], string='Estat', required=True, default='notStarted')
    observacions = fields.Text('Observacions')
    worksDone = fields.Text('Obres Realitzades')
    hoursWorked = fields.Float('Hores Treballades')
    usuari = fields.Many2one('res.users', string='Usuari', default=lambda self: self.env.user)
    preu_hora = fields.Float(
    string="Preu / hora",
    related="tipus_id.preu_hora",
    readonly=True,
    store=True)
    import_pressupost = fields.Monetary(
    string="Import pressupost",
    currency_field="company_currency",
    compute="_compute_import_pressupost",
    store=True)

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
            self.end_date = False
        else:
            self.start_date = False
            self.end_date = False

    # ----------------------------------------------------------
    # COMPUTE
    # ----------------------------------------------------------
    @api.depends("hoursWorked ", "preu_hora")
    def _compute_import_pressupost(self):
        for rec in self:
            rec.import_pressupost = rec.hoursWorked  * rec.preu_hora

    # ----------------------------------------------------------
    # BUTTON
    # ----------------------------------------------------------
    def action_show_pressupost(self):
        """Show a popup with the amount to pay."""
        self.ensure_one()
        if self.state != "completed":
            raise UserError(_("You can only create a pressupost when the project is completed."))

        message = _(
            "Have to pay %(amount).2f € for %(hours).2f hours",
            amount=self.import_pressupost,
            hours=self.hores_treballades,
        )
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Pressupost"),
                "message": message,
                "sticky": True,
            },
        }
