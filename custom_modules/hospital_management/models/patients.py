from odoo import models, fields

class patients_data(models.Model):
    _name='hospital.patient'
    _description='Patients Data'
    
    name = fields.Char('Name', required=True)
    age = fields.Integer('Age')
    gender = fields.Selection([('male','Male'),('female','Female'),('other','Other')], 'Gender')
    dob=fields.Date('Dob')
    contact_number = fields.Char('Contact Number')
    address = fields.Text('Address')
    medical_history = fields.Text('Medical History')
    allergies = fields.Text('Allergies')
    medications = fields.Text('Medications')
    prescriptions = fields.Text('Prescriptions')
    symptoms = fields.Text('Symptoms')
    diagnosis = fields.Text('Diagnosis')
    treatment_plan = fields.Text('Treatment Plan')
    admission_date = fields.Date('Admission Date')
    discharge_date = fields.Date('Discharge Date')
    doctor_name = fields.Char('Doctor Name')
    room_number = fields.Char('Room Number')
    bed_number = fields.Char('Bed Number')
    patient_id = fields.Char('Patient ID', required=True, default=lambda self: self._generate_patient_id())
    
    @staticmethod
    def _generate_patient_id():
        sequence = 'patient_id'
        next_id = 1
        for record in models.env['hospital.patient'].search([('patient_id', 'like', f'{sequence}%')]):
            sequence_number = int(record.patient_id.split('_')[-1])
            next_id = max(next_id, sequence_number + 1)
        return f'{sequence}_{next_id:04d}'
    
    def action_view_patient_details(self):
        action = self.env.ref('hospital_management.action_patient_details_view').read()[0]
        action['domain'] = [('id', 'in', self.ids)]
        return action