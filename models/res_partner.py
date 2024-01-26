# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"
    _description = "Extended Partner Model for Field Service usage"

    type = fields.Selection(
        selection_add=[("field_service", "Service Location")],
        help="Use to identify local service sites of the customer.",
    )
    field_service_type = fields.Selection(
        [
            ("solar", "Solar"),
            ("water_heater", "Water Heater"),
            ("genset", "Genset"),
            ("air_conditioning", "Air Conditioning"),
            ("other", "Other"),
        ],
        string="Type",
        help="Select the type of field service",
    )

    equipement = fields.Char(string="Equipement", index="trigram")
    other_description = fields.Char(
        string="Site Description",
    )
    service_field_count = fields.Integer(compute="compute_count")

    def get_field_service(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Service Location",
            "view_mode": "tree,form",
            "res_model": "res.partner",
            "domain": [
                ("type", "=", "field_service"),
                ("id", "in", self.field_service_type.ids),
            ],
            "context": {
                "create": False,
                "view_mode": "tree,form",
                "target": "main",
            },
        }

    def compute_count(self):
        for record in self:
            record.service_field_count = self.env["res.partner"].search_count(
                [("type", "=", "field_service"), ("id", "in", self.field_service_type.ids)]
            )
