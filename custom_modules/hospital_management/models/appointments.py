from odoo.exceptions import UserError

from odoo import models, fields, api


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    _rec_name = "patient_id"
    patient_id = fields.Many2one("hospital.patient", string="Patient", required=True)
    patient_image = fields.Image(
        related="patient_id.image", string="Patient Image", store=True
    )
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", required=True)
    status = fields.Selection(
        selection=lambda self: self._get_status_selection(),
        string="Status",
        default="draft",
        required=True,
    )
    prescription_ids = fields.One2many(
        "hospital.prescription", "appointment_id", string="Prescribed Medicines"
    )
    medicine_ids = fields.Many2one(
        string="Medicines",
        related="prescription_ids.medicine_id",
    )
    quantity = fields.Integer("Quantity", related="prescription_ids.quantity")

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

    # @api.model_create_multi
    def create(self, vals):
        """Override create method to auto-confirm new appointments"""

        vals["status"] = "confirmed"  # Change status to confirmed on creation
        # return super(HospitalAppointment, self).create(vals_list)
        slot = self.env["hospital.appointment.slot"].browse(vals["slot_id"])

        if slot.is_booked:
            raise UserError("This time slot is already booked.")

        # Create appointment
        appointment = super(HospitalAppointment, self).create(vals)

        # Mark slot as booked
        slot.write({"is_booked": True, "appointment_id": appointment.id})

        return appointment

    def action_start_treatment(self):
        """Move appointment to 'Ongoing' and allow doctors to add medicines."""
        self.status = "ongoing"

    def action_confirm_prescription(self):
        # print("Confirming prescription for appointment:")
        # print(self.prescription_ids.medicine_id.quantity)
        # print(self.quantity)
        for prescription in self.prescription_ids:
            prescription.confirm_prescription()
        self.status = "done"

    #####################################
    def unlink(self):
        """Unlink appointments and free up slots"""
        for appointment in self:
            if appointment.slot_id:
                appointment.slot_id.write({"is_booked": False, "appointment_id": False})
        return super(HospitalAppointment, self).unlink()

    appointment_date = fields.Date(
        "Appointment Date", required=True, default=fields.Date.today
    )
    slot_id = fields.Many2one("hospital.appointment.slot", string="Time Slot")

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
