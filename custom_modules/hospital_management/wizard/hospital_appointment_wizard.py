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
    appointment_date = fields.Date(string="Appointment Date", required=True)
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
        patient = self.patient_id
        message = f"New appointment created with Dr. {self.doctor_id.name} on {self.appointment_date} at {self.slot_id.display_name}"
        patient.message_post(body=message, subtype_xmlid="mail.mt_note")
        return {"type": "ir.actions.act_window_close"}

    @api.onchange("doctor_id", "appointment_date")
    def _onchange_doctor_date(self):
        """
        Automatically generate slots if they don't exist for the selected doctor and date
        """
        if self.doctor_id and self.appointment_date:
            # Check if slots exist for this doctor and date
            slot_env = self.env["hospital.appointment.slot"]
            existing_slots = slot_env.search(
                [
                    ("doctor_id", "=", self.doctor_id.id),
                    ("date", "=", self.appointment_date),
                ]
            )

            # If no slots exist, generate them
            if not existing_slots:
                self.doctor_id.generate_appointment_slots(self.appointment_date)

            # Clear the slot selection
            self.slot_id = False

            # Return domain to filter slots
            return {
                "domain": {
                    "slot_id": [
                        ("doctor_id", "=", self.doctor_id.id),
                        ("date", "=", self.appointment_date),
                        ("is_booked", "=", False),
                    ]
                }
            }
