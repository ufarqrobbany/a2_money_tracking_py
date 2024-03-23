from src import core

def get_category(username, type):
    data = core.read_data()
    categories = []
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                for activity in wallet["activity"]:
                    if activity["type"] == type:
                        category = activity["category"]
                        categories.append(category)

    unique_categories = sorted(set(categories))
    return unique_categories

def get_last_activity_id(username, wallet_id):
    data = core.read_data()
    activity_id = 0
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                if wallet["id"] == wallet_id:
                    for activity in wallet["activity"]:
                        activity_id = activity["id"]
    return activity_id

def add_record(username, amount, category, wallet_id, date, time, note, type, wallet_id_2=0):
    data = core.read_data()
    activity_id = get_last_activity_id(username, wallet_id) + 1
    if type == "Transfer":
        activity_data = {
            "id": activity_id,
            "datetime": f"{date} {time}",
            "type": type,
            "category": category,
            "amount": amount,
            "note": note,
            "wallet_id": wallet_id,
        }
    else:
        activity_data = {
            "id": activity_id,
            "datetime": f"{date} {time}",
            "type": type,
            "amount": amount,
            "note": note,
            "source_wallet_id": wallet_id,
            "destination_wallet_id": wallet_id_2
        }
    for user in data:
        if user["username"] == username:
            for wallet in user["wallet"]:
                if wallet["id"] == wallet_id:
                    wallet["activity"].append(activity_data)
                    core.write_data(data)
                    if type == "Pemasukan":
                        wallet.add_balance(username, wallet_id, amount)
                    elif type == "Pengeluaran":
                        wallet.reduce_balance(username, wallet_id, amount)
                    else:
                        wallet.reduce_balance(username, wallet_id, amount)
                        wallet.add_balance(username, wallet_id_2, amount)
                    return 0
    return 1