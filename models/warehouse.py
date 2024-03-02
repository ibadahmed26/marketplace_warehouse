from odoo import models, fields, api


class MarketplaceWarehouse(models.Model):
    _inherit = 'stock.warehouse'
    _rec_name = "name"
    _description = 'Managing multi warehousing for marketplace sellers'

    marketplace_seller_id = fields.Many2one(
        "res.partner", string="Seller", default=lambda
            self: self.env.user.partner_id.id if self.env.user.partner_id and self.env.user.partner_id.seller else
        self.env['res.partner'], copy=False, tracking=True)
    country_id = fields.Many2one('res.country', string='Country', required=True)
    state_id = fields.Many2one("res.country.state", string='State', required=True)
    city = fields.Char('City')
    zip = fields.Char('Zip')
    is_company = fields.Boolean(default=False)

    @api.onchange('is_company')
    def onchange_is_company(self):
        if self.is_company:
            self.marketplace_seller_id = False
        else:
            self.marketplace_seller_id = self.env['res.partner']