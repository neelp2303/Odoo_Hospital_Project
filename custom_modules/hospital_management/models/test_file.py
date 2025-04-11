from odoo import models, fields, api, _


class ResCompany(models.Model):
    _inherit = "res.company"

    hospital_report_layout = fields.Selection(
        [
            ("modern", "Modern"),
            ("classic", "Classic"),
            ("minimal", "Minimal"),
        ],
        string="Hospital Report Layout",
        default="modern",
    )
    hospital_report = fields.Char("Report_Layout_Name")
    report_image = fields.Image(string="Report Layout Image")


class TestFile(models.Model):
    _name = "test.file"
    _description = "Test"
    # _inherits = "res.partner"
    # _inherit = ["res.partner"]
    _inherits = {"res.partner": "partner_id"}
    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True, ondelete="cascade"
    )

    # name = fields.Char("Name", required=True)
    def test_notification(self):

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("This is test notification"),
                "sticky": False,
            },
        }

    @api.model
    def test_action(self):
        print("Test Action")
