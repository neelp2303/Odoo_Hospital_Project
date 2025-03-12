from odoo import models, fields


class HospitalSettings(models.TransientModel):
    _inherit = "res.config.settings"

    cancel_days = fields.Integer(string="Cancel Days")
