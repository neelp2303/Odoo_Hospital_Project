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

    def confirm_prescription(self):
        self.medicine_id.quantity -= self.quantity
