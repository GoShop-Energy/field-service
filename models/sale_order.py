# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    instruction = fields.Html(string='Notes')

    product_id = fields.Many2one(
        comodel_name='product.product',related='order_line.product_id',
        string="Product")
    
    has_service = fields.Boolean(
        string='Has Service Product',
        compute='_compute_has_service',
        store=True,
    )

    @api.depends('order_line.product_id')
    def _compute_has_service(self):
        for order in self:
            order.has_service = any(line.product_id.type == 'service' for line in order.order_line)
    
    def get_products_from_sale_order(self): 
        order_lines = self.env['sale.order.line'].search([('order_id', '=', self.id)])
        products = order_lines.mapped('product_id') 
        return products
    
    service_product_names = fields.Text(
        string='Service Product Names',
        compute='_compute_service_product_names',
        store=True,
    )

    @api.depends('order_line.product_id')
    def _compute_service_product_names(self):
        for order in self:
            service_product_names = order.order_line.filtered(lambda line: line.product_id.type == 'service').mapped('product_id.display_name')
            order.service_product_names = ", ".join(service_product_names)