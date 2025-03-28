from odoo import api, fields, models


class hospitalImage(models.Model):
    _name = "hospital.image"
    image_hos = fields.Image("Hospital Image")
