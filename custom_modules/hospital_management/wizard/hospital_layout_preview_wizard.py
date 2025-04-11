from odoo import models, fields, api
from odoo.exceptions import UserError


class HospitalLayoutPreviewWizard(models.TransientModel):
    _name = "hospital.layout.preview.wizard"
    _description = "Preview Hospital Report Layout"

    _inherit = "res.config.settings"

    # hospital_report_layout = fields.Selection(
    #     string="Hospital Report Layout",
    #     related="company_id.hospital_report_layout",
    #     readonly=False,
    # )
    hospital_report_layout = fields.Many2one("hospital.reports", string="Report Layout")

    report_image = fields.Image(
        "hospital.reports",
        related="hospital_report_layout.image",
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

    def action_confirm_layout(self):
        if self.hospital_report_layout:
            self.company_id.hospital_report_layout = (
                self.hospital_report_layout.hospital_report_layout
            )

        return {"type": "ir.actions.act_window_close"}

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        layout_key = self.env.company.hospital_report_layout
        if layout_key:
            report = self.env["hospital.reports"].search(
                [("hospital_report_layout", "=", layout_key)], limit=1
            )
            res["hospital_report_layout"] = report.id
        return res
