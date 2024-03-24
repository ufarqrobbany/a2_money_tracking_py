from src import core
from src import wallet


def get_category(username, type):
    data = core.read_data()
    categories = []
    try:
        for user in data:
            if user["username"] == username:
                for wallet in user["wallet"]:
                    for activity in wallet["activity"]:
                            if activity["type"] == type:
                                category = activity["category"]
                                categories.append(category)
    except:
        return categories

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
    status = 0
    if type != "Transfer":
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
            for dompet in user["wallet"]:
                if dompet["id"] == wallet_id:
                    dompet["activity"].append(activity_data)
                    core.write_data(data)
                    if type == "Pemasukan":
                        status = wallet.add_balance(username, wallet_id, amount)
                    elif type == "Pengeluaran":
                        status = wallet.reduce_balance(username, wallet_id, amount)
                    else:
                        status_1 = wallet.reduce_balance(username, wallet_id, amount)
                        status_2 = wallet.add_balance(username, wallet_id_2, amount)
                        if status_1 == status_2 and status_1 == 0:
                            status = 0
                        else:
                            status = 1
                    return status
    return 1

