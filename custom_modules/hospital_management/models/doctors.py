from odoo import models, fields, api


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


from datetime import datetime, timedelta


class HospitalAppointmentDate(models.Model):
    _name = "hospital.appointment.date"
    _description = "Appointment Date"
    _rec_name = "date"

    date = fields.Date("Date", required=True)
    slot_ids = fields.One2many(
        "hospital.appointment.slot", "date_id", string="Time Slots"
    )
    _sql_constraints = [
        ("unique_appointment_date", "unique(date)", "Appointment date must be unique!")
    ]

    @api.model
    def _generate_time_slots(self):
        """Generate predefined time slots (9:00 AM - 6:00 PM with a break from 1:00 - 2:00 PM)."""
        slots = []
        start_time = 9.0  # 9:00 AM in float format
        end_time = 18.0  # 6:00 PM
        break_start = 13.0  # 1:00 PM
        break_end = 14.0  # 2:00 PM

        while start_time < end_time:
            if start_time < break_start or start_time >= break_end:
                slots.append(start_time)
            start_time += 0.5  # Increment by 30 minutes
        return slots

    @api.model
    def _generate_appointment_dates(self):
        """Creates appointment dates automatically for the next 30 days if not already present."""
        today = datetime.today().date()
        for i in range(30):
            appointment_date = today + timedelta(days=i)

            # Check if the date already exists
            if not self.search([("date", "=", appointment_date)]):
                new_date = self.create({"date": appointment_date})
                predefined_slots = self._generate_time_slots()

                # Create slots for the date
                for slot_time in predefined_slots:
                    self.env["hospital.appointment.slot"].create(
                        {"date_id": new_date.id, "time": slot_time}
                    )


class HospitalAppointmentSlot(models.Model):
    _name = "hospital.appointment.slot"
    _description = "Appointment Slot"
    _rec_name = "time"

    date_id = fields.Many2one(
        "hospital.appointment.date",
        string="Appointment Date",
        ondelete="cascade",
    )
    time = fields.Char(
        "Time Slot",
        help="Time in 24-hour format (e.g., 9.5 for 9:30 AM)",
    )
    is_booked = fields.Boolean("Booked", default=False)
