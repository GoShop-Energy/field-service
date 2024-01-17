# -*- coding: utf-8 -*-

from odoo import models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _timesheet_create_task_prepare_values(self, project):
        values = super(SaleOrderLine, self)._timesheet_create_task_prepare_values(
            project
        )
        tag_values = self._prepare_default_tag_id()
        values["tag_ids"] = tag_values
        values["description"] = self.order_id.instruction
        values["order_line_table"] = self._compute_order_line_table()

        return values

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
                        "name": self.warehouse_id.name,
                    }
                )
                default_tag_ids.append((4, new_tag.id))
            else:
                default_tag_ids.append((4, existing_tag.id))

        return default_tag_ids

    def _compute_order_line_table(self):
        for record in self:
            html_content = '<table style="width:100%; border-collapse: collapse; border: 1px solid black;">'
            html_content += '<tr style="background-color: #f2f2f2;"><th style="border: 1px solid black; padding: 8px;">Product</th><th style="border: 1px solid black; padding: 8px;">Description</th><th style="border: 1px solid black; padding: 8px;">Quantity</th></tr>'

            for line in record.order_id.order_line:
                html_content += f'<tr><td style="border: 1px solid black; padding: 8px;">{line.product_id.name}</td><td style="border: 1px solid black; padding: 8px;">{line.name}</td><td style="border: 1px solid black; padding: 8px;">{line.product_uom_qty}</td></tr>'

            html_content += "</table>"
        return html_content
