from odoo import models, fields, api


class PharmacySale(models.Model):
    _name = "pharmacy.sale"
    _description = "Pharmacy Sales"

    patient_id = fields.Many2one("hospital.patient", string="Patient", required=True)
    medicine_id = fields.Many2one("pharmacy.medicine", string="Medicine", required=True)
    quantity = fields.Integer(string="Quantity", required=True, default=1)
    price = fields.Float(string="Total Price", compute="_compute_price", store=True)

    @api.depends("medicine_id", "quantity")
    def _compute_price(self):
        for record in self:
            record.price = record.medicine_id.price * record.quantity

    def create(self, vals):
        medicine = self.env["pharmacy.medicine"].browse(vals["medicine_id"])
        if medicine.quantity < vals["quantity"]:
            raise ValueError("Not enough stock!")
        medicine.quantity -= vals["quantity"]
        return super(PharmacySale, self).create(vals)
