from odoo import models, fields


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


class PharmacyMedicine(models.Model):
    _inherit = "pharmacy.medicine"

    prescription_ids = fields.One2many(
        "hospital.prescription", "medicine_id", string="Prescriptions"
    )
