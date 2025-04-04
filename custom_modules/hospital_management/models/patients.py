from odoo import models, fields, api, _


class patients_data(models.Model):
    _name = "hospital.patient"
    _description = "Patients Data"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _inherits = {"res.partner": "partner_id"}
    # name = fields.Char("Name", required=True, tracking=True)

    age = fields.Integer("Age", tracking=True)
    ref = fields.Char("Ref", default="NEW", tracking=True)
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")], "Gender", tracking=True
    )
    dob = fields.Date("Dob", tracking=True)
    contact_number = fields.Char("Contact Number", tracking=True)
    address = fields.Text("Address", tracking=True)
    admission_date = fields.Datetime("Admission Date", tracking=True)
    discharge_date = fields.Datetime("Discharge Date", tracking=True)
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", tracking=True)
    image = fields.Image("Patient Image", tracking=True)
    email = fields.Char("Email", tracking=True)
    doctor_reference = fields.Reference(
        [("hospital.doctor", "Doctor")], string="Doctor by reference", tracking=True
    )
    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True, ondelete="cascade"
    )
    prescription_id = fields.One2many(
        "hospital.prescription", "patient_id", string="Prescriptions", tracking=True
    )
    appointment_id = fields.Many2one(
        related="prescription_id.appointment_id", string="Appointment", tracking=True
    )
    medicine_ids = fields.Many2one(
        related="prescription_id.medicine_id", string="Medicine", tracking=True
    )
    quantity = fields.Integer(
        related="prescription_id.quantity", string="Quantity", tracking=True
    )
    bed_type_id = fields.Many2one(
        "hospital.bed.type", string="Preferred Bed Type", tracking=True
    )
    bed_id = fields.Many2one(
        "hospital.bed",
        string="Bed Booked",
        domain="[('bed_type_id', '=', bed_type_id), ('status', '=', 'discharged')]",
        ondelete="set null",  # When the related bed is deleted, this field becomes NULL
    )
    has_bed = fields.Boolean(
        "Has Bed", compute="_compute_has_bed", store=True, readonly=True, tracking=True
    )
    bed_name = fields.Char(
        "Bed Type",
        # Fetches bed type automatically
        store=True,
        readonly=True,
    )
    patient_stat = fields.Char("Patient Stat")
    # Ensure that the patient has a related partner record

    def action_open_appointment_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Create Appointment",
            "res_model": "hospital.appointment.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_patient_id": self.id},
        }

    def action_open_mass_edit(self):
        return {
            "name": "Mass Edit Patients",
            "type": "ir.actions.act_window",
            "res_model": "hospital.patient.mass.edit.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "active_ids": self.env.context.get("active_ids", []),
                "active_model": "hospital.patient",
            },
        }

    @api.depends("bed_id")
    def _compute_has_bed(self):
        """Compute if the patient has a booked bed"""
        for record in self:
            record.has_bed = bool(record.bed_id)
            record.bed_name = record.bed_id.bed_type_id.name if record.bed_id else False
            record.patient_stat = record.bed_id.status
            record.discharge_date = record.bed_id.discharge_date
            record.admission_date = record.bed_id.admission_date

    # @api.model
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Generate Reference
            if not vals.get("ref") or vals["ref"] == "NEW":
                vals["ref"] = self.env["ir.sequence"].next_by_code("hospital.patient")

        return super(patients_data, self).create(vals_list)


class AccountMove(models.Model):
    _inherit = "account.move"

    patient_id = fields.Many2one("hospital.patient", string="Patient")
    my_name = fields.Char(string="My_Name")
    department_name = fields.Char(string="Department")


class ResPartner(models.Model):
    _inherit = "res.partner"
    department_name = fields.Char(string="Department")

    def test_notification_button(self):
        self.ensure_one()  # optional for safety
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("This is test notification"),
                "message": "Hello from smart button!",
                "type": "success",
                "sticky": False,
            },
        }
