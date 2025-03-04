from odoo import models, fields, api


class HospitalBedType(models.Model):
    _name = "hospital.bed.type"
    _description = "Hospital Bed Type"
    price_per_day = fields.Float("Price per Day")
    name = fields.Char("Bed Type", required=True)
    total_beds = fields.Integer("Total Beds", required=True, default=0)
    

    


