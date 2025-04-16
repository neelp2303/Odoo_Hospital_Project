from odoo import models, fields, api, _


class ResCompany(models.Model):
    _inherit = "res.company"

    hospital_report_layout = fields.Selection(
        [
            ("modern", "Modern"),
            ("classic", "Classic"),
            ("minimal", "Minimal"),
        ],
        string="Hospital Report Layout",
        default="modern",
    )
    hospital_report = fields.Char("Report_Layout_Name")
    report_image = fields.Image(string="Report Layout Image")


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


# -*- coding: utf-8 -*-
# wizard/patient_export_wizard.py

import base64
import io
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import xlsxwriter


class PatientExportWizard(models.TransientModel):
    _name = "hospital.patient.export.wizard"
    _description = "Patient Data Export Wizard"

    field_ids = fields.Many2many(
        "ir.model.fields",
        "patient_export_field_rel",
        "wizard_id",
        "field_id",
        string="Fields to Export",
        domain="[('model', '=', 'hospital.patient'), ('store', '=', True)]",
    )
    create_sheets = fields.Boolean(
        string="Create Sheet Per Patient",
        default=True,
        help="If checked, each patient record will be written on a new sheet",
    )
    export_data = fields.Binary("Download", readonly=True)
    export_filename = fields.Char("Export File Name", readonly=True)
    state = fields.Selection([("choose", "Choose"), ("get", "Get")], default="choose")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        model = self.env["ir.model"].search(
            [("model", "=", "hospital.patient")], limit=1
        )
        default_fields = self.env["ir.model.fields"].search(
            [
                ("model_id", "=", model.id),
                ("name", "in", ["name", "age", "ref", "gender"]),
            ]
        )
        res.update({"field_ids": [(6, 0, default_fields.ids)]})
        return res

    def action_export(self):
        self.ensure_one()
        if not self.field_ids:
            raise UserError(_("You must select at least one field to export."))

        active_ids = self.env.context.get("active_ids", [])
        if not active_ids:
            raise UserError(_("No patients selected."))

        patients = self.env["hospital.patient"].browse(active_ids)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)

        if self.create_sheets:
            for patient in patients:
                safe_sheet_name = f"{patient.name or patient.ref or patient.id}"[
                    :31
                ]  # XLSX sheet name max 31 chars
                sheet = workbook.add_worksheet(safe_sheet_name)

                # Write headers
                for col, field in enumerate(self.field_ids):
                    sheet.write(0, col, field.field_description or field.name)

                # Write patient data
                for col, field in enumerate(self.field_ids):
                    value = self._get_field_value(patient, field.name)
                    sheet.write(1, col, value)
        else:
            sheet = workbook.add_worksheet("Patients")
            for col, field in enumerate(self.field_ids):
                sheet.write(0, col, field.field_description or field.name)

            for row, patient in enumerate(patients, start=1):
                for col, field in enumerate(self.field_ids):
                    value = self._get_field_value(patient, field.name)
                    sheet.write(row, col, value)

        workbook.close()
        output.seek(0)
        export_file = base64.b64encode(output.read())
        output.close()

        self.write(
            {
                "state": "get",
                "export_data": export_file,
                "export_filename": "patient_export.xlsx",
            }
        )

        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "view_mode": "form",
            "res_id": self.id,
            "target": "new",
        }

    def _get_field_value(self, record, field_name):
        if not hasattr(record, field_name):
            return ""

        value = getattr(record, field_name)
        if isinstance(value, models.Model):
            return value.display_name or ""
        elif isinstance(value, (fields.Date, fields.Datetime)):
            return value.strftime("%Y-%m-%d %H:%M:%S") if value else ""
        return str(value or "")
