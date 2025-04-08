import xmlrpc.client

url = "http://localhost:8069"
db = "odoo-18"
username = "odoohospital@gmail.com"
password = "8589f95820e27e9c04739a4c6e907e7b3471220f"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

if not uid:
    raise Exception("Authentication Failed. Check credentials!")

print(f"Authenticated as UID: {uid}")

models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# Get some partner records
partners = models.execute_kw(
    db,
    uid,
    password,
    "hospital.patient",
    "search_read",
    [],
    {"fields": ["name", "email"]},
)

for partner in partners:
    print(partner)
print("----------------------------------------")
customers = models.execute_kw(
    db,
    uid,
    password,
    "res.partner",
    "search_read",
    [],
    {"fields": ["name", "email"]},
)

for customer in customers:
    print(customer)
