from odoo import models, fields


class SaleOrderLineWizard(models.TransientModel):
    _name = "sale.order.line.wizard"
    _description = "Appointment Wizard"

    order_id = fields.Many2one("sale.order", string="Sale Order", required=True)
    product_id = fields.Many2one("product.product", string="Product", required=True)
    name = fields.Char(string="Description", required=True)
    product_uom_qty = fields.Float(string="Quantity", required=True)
    price_unit = fields.Float(string="Unit Price", required=True)

    def action_add_line(self):
        self.ensure_one()
        self.env["sale.order.line"].create(
            {
                "order_id": self.order_id.id,
                "product_id": self.product_id.id,
                "name": self.name,
                "product_uom_qty": self.product_uom_qty,
                "price_unit": self.price_unit,
            }
        )
