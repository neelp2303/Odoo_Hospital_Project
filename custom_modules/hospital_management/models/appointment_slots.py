from odoo import models, fields, api


class AppointmentSlot(models.Model):
    _name = "hospital.appointment.slot"
    _description = "Doctor Appointment Slots"
    _rec_name = "display_name"
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor")
    date = fields.Date(string="Date")
    start_time = fields.Float(string="Start Time")
    end_time = fields.Float(string="End Time")
    is_booked = fields.Boolean(string="Booked", default=False)
    appointment_id = fields.Many2one("hospital.appointment", string="Appointment")
    display_name = fields.Char(
        string="Slot Name", compute="_compute_display_name", store=True
    )

    def _format_time(self, time_float):
        """Convert float time to formatted time string"""
        # Separate hours and minutes
        hours = int(time_float)
        minutes = int((time_float % 1) * 60)

        # Convert to 12-hour format
        am_pm = "AM" if hours < 12 else "PM"
        display_hours = hours if hours <= 12 else hours - 12
        display_hours = 12 if display_hours == 0 else display_hours

        # Format the time
        return f"{display_hours}:{minutes:02d} {am_pm}"

    @api.depends("start_time", "end_time")
    def _compute_display_name(self):
        """Compute a readable display name for the slot"""
        for slot in self:
            start_time_str = self._format_time(slot.start_time)
            end_time_str = self._format_time(slot.end_time)
            slot.display_name = f"{start_time_str} - {end_time_str}"

    def name_get(self):
        """Override name_get to use the computed display name"""
        return [(slot.id, slot.display_name) for slot in self]

    @api.model
    def generate_slots_for_doctor(self, doctor_id, date):
        """
        Generate time slots for a specific doctor on a given date
        Slots from 9 AM to 6 PM with 30-minute intervals and a break from 1-2 PM
        """
        # Delete existing slots for this doctor and date first
        existing_slots = self.search(
            [
                ("doctor_id", "=", doctor_id),
                ("date", "=", date),
                ("is_booked", "=", False),
            ]
        )
        existing_slots.unlink()

        # Define time slots
        slot_intervals = [
            (9.0, 13.0),  # Morning: 9 AM to 1 PM
            (14.0, 18.0),  # Afternoon: 2 PM to 6 PM
        ]

        slots_to_create = []
        for start, end in slot_intervals:
            current_time = start
            while current_time < end:
                slots_to_create.append(
                    {
                        "doctor_id": doctor_id,
                        "date": date,
                        "start_time": current_time,
                        "end_time": current_time + 0.5,
                        "is_booked": False,
                    }
                )
                current_time += 0.5

        return self.create(slots_to_create)
