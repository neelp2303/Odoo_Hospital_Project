from odoo import models, fields


class patients_data(models.Model):
    _name = "hospital.patient"
    _description = "Patients Data"

    name = fields.Char("Name", required=True)
    age = fields.Integer("Age")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], "Gender")
    dob = fields.Date("Dob")
    contact_number = fields.Char("Contact Number")
    address = fields.Text("Address")
    admission_date = fields.Date(default=fields.Datetime.now)
    discharge_date = fields.Date("Discharge Date")
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", required=True)
    image = fields.Image("Patient Image")

    def action_open_appointment_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Create Appointment",
            "res_model": "hospital.appointment.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_patient_id": self.id},
        }


class HospitalPatient(models.Model):
    _inherit = "hospital.patient"

    bed_type_id = fields.Many2one("hospital.bed.type", string="Preferred Bed Type")
    bed_id = fields.Many2one(
        "hospital.bed",
        string="Bed Booked",
        domain="[('bed_type_id', '=', bed_type_id), ('status', '=', 'available')]",
    )
