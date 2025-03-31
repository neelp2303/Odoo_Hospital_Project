from odoo import models, fields, api, _


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
