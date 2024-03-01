from odoo import models, fields, api


class WarehouseSelectionWizard(models.TransientModel):
    _name = 'warehouse.selection.wizard'

    warehouse_id = fields.Many2one('stock.warehouse', string='Destination Warehouse', domain=[('is_company', '=', True)])

    def confirm_action(self):
        print("Hello wizard")
        # Here you can access the selected warehouse using self.warehouse_id
