from odoo import models, fields, api


class Medicine(models.Model):
    _name = "pharmacy.medicine"
    _description = "Medicine Inventory"

    name = fields.Char(string="Medicine Name", required=True)
    category = fields.Selection(
        [
            ("tablet", "Tablet"),
            ("capsule", "Capsule"),
            ("syrup", "Syrup"),
            ("injection", "Injection"),
        ],
        string="Category",
        required=True,
    )
    quantity = fields.Integer(string="Stock Quantity", default=0)
    price = fields.Float(string="Price", required=True)

    prescription_ids = fields.One2many(
        "hospital.prescription", "medicine_id", string="Prescriptions"
    )

    product_id = fields.Many2one(
        "product.product", string="Linked Product", readonly=True
    )

    def create(self, vals):
        """Create a corresponding product in the Sales module when a new medicine is added."""
        medicine = super(Medicine, self).create(vals)

        # Check for existing product template
        existing_product = self.env["product.template"].search(
            [("name", "=", medicine.name)], limit=1
        )

        if existing_product:
            # Use the existing product's variant
            product = existing_product.product_variant_id
        else:
            # Create new product template and use its variant
            product_template_vals = {
                "name": medicine.name,
                "type": "consu",
                "list_price": medicine.price,
                "default_code": f"MED-{medicine.id}",
                "categ_id": self.env.ref("product.product_category_all").id,
            }
            product_template = self.env["product.template"].create(
                product_template_vals
            )
            product = product_template.product_variant_id

        return medicine
