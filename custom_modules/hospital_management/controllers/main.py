# -*- coding: utf-8 -*-
# controllers/main.py

import base64
from odoo import http
from odoo.http import request, content_disposition


class PatientExportController(http.Controller):
    @http.route("/web/hospital/export_csv", type="http", auth="user")
    def export_csv(self, wizard_id, **kw):
        wizard = request.env["hospital.patient.export.wizard"].browse(int(wizard_id))

        if not wizard or not wizard.export_data:
            return request.not_found()

        # Decode the data
        csv_content = base64.b64decode(wizard.export_data)

        # Return with proper headers to ensure it's recognized as CSV
        return request.make_response(
            csv_content,
            headers=[
                ("Content-Type", "text/csv; charset=utf-8"),
                ("Content-Disposition", content_disposition(wizard.export_filename)),
                ("Content-Length", len(csv_content)),
            ],
        )
