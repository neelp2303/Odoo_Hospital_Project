from odoo import models, fields


class appointment_data(models.Model):
    _name = "hospital.appointment"
    _description = "appointment_data"
    patient_id = fields.Many2one("hospital.patient", string="Patient", required=True)
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", required=True)
    appointment_date = fields.Datetime(
        "Appointment Date", required=True, default=fields.Datetime.now
    )
    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("done", "Done"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        default="draft",
        required=True,
    )
