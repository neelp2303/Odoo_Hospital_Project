from odoo import models, fields, api


class HospitalAppointmentWizard(models.TransientModel):
    _name = "hospital.appointment.wizard"
    _description = "Appointment Wizard"

    patient_id = fields.Many2one(
        "hospital.patient",
        string="Patient",
        required=True,
        default=lambda self: self._default_patient(),
    )
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", required=True)
    appointment_date = fields.Datetime(string="Appointment Date", required=True)
    slot_id = fields.Many2one("hospital.appointment.slot", string="Time Slot")

    @api.model
    def _default_patient(self):
        return self.env.context.get("default_patient_id")

    def action_confirm_appointment(self):
        self.env["hospital.appointment"].create(
            {
                "patient_id": self.patient_id.id,
                "doctor_id": self.doctor_id.id,
                "appointment_date": self.appointment_date,
                "slot_id": self.slot_id.id,
            }
        )
        return {"type": "ir.actions.act_window_close"}
