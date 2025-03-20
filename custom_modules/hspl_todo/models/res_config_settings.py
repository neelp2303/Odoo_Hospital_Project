from odoo import models, fields


class hspl_todo(models.TransientModel):
    _inherit = "res.config.settings"

    cancel_days = fields.Boolean(string="Enable Cancellation")
