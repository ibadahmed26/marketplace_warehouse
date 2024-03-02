from odoo import models, fields, api


class WarehouseSelectionWizard(models.TransientModel):
    _name = 'warehouse.selection.wizard'

    warehouse_id = fields.Many2one('stock.warehouse', string='Destination Warehouse', domain=[('is_company', '=', True)])
    sale_order_line_id = fields.Many2one('sale.order.line', string='Sale Order Line')

    def confirm_action(self):
        nearby_company_warehouse = self.warehouse_id
        for sale_line in self.sale_order_line_id:
            operational_user = self.env.user.id
            picking_type = sale_line.warehouse_id.int_type_id
            location_id = sale_line.warehouse_id.lot_stock_id
            company_warehouse = nearby_company_warehouse
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

            sale_order = self.env['sale.order'].browse(sale_line.order_id.id)
            if sale_order.exists:
                for picking in sale_order.picking_ids:
                    picking.update({'location_id': company_warehouse_location.id})
                    for move in picking.move_lines:
                        move.update({'warehouse_id': company_warehouse.id})
                        move.update({'location_id': company_warehouse_location.id})
                        for move_line in move.move_line_ids:
                            move_line.update({'location_id': company_warehouse_location.id})
