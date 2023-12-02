# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = "project.task"

    sale_order_id = fields.Many2one(
        "sale.order",
        "Sales Order",
        store=True,
        help="Sales order to which the task is linked.",
    )
    description = fields.Html(compute="_compute_description", readonly=False)
    order_line_table = fields.Html(
        string="HTML Field", compute="_compute_order_line_table"
    )

    product_ids = fields.Many2many(
        "product.product", string="Products", compute="_compute_product_ids", store=True
    )
    warehouse_id = fields.Many2one(related="sale_order_id.warehouse_id")
    order_line = fields.One2many(
        comodel_name="sale.order.line",
        related="sale_order_id.order_line",
        readonly=False,
    )

    delivery_count = fields.Integer(related="sale_order_id.delivery_count")
    picking_ids = fields.One2many(related="sale_order_id.picking_ids")
    partner_id = fields.Many2one(related="sale_order_id.partner_id")
    child_id = fields.Many2one(related="sale_order_id.child_id", readonly=False)

    tag_ids = fields.Many2many("project.tags", string="Tags", readonly=False)
    company_id = fields.Many2one(comodel_name="res.company")

    has_default_tag = fields.Boolean(string="Default Tag Created", default=False)

    @api.depends("sale_order_id")
    def _compute_product_ids(self):
        for task in self:
            task.product_ids = task.sale_order_id.order_line.mapped("product_id")

    def action_view_delivery(self):
        return self._get_action_view_picking(self.picking_ids)

    def _get_action_view_picking(self, pickings):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock.action_picking_tree_all"
        )
        if len(pickings) > 1:
            action["domain"] = [("id", "in", pickings.ids)]
        elif len(pickings) == 1:
            action["views"] = [(self.env.ref("stock.view_picking_form").id, "form")]
            action["res_id"] = pickings.id
        else:
            action = {"type": "ir.actions.act_window_close"}
        return action

    @api.model
    def create(self, values):
        record = super(ProjectTask, self).create(values)
        tag_values = record._prepare_default_tag_id()
        record.write({"tag_ids": tag_values})

        return record

    def _prepare_default_tag_id(self):
        self.ensure_one()
        default_tag_ids = []

        if self.warehouse_id:
            existing_tag = self.env["project.tags"].search(
                [("name", "=", self.warehouse_id.name)], limit=1
            )
            if not existing_tag:
                new_tag = self.env["project.tags"].create(
                    {
                        "warehouse_id": self.warehouse_id.id,
                        "name": self.warehouse_id.name,
                    }
                )
                default_tag_ids.append((4, new_tag.id))
            else:
                default_tag_ids.append((4, existing_tag.id))

        return default_tag_ids

    @api.depends("sale_order_id.instruction")
    def _compute_description(self):
        for record in self:
            record.description = record.sale_order_id.instruction

    def _compute_order_line_table(self):
        for record in self:
            html_content = '<table style="width:100%; border-collapse: collapse; border: 1px solid black;">'
            html_content += '<tr style="background-color: #f2f2f2;"><th style="border: 1px solid black; padding: 8px;">Product</th><th style="border: 1px solid black; padding: 8px;">Description</th><th style="border: 1px solid black; padding: 8px;">Quantity</th></tr>'

            for line in record.order_line:
                html_content += f'<tr><td style="border: 1px solid black; padding: 8px;">{line.product_id.name}</td><td style="border: 1px solid black; padding: 8px;">{line.name}</td><td style="border: 1px solid black; padding: 8px;">{line.product_uom_qty}</td></tr>'

            html_content += "</table>"
            record.order_line_table = html_content

    def action_fs_navigate(self):
        if not self.child_id.city or not self.child_id.country_id:
            return {
                "name": _("Service Location"),
                "type": "ir.actions.act_window",
                "res_model": "res.partner",
                "res_id": self.child_id.id,
                "view_mode": "form",
                "view_id": self.env.ref(
                    "industry_fsm.view_partner_address_form_industry_fsm"
                ).id,
                "target": "new",
            }
        return self.child_id.action_partner_navigate()
