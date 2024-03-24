def get_total_income_month(username):
    data = core.read_data()
    total_income = 0
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                for activity in wallet["activity"]:
                    if activity["type"] == "Pemasukan":
                        total_income += int(activity["amount"])
    return total_income


def get_total_outcome_month(username):
    data = core.read_data()
    total_income = 0
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                for activity in wallet["activity"]:
                    if activity["type"] == "Pengeluaran":
                        total_income += int(activity["amount"])
    return total_income