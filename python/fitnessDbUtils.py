"""
fitnessDbUtils.py

Description:
    Module description
"""


# ==============================================================================
# Constants/Globals
# ==============================================================================
DB_TABLES = ["person",
             "client",
             "account",
             "bodyWeight",
             "measurement",
             "exercise",
             "active_set",
             "workout"]


def insert(table, **data):
    columns = []
    values = []
    for k, v in data.iteritems():
        columns.append(k)
        if isinstance(v, basestring):
            v = "{0!r}".format(v)
        values.append(v)
    columns = ", ".join(columns)
    values = ", ".join(values)
    stmnt = "INSERT INTO {0} ({1})\nVALUES ({2});".format(table, columns, values)
    print(stmnt)

data = {"first_name": "paul",
        "last_name": "katzen",
        "street_number": " 1746",
        "street_name": "9th street",
        "apt_num": "3C",
        "city": "Santa Monica",
        "state": "CA",
        "zipcode": "90404",
        "e_mail": "pkatzen@gmail.com"}
insert("person", **data)
