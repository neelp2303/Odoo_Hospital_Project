from odoo import models, fields, api, _


class HospitalDashboard(models.Model):
    _name = "hospital.dashboard"
    _description = "Hospital Dashboard"
    _auto = False

    # Fields from hospital.appointment
    patient_id = fields.Many2one("hospital.patient", string="Patient")
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor")
    appointment_date = fields.Date("Appointment Date")
    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("ongoing", "Ongoing"),
            ("done", "Done"),
            ("canceled", "Canceled"),
        ],
        string="Status",
    )

    # Fields from hospital.patient
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")
    age = fields.Integer("Age")
    has_bed = fields.Boolean("Has Bed")
    bed_name = fields.Char("Bed Type")
    patient_stat = fields.Char("Patient Status")

    # Metrics fields
    appointment_count = fields.Integer("Appointment Count")

    @api.model
    def init(self):
        # Let's verify the fields in hospital_appointment table first
        self._cr.execute(
            """
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'hospital_appointment'
        """
        )
        columns = [row[0] for row in self._cr.fetchall()]

        # Base query - we'll include fields dynamically based on what's available
        base_query = """
            CREATE OR REPLACE VIEW hospital_dashboard AS (
                SELECT
                    a.id,
                    a.patient_id,
                    a.doctor_id,
                    a.appointment_date,
                    a.status,
                    p.gender,
                    p.age,
                    p.has_bed,
                    p.bed_name,
                    p.patient_stat,
                    1 as appointment_count
                FROM
                    hospital_appointment a
                JOIN
                    hospital_patient p ON a.patient_id = p.id
            )
        """

        self._cr.execute(base_query)
