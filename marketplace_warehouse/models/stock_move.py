from odoo import models, api


class StockMove(models.Model):
    _inherit = "stock.move"

    def _action_assign(self):
        for stock_move in self:
            if stock_move.sale_line_id:
                for order_line in stock_move.sale_line_id:
                    if order_line.order_id and order_line.order_id.warehouse_id:
                        stock_move.write({'warehouse_id': order_line.order_id.warehouse_id})
                        stock_move.write({'location_id': order_line.order_id.warehouse_id.lot_stock_id})
        res = super(StockMove, self)._action_assign()
        return res
