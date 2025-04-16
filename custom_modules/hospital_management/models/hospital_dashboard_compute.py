from odoo import models, fields, api
from datetime import datetime


class HospitalAppointment(models.Model):
    _inherit = "hospital.appointment"

    # KPI Fields
    today_appointments = fields.Integer(
        string="Today's Appointments", compute="_compute_kpi_values", store=False
    )
    patients_with_beds = fields.Integer(
        string="Patients with Beds", compute="_compute_kpi_values", store=False
    )
    pending_prescriptions = fields.Integer(
        string="Pending Prescriptions", compute="_compute_kpi_values", store=False
    )

    @api.depends("appointment_date", "status")
    def _compute_kpi_values(self):
        """Compute KPI values for dashboard"""
        for record in self:
            # Today's appointments
            today = fields.Date.today()
            today_appointments = self.search_count([("appointment_date", "=", today)])

            # Patients with beds
            patients_with_beds = self.env["hospital.patient"].search_count(
                [("has_bed", "=", True)]
            )

            # Pending prescriptions (appointments in ongoing status)
            pending_prescriptions = self.search_count([("status", "=", "ongoing")])

            record.today_appointments = today_appointments
            record.patients_with_beds = patients_with_beds
            record.pending_prescriptions = pending_prescriptions
