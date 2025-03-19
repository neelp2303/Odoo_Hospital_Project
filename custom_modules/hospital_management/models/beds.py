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
                record.bed_ids.filtered(lambda b: b.status == "admitted")
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
    room_number = fields.Char(
        string="Room Number", compute="_compute_room_number", readonly=True
    )

    status = fields.Selection(
        [
            ("admitted", "Admitted"),
            ("discharged", "Discharged"),
        ],
        string="Status",
        default="admitted",
    )

    patient_id = fields.Many2one(
        "hospital.patient", string="Assigned Patient", domain=[("has_bed", "=", False)]
    )
    admission_date = fields.Datetime(default=fields.Datetime.now)
    discharge_date = fields.Datetime()
    invoice_id = fields.Many2one("account.move", string="Invoice", readonly=True)

    @api.onchange("patient_id", "bed_type_id", "status", "admission_date")
    def _onchange_patient_id(self):
        """Automatically update the patient's booked bed when assigned"""
        for bed in self:
            if bed.patient_id:
                bed.patient_id.has_bed = True
                bed.patient_id.bed_name = bed.bed_type_id.name
                bed.patient_id.patient_stat = bed.status
                bed.patient_id.admission_date = bed.admission_date

            if bed.status == "discharged":
                current_date = fields.Datetime.now()
                bed.patient_id.discharge_date = current_date
                bed.discharge_date = current_date
                bed.patient_id.has_bed = False

                # Generate an invoice
                bed._create_invoice()

    def _create_invoice(self):
        for bed in self:
            if not bed.patient_id.partner_id:
                # Automatically create a linked customer
                partner = self.env["res.partner"].create(
                    {
                        "name": bed.patient_id.name,
                        "customer_rank": 1,  # Mark as customer
                    }
                )
                bed.patient_id.partner_id = partner
        """Creates an invoice for the patient based on bed stay duration"""
        for bed in self:
            if not bed.patient_id or not bed.bed_type_id:
                return

            if not bed.admission_date or not bed.discharge_date:
                raise ValueError("Missing admission or discharge date!")

            # ✅ Ensure the patient has a linked customer (partner)
            partner = bed.patient_id.partner_id
            if not partner:
                raise ValueError(
                    f"Patient {bed.patient_id.name} does not have a linked customer!"
                )

            admission_dt = fields.Datetime.from_string(bed.admission_date)
            discharge_dt = fields.Datetime.from_string(bed.discharge_date)
            num_days = (discharge_dt - admission_dt).days or 1  # Minimum 1 day charge

            total_price = num_days * bed.price_per_day

            # ✅ Explicitly set partner_id (Odoo requires this)
            invoice_vals = {
                "move_type": "out_invoice",
                "partner_id": partner.id,  # ✅ Required by Odoo
                "patient_id": bed.patient_id.id,  # ✅ Custom field
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": f"Bed Stay: {bed.bed_type_id.name} ({num_days} days)",
                            "quantity": num_days,
                            "price_unit": bed.price_per_day,
                            "price_subtotal": total_price,
                        },
                    )
                ],
                # "amount_total": total_price,
            }

            invoice = self.env["account.move"].create(invoice_vals)
            bed.invoice_id = invoice.id

            return {
                "name": "Invoice",
                "type": "ir.actions.act_window",
                "res_model": "account.move",
                "view_mode": "form",
                "res_id": invoice.id,
            }

    def unlink(self):
        """Ensure that deleting a bed updates the patient's has_bed field"""
        for bed in self:
            if bed.patient_id:
                bed.patient_id.bed_id = False
                bed.patient_id.has_bed = False
        return super(HospitalBed, self).unlink()
