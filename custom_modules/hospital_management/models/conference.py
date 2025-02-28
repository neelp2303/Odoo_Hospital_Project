from odoo import models, fields


class Conference(models.Model):
    _name = "hospital.conference"
    _description = "Medical Conferences"

    name = fields.Char("Conference Name", required=True)
    date = fields.Date("Conference Date")
    doctor_ids = fields.Many2many("hospital.doctor", string="Attending Doctors")
