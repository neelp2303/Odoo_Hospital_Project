/** @odoo-module */
import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class HospitalDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            total_doctors: 0,
            total_patients: 0,
            total_appointments_today: 0,
            total_appointments_week: 0,
            upcoming_appointments: [],
            new_patients: [],
        });

        onWillStart(async () => {
            const [
                totalDoctors,
                totalPatients,
                totalAppointmentsToday,
                totalAppointmentsWeek,
                upcomingAppointments,
                newPatients
            ] = await Promise.all([
                this.orm.call("hospital.doctor", "search_count", [[]]),
                this.orm.call("hospital.patient", "search_count", [[]]),
                this.orm.call("hospital.appointment", "search_count", [[["appointment_date", "=", new Date().toISOString().slice(0, 10)]]]),
                this.orm.call("hospital.appointment", "search_count", [[["appointment_date", ">=", new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().slice(0, 10)]]]),
                this.orm.call("hospital.appointment", "search_read", [[], ["patient_id", "doctor_id", "appointment_date"], 5]),
                this.orm.call("hospital.patient", "search_read", [[], ["name", "age", "gender"], 5]),
            ]);

            this.state.total_doctors = totalDoctors;
            this.state.total_patients = totalPatients;
            this.state.total_appointments_today = totalAppointmentsToday;
            this.state.total_appointments_week = totalAppointmentsWeek;
            this.state.upcoming_appointments = upcomingAppointments;
            this.state.new_patients = newPatients;
        });
    }
}

HospitalDashboard.template = "hospital_dashboard.dashboard";
registry.category("actions").add("hospital_dashboard.dashboard", HospitalDashboard);
