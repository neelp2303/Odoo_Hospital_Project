from odoo import models, fields


class patients_data(models.Model):
    _name = "hospital.patient"
    _description = "Patients Data"

    name = fields.Char("Name", required=True)
    age = fields.Integer("Age")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("other", "Other")], "Gender"
    )
    dob = fields.Date("Dob")
    contact_number = fields.Char("Contact Number")
    address = fields.Text("Address")
    admission_date = fields.Date("Admission Date")
    discharge_date = fields.Date("Discharge Date")
    doctor_name = fields.Char("Doctor Name")

