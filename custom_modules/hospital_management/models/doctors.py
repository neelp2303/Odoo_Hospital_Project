from odoo import models, fields


class doctors_data(models.Model):
    _name = "hospital.doctor"
    _description = "doctors Data"

    name = fields.Char("Name", required=True)
    age = fields.Integer("Age")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("other", "Other")], "Gender"
    )
    dob = fields.Date("Dob")
    contact_number = fields.Char("Contact Number")
    address = fields.Text("Address")
    specialization = fields.Char("Specialization")
    image = fields.Image("Doctor Image")
    conference_ids = fields.Many2many("hospital.conference", string="Conferences")
    appointment_ids = fields.One2many(
        "hospital.appointment", "doctor_id", string="Appointments"
    )

    def write(self, vals):
        print("Updated Doctor")
        return super(doctors_data, self).write(vals)

    appointment_slot_ids = fields.One2many(
        "hospital.appointment.slot", "doctor_id", string="Appointment Slots"
    )

    # @api.model
    def create(self, vals):
        """Automatically generate fixed time slots for new doctors"""
        doctor = super(doctors_data, self).create(vals)

        # Predefined fixed slots (9 AM - 6 PM with 30-min intervals, excluding 1 PM - 2 PM)
        slot_times = [
            (9, 0),
            (9, 30),
            (10, 0),
            (10, 30),
            (11, 0),
            (11, 30),
            (12, 0),
            (12, 30),
            (2, 0),
            (2, 30),
            (3, 0),
            (3, 30),
            (4, 0),
            (4, 30),
            (5, 0),
            (5, 30),
        ]

        slots = []
        for hour, minute in slot_times:
            slots.append(
                (
                    0,
                    0,
                    {
                        "doctor_id": doctor.id,
                        "time": f"{hour:02}:{minute:02}",
                    },
                )
            )

        doctor.appointment_slot_ids = slots
        return doctor


class HospitalAppointmentSlot(models.Model):
    _name = "hospital.appointment.slot"
    _description = "Appointment Slots"
    _rec_name = "time"

    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", required=True)
    time = fields.Char("Time Slot")
    is_booked = fields.Boolean("Booked", default=False)
