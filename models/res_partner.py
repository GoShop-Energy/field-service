from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Add service field'
    
    type = fields.Selection(selection_add=[('field_service', 'Service Location')],
                            help="Service Location: This field represents the type of service.")
    field_service_type = fields.Selection([
        ('solar', 'Solar'),
        ('water_heater', 'Water Heater'),
        ('genset', 'Genset'),
        ('air_conditioning', 'Air Conditioning'),
        ('other', 'Other')],
        string='Type',
        help='Select the type of field service'
    )

    other_description = fields.Char('Other Description')
    
    @api.onchange('field_service_type')
    def on_change_field_service_type(self):
        if self.field_service_type != 'other':
            self.other_description = ''