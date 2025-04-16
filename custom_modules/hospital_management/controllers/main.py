from odoo import http
from odoo.http import request


class HospitalPatientController(http.Controller):

    @http.route("/hospital/patients", type="http", auth="public", website=True)
    def list_patients(self, **kwargs):
        patients = request.env["hospital.patient"].sudo().search([])
        return request.render(
            "hospital_management.patient_list_template", {"patients": patients}
        )
