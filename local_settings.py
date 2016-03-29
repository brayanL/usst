#Este es mi Archivo Siiii
DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "c0ql12d#q%z&y_it#&kahkd)**2_ly&^dujxs6q#d=vl4cc=c^"
NEVERCACHE_KEY = "50f77f85-3e1e-428a-bdd1-e8f8532e996cf574c551-89f8-4487-ab5b-326bdfadcd815f2a3635-ff43-4ee7-af0c-b1470976cf12"

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        "NAME": "usst_db",
        "USER": "user1",
        "PASSWORD": "admin",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
