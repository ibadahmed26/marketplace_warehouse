from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange('product_id')
    def onchange_order_line(self):
        for order_line in self:
            if order_line.product_id:
                order_line.order_id.warehouse_id = order_line.product_id.warehouse.id

    def action_sent_to_supplier(self):
        for sale_line in self:
            view_id = self.env.ref('marketplace_warehouse.view_warehouse_selection_wizard_form').id
            return {
                'name': 'Select Destination Warehouse',
                'view_mode': 'form',
                'view_id': view_id,
                'view_type': 'form',
                'res_model': 'warehouse.selection.wizard',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context': {'default_sale_order_line_id': sale_line.id},
            }


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('order_line', 'partner_id', 'partner_shipping_id')
    def onchange_order_line(self):
        self.ensure_one()
        delivery_line = self.order_line.filtered('is_delivery')
        if delivery_line:
            self.recompute_delivery_price = True

        product_with_warehouse = next(
            (line.product_id for line in self.order_line if line.product_id and line.product_id.warehouse), None)
        self.warehouse_id = product_with_warehouse.warehouse.id if product_with_warehouse else self._get_default_warehouse_id()

    def _get_default_warehouse_id(self):
        default_warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.env.company.id)], limit=1)
        return default_warehouse.id if default_warehouse else False
