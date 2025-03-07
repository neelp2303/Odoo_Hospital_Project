from odoo import models, fields, api


class Conference(models.Model):
    _name = "hospital.conference"
    _description = "Medical Conferences"

    name = fields.Char("Conference Name", required=True)
    date = fields.Date("Conference Date")
    doctor_ids = fields.Many2many("hospital.doctor", string="Attending Doctors")
    doctor_count = fields.Integer(
        string="Doctor Count", compute="_compute_doctor_count"
    )

    @api.depends("doctor_ids")
    def _compute_doctor_count(self):
        for record in self:
            record.doctor_count = len(record.doctor_ids)

    def action_attending_doctors(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Attending Doctors",
            "res_model": "hospital.doctor",
            "view_mode": "list,form",
            "domain": [("id", "in", self.doctor_ids.ids)],
            "target": "current",
        }
