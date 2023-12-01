from odoo import api, fields, models

class ProjectTask(models.Model):
    _inherit = "project.task"

    sale_order_id = fields.Many2one('sale.order', 'Sales Order', store=True, help="Sales order to which the task is linked.")
    description = fields.Html(related='sale_order_id.instruction')
    product_id = fields.Many2one(related='sale_order_id.product_id') 
    product_ids = fields.Many2many('product.product', string='Products', compute='_compute_product_ids', store=True)
    warehouse_id = fields.Many2one(related='sale_order_id.warehouse_id') 
    sale_order_line_id = fields.Many2one('sale.order.line', string="Sales Order Line", required=True, ondelete='cascade')
    product_uom_qty = fields.Float(related='sale_order_line_id.product_uom_qty')
    name = fields.Text(related='sale_order_line_id.name')
    order_id = fields.Many2one(related='sale_order_line_id.order_id')
    order_line = fields.One2many(
        comodel_name='sale.order.line', related='sale_order_id.order_line')
    delivery_count = fields.Integer(related='sale_order_id.delivery_count')
    picking_ids = fields.One2many(related='sale_order_id.picking_ids')
    partner_id = fields.Many2one(related='sale_order_id.partner_id')
    tag_ids = fields.Many2many('project.tags', string='Tags', compute='_compute_default_tags')

    @api.depends('sale_order_id')
    def _compute_product_ids(self):
        for task in self:
            task.product_ids = task.sale_order_id.order_line.mapped('product_id')


    def action_view_delivery(self):
        return self._get_action_view_picking(self.picking_ids)

    def _get_action_view_picking(self, pickings):
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif len(pickings) == 1:
            action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
            action['res_id'] = pickings.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.depends('warehouse_id')
    def _compute_default_tags(self):
        for record in self:  
            if record.warehouse_id: 
                existing_tag = self.env['project.tags'].search([
                    ('name', '=', record.warehouse_id.name)
                ], limit=1)
                if not existing_tag:  
                    new_tag = self.env['project.tags'].create({ 
                        'warehouse_id': record.warehouse_id.id, 
                    }) 
                    record.write({'tag_ids': [(4, new_tag.id)]})
                else: 
                    record.write({'tag_ids': [(4, existing_tag.id)]}) 


class ProjectTags(models.Model):
    _inherit = 'project.tags'

    sale_order_id = fields.Many2one('sale.order', 'Sales Order', store=True, help="Sales order to which the task is linked.") 
    warehouse_id = fields.Many2one(related='sale_order_id.warehouse_id') 
