from odoo import models, fields


class HospitalLayoutPreviewWizard(models.TransientModel):
    _name = "hospital.layout.preview.wizard"
    _description = "Preview Hospital Report Layout"

    _inherit = "res.config.settings"
    hospital_report_layout = fields.Selection(
        [
            ("modern", "Modern"),
            ("classic", "Classic"),
            ("minimal", "Minimal"),
        ],
        string="Hospital Report Layout",
        related="company_id.hospital_report_layout",
        readonly=False,
    )

    def action_preview_report(self):
        dummy_patient = self.env["hospital.patient"].search([], limit=1)
        if not dummy_patient:
            raise UserError("No patient found to preview. Please create one.")

        return {
            "type": "ir.actions.report",
            "report_name": "hospital_management.report_patient_appointments",
            "report_type": "qweb-html",
            "context": {
                "active_model": "hospital.patient",
                "active_ids": [dummy_patient.id],
                "company": self.env.company,  # <-- Add this line
            },
        }
