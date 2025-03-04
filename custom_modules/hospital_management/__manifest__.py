{
    "name": "Hospital Management",
    "description": """A Hospital Management app from Heliconia Solutions""",
    "summary": "A simple Hospital Management app",
    "version": "0.0.0",
    "category": "Health and Fitness",
    "sequence": 0,
    "website": "https://www.heliconia.io",
    "author": "Neel Patel (Heliconia Solutions Pvt. Ltd.), ",
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/patient_data.xml",
        "views/doctor_data.xml",
        "views/appointments_data.xml",
        "views/conference_data.xml",
        "views/beds_data.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
