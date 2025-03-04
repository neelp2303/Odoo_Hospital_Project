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
        "hospital.patient", string="Assigned Patient", domain=[("bed_id", "=", False)]
    )

    @api.onchange("patient_id")
    def _onchange_patient_id(self):
        """Mark bed as occupied & update available count"""
        for bed in self:
            if bed.patient_id:
                bed.status = "occupied"
            else:
                bed.status = "available"

        # Update bed type counts
        if self.bed_type_id:
            self.bed_type_id._compute_occupied_beds()
            self.bed_type_id._compute_available_beds()
