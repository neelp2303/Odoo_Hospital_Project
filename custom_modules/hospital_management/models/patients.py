from odoo import models, fields, api


class patients_data(models.Model):
    _name = "hospital.patient"
    _description = "Patients Data"

    name = fields.Char("Name", required=True)
    age = fields.Integer("Age")
    ref = fields.Char("Ref", default="NEW")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], "Gender")
    dob = fields.Date("Dob")
    contact_number = fields.Char("Contact Number")
    address = fields.Text("Address")
    admission_date = fields.Datetime("Admission Date")
    discharge_date = fields.Datetime("Discharge Date")
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor")
    image = fields.Image("Patient Image")
    doctor_reference = fields.Reference(
        [("hospital.doctor", "Doctor")], string="Doctor by reference"
    )
    partner_id = fields.Many2one(
        "res.partner", string="Related Partner", required=True
    )

    # Ensure that the patient has a related partner record
    @api.model
    def create(self, vals):
        # Create a related partner automatically
        partner = self.env["res.partner"].create(
            {"name": vals.get("name", "New Patient")}
        )
        vals["partner_id"] = partner.id  # Link patient to partner
        return super(patients_data, self).create(vals)

    def action_open_appointment_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Create Appointment",
            "res_model": "hospital.appointment.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_patient_id": self.id},
        }

    bed_type_id = fields.Many2one("hospital.bed.type", string="Preferred Bed Type")
    bed_id = fields.Many2one(
        "hospital.bed",
        string="Bed Booked",
        domain="[('bed_type_id', '=', bed_type_id), ('status', '=', 'discharged')]",
        ondelete="set null",  # When the related bed is deleted, this field becomes NULL
    )
    has_bed = fields.Boolean(
        "Has Bed", compute="_compute_has_bed", store=True, readonly=True
    )
    bed_name = fields.Char(
        "Bed Type",
        # Fetches bed type automatically
        store=True,
        readonly=True,
    )
    patient_stat = fields.Char("Patient Stat")

    @api.depends("bed_id")
    def _compute_has_bed(self):
        """Compute if the patient has a booked bed"""
        for record in self:
            record.has_bed = bool(record.bed_id)
            record.bed_name = record.bed_id.bed_type_id.name if record.bed_id else False
            record.patient_stat = record.bed_id.status
            record.discharge_date = record.bed_id.discharge_date
            record.admission_date = record.bed_id.admission_date

    # def write(self, vals):
    #     print("Update Patient")
    #     return super(patients_data, self).write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "ref" not in vals or vals["ref"] == "NEW":
                vals["ref"] = self.env["ir.sequence"].next_by_code("hospital.patient")

        return super(patients_data, self).create(vals_list)


class AccountMove(models.Model):
    _inherit = "account.move"

    patient_id = fields.Many2one("hospital.patient", string="Patient")
