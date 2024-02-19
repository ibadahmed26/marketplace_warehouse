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
            operational_user = self.env.user.id
            picking_type = sale_line.warehouse_id.int_type_id
            location_id = sale_line.warehouse_id.lot_stock_id
            company_warehouse = self.env['stock.warehouse'].search([
                ('company_id', '=', self.env.company.id)], limit=1)
            seller_id = sale_line.warehouse_id.marketplace_seller_id
            company_warehouse_location = company_warehouse.lot_stock_id

            picking_vals = {
                'partner_id': operational_user,
                'picking_type_id': picking_type.id,
                'location_id': location_id.id,
                'location_dest_id': company_warehouse_location.id,
                'seller_id': seller_id.id,
                'move_ids_without_package': [],
            }
            move_line = {
                'name': sale_line.product_id.name,
                'product_id': sale_line.product_id.id,
                'product_uom_qty': sale_line.product_uom_qty,
                'product_uom': sale_line.product_id.uom_id.id,
                'location_id': location_id.id,
                'location_dest_id': company_warehouse_location.id,
                'quantity_done': sale_line.product_uom_qty,
            }
            picking_vals['move_ids_without_package'].append((0, 0, move_line))

            created_picking = self.env['stock.picking'].create(picking_vals)
            if created_picking:
                created_picking.action_confirm()
                created_picking.button_validate()

            if created_picking.state == 'done':
                sale_line.write({'marketplace_state': 'sent_to_supplier'})


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
