from odoo import models, fields


class HospitalSettings(models.TransientModel):
    _inherit = "res.config.settings"

    cancel_days = fields.Boolean(
        string="Enable Cancellation", config_parameter="hospital_management.cancel_days"
    )
    send_mail = fields.Boolean(
        "Enable Mail Sending on Appointment Booking",
        config_parameter="hospital_management.send_mail",
    )
