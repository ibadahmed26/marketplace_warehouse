from odoo import models, api


class Picking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def create(self, vals):
        picking_sale_order = vals.get('origin')
        sale_order = self.env['sale.order'].search([("name", '=', picking_sale_order)])
        if sale_order:
            if sale_order.warehouse_id and sale_order.warehouse_id.lot_stock_id:
                vals['location_id'] = sale_order.warehouse_id.lot_stock_id.id
        res = super(Picking, self).create(vals)
        return res
