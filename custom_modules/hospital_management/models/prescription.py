from odoo import models, fields, api
from odoo.exceptions import UserError


class HospitalPrescription(models.Model):
    _name = "hospital.prescription"
    _description = "Hospital Prescription"

    appointment_id = fields.Many2one(
        "hospital.appointment",
        string="Appointment",
        required=True,
        ondelete="cascade",
    )
    patient_id = fields.Many2one(
        "hospital.patient",
        related="appointment_id.patient_id",
        string="Patient",
        store=True,
        readonly=True,
    )
    medicine_id = fields.Many2one(
        "pharmacy.medicine",
        string="Medicine",
        required=True,
        ondelete="restrict",
    )
    quantity = fields.Integer("Quantity", required=True, default=1)
    status = fields.Selection(
        [("draft", "Draft"), ("confirmed", "Confirmed")],
        string="Status",
        default="draft",
    )

    def confirm_prescription(self):
        """Move prescription to 'Confirmed' and update pharmacy inventory."""
        for record in self:
            if record.status == "confirmed":
                continue  # Avoid double confirmation

            # Fetch the correct medicine record
            medicine = self.env["pharmacy.medicine"].search(
                [("id", "=", record.medicine_id.id)], limit=1
            )

            if not medicine:
                raise UserError("Medicine not found in pharmacy inventory!")

            if medicine.quantity < record.quantity:
                raise UserError(
                    f"Not enough stock for {medicine.name}! Available: {medicine.quantity}"
                )

            # Deduct stock and confirm the prescription
            medicine.sudo().write({"quantity": medicine.quantity - record.quantity})
            record.status = "confirmed"
