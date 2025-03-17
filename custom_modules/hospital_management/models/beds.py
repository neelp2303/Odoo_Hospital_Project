from odoo import models, fields, api


class HospitalBedType(models.Model):
    _name = "hospital.bed.type"
    _description = "Hospital Bed Type"
    price_per_day = fields.Float("Price per Day")
    name = fields.Char("Bed Type", required=True)
    total_beds = fields.Integer("Total Beds", required=True, default=0)
    occupied_beds = fields.Integer(
        "Occupied Beds", compute="_compute_occupied_beds", store=True
    )
    available_beds = fields.Integer(
        "Available Beds", compute="_compute_available_beds", store=True
    )

    bed_ids = fields.One2many("hospital.bed", "bed_type_id", string="Beds")
    patient_ids = fields.One2many(
        "hospital.patient", compute="_compute_patient_ids", string="Admitted Patients"
    )

    @api.depends("bed_ids.patient_id")
    def _compute_patient_ids(self):
        """Find all patients who have booked a bed of this type"""
        for record in self:
            record.patient_ids = record.bed_ids.mapped("patient_id")

    @api.depends("bed_ids.status")
    def _compute_occupied_beds(self):
        """Calculate occupied beds based on assigned patients"""
        for record in self:
            record.occupied_beds = len(
                record.bed_ids.filtered(lambda b: b.status == "occupied")
            )

    @api.depends("total_beds", "occupied_beds")
    def _compute_available_beds(self):
        """Calculate available beds"""
        for record in self:
            record.available_beds = record.total_beds - record.occupied_beds

    def action_view_admitted_patients(self):
        """Opens the admitted patients list"""
        return {
            "name": "Admitted Patients",
            "type": "ir.actions.act_window",
            "res_model": "hospital.patient",
            "view_mode": "list,form",
            "domain": [("id", "in", self.patient_ids.ids)],
        }


class HospitalBed(models.Model):
    _name = "hospital.bed"
    _description = "Hospital Bed Management"

    price_per_day = fields.Float(
        string="Price per Day",
        related="bed_type_id.price_per_day",
        store=True,
        readonly=True,
    )
    bed_type_id = fields.Many2one("hospital.bed.type", string="Bed Type", required=True)

    status = fields.Selection(
        [
            ("available", "Available"),
            ("occupied", "Occupied"),
        ],
        string="Status",
        default="occupied",
    )

    patient_id = fields.Many2one(
        "hospital.patient", string="Assigned Patient", domain=[("has_bed", "=", False)]
    )

    @api.onchange("patient_id")
    def _onchange_patient_id(self):
        """Automatically update the patient's booked bed when assigned"""
        for bed in self:
            if bed.patient_id:
                # Update patient's bed_id
                bed.patient_id.has_bed = True  # Set has_bed = True
