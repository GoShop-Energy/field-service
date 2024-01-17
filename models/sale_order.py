# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    instruction = fields.Html(
        string="Service Instructions",
        store=True,
        readonly=False,
    )

    product_id = fields.Many2one(
        comodel_name="product.product",
        related="order_line.product_id",
        string="Product",
    )

    service_tracking = fields.Selection(
        related="product_id.service_tracking", string="Service Tracking"
    )

    has_service = fields.Boolean(
        string="Has Service Product", compute="_compute_has_service", store=True
    )

    parent_id = fields.Many2one("res.partner")
    child_id = fields.Many2one(
        "res.partner",
        domain="[('parent_id', '=', partner_id), ('type', '=', 'field_service')]",
        compute="_compute_child_id",
        store=True,
    )
    terms_type = fields.Selection(related="company_id.terms_type")

    @api.depends("order_line.product_id")
    def _compute_has_service(self):
        for order in self:
            order.has_service = any(
                line.product_id.type == "service"
                and line.product_id.service_tracking == "task_global_project"
                for line in order.order_line
            )

    @api.depends("partner_id")
    def _compute_child_id(self):
        for order in self:
            field_service_children = order.partner_id.child_ids.filtered(
                lambda child: child.type == "field_service"
            )
            # Assign the first child if available, otherwise assign the partner itself
            order.child_id = field_service_children[:1] or order.partner_id
