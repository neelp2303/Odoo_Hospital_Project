from odoo import models, fields, api


class MyReportLayout(models.Model):
    _name = "hospital.reports"
    _description = "Report Models"
    _rec_name = "hospital_report_layout"

    image = fields.Image("Layout image")
    hospital_report_layout = fields.Selection(
        [
            ("modern", "Modern"),
            ("classic", "Classic"),
            ("minimal", "Minimal"),
        ],
        string="Hospital Report Layout",
        default="modern",
    )
