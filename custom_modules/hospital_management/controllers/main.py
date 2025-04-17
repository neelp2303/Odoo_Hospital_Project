from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
from datetime import date


class HospitalPatientController(http.Controller):

    @http.route("/hospital/patients", type="http", auth="public", website=True)
    def list_patients(self, **kwargs):
        patients = request.env["hospital.patient"].sudo().search([])
        return request.render(
            "hospital_management.patient_list_template", {"patients": patients}
        )

    @http.route(["/appointments"], type="http", auth="public", website=True)
    def appointment_list(self, **kw):
        appointments = request.env["hospital.appointment"].sudo().search([])
        return request.render(
            "hospital_management.website_appointment_list",
            {"appointments": appointments},
        )

    @http.route(["/appointments/book"], type="http", auth="public", website=True)
    def appointment_form(self, **kw):
        doctors = request.env["hospital.doctor"].sudo().search([])
        patients = request.env["hospital.patient"].sudo().search([])
        default_date = date.today().strftime("%Y-%m-%d")
        slots = (
            request.env["hospital.appointment.slot"]
            .sudo()
            .search(
                [
                    ("date", "=", default_date),
                    ("is_booked", "=", False),
                ]
            )
        )

        return request.render(
            "hospital_management.website_appointment_form",
            {
                "doctors": doctors,
                "patients": patients,
                "default_date": default_date,
                "slots": slots,
            },
        )

    @http.route("/appointments/get_slots", type="json", auth="public", csrf=False)
    def get_available_slots(self, doctor_id, appointment_date):
        print("==> get_available_slots CALLED", doctor_id, appointment_date)
        slots = (
            request.env["hospital.appointment.slot"]
            .sudo()
            .search(
                [
                    ("doctor_id", "=", int(doctor_id)),
                    ("date", "=", appointment_date),
                    ("is_booked", "=", False),
                ]
            )
        )
        return [{"id": slot.id, "name": slot.display_name} for slot in slots]

    @http.route(
        ["/appointments/book/submit"],
        type="http",
        auth="public",
        website=True,
        methods=["POST"],
    )
    def appointment_submit(self, **post):
        try:
            request.env["hospital.appointment"].sudo().create(
                {
                    "patient_id": int(post.get("patient_id")),
                    "doctor_id": int(post.get("doctor_id")),
                    "appointment_date": post.get("appointment_date"),
                    "slots": int(post.get("slots")),  # Include time slot here
                }
            )
        except (ValidationError, Exception) as e:
            return request.render(
                "hospital_management.website_appointment_form",
                {
                    "error": str(e),
                    "doctors": request.env["hospital.doctor"].sudo().search([]),
                    "patients": request.env["hospital.patient"].sudo().search([]),
                    "slots": request.env["hospital.appointment.slot"]
                    .sudo()
                    .search(
                        [
                            ("is_booked", "=", False),
                        ]
                    ),
                },
            )
        return request.redirect("/appointments")
