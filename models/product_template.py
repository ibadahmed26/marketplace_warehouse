from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    warehouse = fields.Many2one("stock.warehouse", string="Warehouse", copy=False)

    @api.onchange('marketplace_seller_id')
    def _compute_seller_warehouses(self):
        for record in self:
            return {
                'domain': {
                    'warehouse': [
                        ('marketplace_seller_id', '=', record.marketplace_seller_id.id),
                        ('active', '=', True),
                    ]
                }
            }

    def set_initial_qty(self):
        for template_obj in self:

            location_id = template_obj.marketplace_seller_id.get_seller_global_fields('location_id')
            if template_obj.warehouse:
                location_id = template_obj.warehouse.lot_stock_id.id

            if len(self) == 1:
                if template_obj.mp_qty < 0:
                    raise Warning(_('Initial Quantity can not be negative'))
            if not location_id:
                raise Warning(_("Product seller has no location/warehouse."))
            if template_obj.mp_qty > 0:
                vals = {
                    'product_id': template_obj.product_variant_ids[0].id,
                    'product_temp_id': template_obj.id,
                    'new_quantity': template_obj.mp_qty,
                    'location_id': location_id or False,
                    'note': _("Initial Quantity."),
                    'state': "requested",
                }
                mp_product_stock = self.env['marketplace.stock'].create(vals)
                template_obj.is_initinal_qty_set = True
                mp_product_stock.auto_approve()
