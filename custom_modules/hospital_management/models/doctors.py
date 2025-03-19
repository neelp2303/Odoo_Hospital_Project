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
