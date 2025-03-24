from odoo import models, fields, api


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"

    patient_id = fields.Many2one("hospital.patient", string="Patient", required=True)
    patient_image = fields.Image(
        related="patient_id.image", string="Patient Image", store=True
    )
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", required=True)
    appointment_date = fields.Datetime(
        "Appointment Date", required=True, default=fields.Datetime.now
    )

    status = fields.Selection(
        selection=lambda self: self._get_status_selection(),
        string="Status",
        default="draft",
        required=True,
    )

    @api.model
    def _get_status_selection(self):
        """Dynamically get status selection based on cancel_days setting"""
        selection = [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("ongoing", "Ongoing"),
            ("done", "Done"),
        ]
        cancel_enabled = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("hospital_management.cancel_days")
            == "True"
        )
        if cancel_enabled:
            selection.append(("canceled", "Canceled"))
        return selection

    @api.model_create_multi
    def create(self, vals_list):
        """Override create method to auto-confirm new appointments"""
        for vals in vals_list:
            vals["status"] = "confirmed"  # Change status to confirmed on creation
        return super(HospitalAppointment, self).create(vals_list)

    prescription_ids = fields.One2many(
        "hospital.prescription", "appointment_id", string="Prescribed Medicines"
    )
    medicine_ids = fields.Many2one(
        string="Medicines",
        related="prescription_ids.medicine_id",
    )
    quantity = fields.Integer("Quantity", related="prescription_ids.quantity")

    def action_start_treatment(self):
        """Move appointment to 'Ongoing' and allow doctors to add medicines."""
        self.status = "ongoing"

    def action_confirm_prescription(self):
        print("Confirming prescription for appointment:")
        # print(self.prescription_ids.medicine_id.quantity)
        # print(self.quantity)
        for prescription in self.prescription_ids:
            prescription.confirm_prescription()
        self.status = "done"
