from odoo import models, fields, api


class PatientMassEditWizard(models.TransientModel):
    _name = "hospital.patient.mass.edit.wizard"
    _description = "Mass Edit Patients"

    # Fields that can be mass edited

    doctor_id = fields.Many2one("hospital.doctor", string="Doctor")

    address = fields.Text("Address")

    # Field to determine whether to set this value

    update_doctor = fields.Boolean("Update Doctor")

    update_address = fields.Boolean("Update Address")

    # For display/information only
    patient_count = fields.Integer("Number of Patients", readonly=True)

    @api.model
    def default_get(self, fields):
        """Initialize with information about selected records"""
        res = super().default_get(fields)
        active_ids = self.env.context.get("active_ids", [])
        res["patient_count"] = len(active_ids)
        return res

    def action_apply(self):
        """Apply the changes to all selected patients"""
        active_ids = self.env.context.get("active_ids", [])
        patients = self.env["hospital.patient"].browse(active_ids)

        # Prepare values dictionary based on selected checkboxes
        values = {}
        changes_summary = []

        if self.update_doctor and self.doctor_id:
            values["doctor_id"] = self.doctor_id.id
            changes_summary.append(f"Doctor: {self.doctor_id.name}")

        if self.update_address and self.address:
            values["address"] = self.address
            changes_summary.append(f"Address: {self.address}")

        # Only apply if we have values to update
        if values:
            # Turn off tracking temporarily to avoid automatic tracking messages
            # Store the current tracking status of each field

            # Write the values without automatic tracking
            patients.write(values)

            # Create a single properly formatted message about the mass update

            # Restore tracking settings

        return {"type": "ir.actions.act_window_close"}
