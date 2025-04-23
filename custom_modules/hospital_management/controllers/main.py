from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
from datetime import date
from werkzeug.exceptions import NotFound
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager


class HospitalPatientController(http.Controller):

    @http.route("/hospital/patients", type="http", auth="public", website=True)
    def list_patients(self, **kwargs):
        patients = request.env["hospital.patient"].sudo().search([])
        return request.render(
            "hospital_management.patient_list_template", {"patients": patients}
        )

    @http.route(
        ["/appointments", "/appointments/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
    )
    def appointment_list(self, page=1, **kw):
        appointments_obj = request.env["hospital.appointment"].sudo()
        total = appointments_obj.search_count([])

        pager = portal_pager(
            url="/appointments",
            total=total,
            page=page,
            step=2,  # Only 2 appointments per page
        )

        appointments = appointments_obj.search([], limit=2, offset=pager["offset"])

        return request.render(
            "hospital_management.website_appointment_list",
            {
                "appointments": appointments,
                "pager": pager,
            },
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
                    "slot_id": int(post.get("slots")),  # Include time slot here
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

    # @http.route("/", auth="user", website=True)
    # def home_redirect(self, **kw):
    #     # Redirect to backend instead of website
    #     return request.redirect("/odoo")

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        patient = request.env["hospital.patient"].search(
            [("partner_id", "=", request.env.user.partner_id.id)], limit=1
        )

        if patient:
            appointments = request.env["hospital.appointment"].search_count(
                [("patient_id", "=", patient.id)]
            )
            values["appointments_count"] = appointments
        return values

    @http.route(
        ["/my/appointments", "/my/appointments/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_appointments(self, page=1, **kwargs):
        if not request.env.user.has_group("base.group_portal"):
            raise NotFound()

        patient = request.env["hospital.patient"].search(
            [("partner_id", "=", request.env.user.partner_id.id)], limit=1
        )

        domain = [("patient_id", "=", patient.id)]
        appointments_obj = request.env["hospital.appointment"].sudo()
        total = appointments_obj.search_count(domain)

        pager = portal_pager(
            url="/my/appointments",
            total=total,
            page=page,
            step=2,
        )

        appointments = appointments_obj.search(domain, limit=2, offset=pager["offset"])

        return request.render(
            "hospital_management.portal_my_appointments",
            {
                "appointments": appointments,
                "pager": pager,
                "page_name": "appointments",
            },
        )
