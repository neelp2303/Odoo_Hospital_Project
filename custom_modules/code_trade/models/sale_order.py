from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"
    project_name = fields.Char(string="Project Name")

    def action_open_add_line_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Add Sale Order Line",
            "res_model": "code.trade.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_order_id": self.id,
            },
        }

    def action_quotation_send(self):
        res = super(SaleOrder, self).action_quotation_send()
        if res.get("context") and self.project_name:
            new_subject = f"{self.name} ({self.project_name})"
            res["context"].update({"default_subject": new_subject})
        return res
