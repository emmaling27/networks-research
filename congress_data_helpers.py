
def get_last_name(row):
    return row['name'].split(",")[0].split(" ")[0].lower(), row['party']

def last_name(name):
    return name.split(",")[0].split(" ")[0].lower()