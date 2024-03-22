import json
from datetime import datetime

curr = datetime.now()

def record_income(username, id_wallet, category, amount):
    file_name = "data/data.json"

    try:
        with open(file_name, "r+") as file:
            data = json.load(file)
            for user in data:
                if user.get("username") == username:
                    wallets = user.get("wallet", [])
                    for wallet in wallets:
                        if wallet.get("id") == id_wallet:
                            activities = wallet.get("actitivy", [])
                            activity = {
                                "id": len(activities) + 1,
                                "waktu": str(curr),
                                "jenis": "Pemasukan",
                                "kategori": category,
                                "nominal": amount
                            }
                            activities.append(activity)
                            # Update balance
                            wallet["saldo"] += amount
                            file.seek(0)
                            json.dump(data, file, indent=4)
                            file.truncate()
                            print("Income activity recorded successfully.")
                            return
                    print("\nDompet dengan ID yang diberikan tidak ditemukan\n")
                    return
            print("\nUsername tidak ditemukan\n")
    except FileNotFoundError:
        print("\nGagal membuka file dompet\n")
    except json.JSONDecodeError:
        print("\nFile dompet tidak valid (JSON tidak valid)\n")
    except Exception as e:
        print(f"\nError: {str(e)}\n")


def record_outcome(username, id_wallet, category, amount):
    file_name = "data/data.json"

    try:
        with open(file_name, "r+") as file:
            data = json.load(file)
            for user in data:
                if user.get("username") == username:
                    wallets = user.get("wallet", [])
                    for wallet in wallets:
                        if wallet.get("id") == id_wallet:
                            activities = wallet.get("actitivy", [])
                            activity = {
                                "id": len(activities) + 1,
                                "waktu": str(curr),
                                "jenis": "Pengeluaran",
                                "kategori": category,
                                "nominal": amount
                            }
                            activities.append(activity)
                            # Update balance
                            wallet["saldo"] -= amount
                            file.seek(0)
                            json.dump(data, file, indent=4)
                            file.truncate()
                            print("Outcome activity recorded successfully.")
                            return
                    print("\nDompet dengan ID yang diberikan tidak ditemukan\n")
                    return
            print("\nUsername tidak ditemukan\n")
    except FileNotFoundError:
        print("\nGagal membuka file dompet\n")
    except json.JSONDecodeError:
        print("\nFile dompet tidak valid (JSON tidak valid)\n")
    except Exception as e:
        print(f"\nError: {str(e)}\n")