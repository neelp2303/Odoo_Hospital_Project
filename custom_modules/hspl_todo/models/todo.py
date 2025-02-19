from odoo import models, fields


class todo(models.Model):

    _name = "hspl.todo"
    _description = "Heliconia Todo"

    name = fields.Char("Name", required=True)
    done = fields.Boolean()
