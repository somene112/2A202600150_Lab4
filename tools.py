from langchain_core.tools import tool
import json

# ================= MOCK DATA =================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],

    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],

    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],

    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],

    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],

    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],

    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}


# ================= TOOL 1 =================
@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm chuyến bay
    """
    try:
        flights = FLIGHTS_DB.get((origin, destination)) or FLIGHTS_DB.get((destination, origin))

        if not flights:
            return json.dumps({
                "raw": [],
                "formatted": f"Không tìm thấy chuyến bay từ {origin} đến {destination}"
            }, ensure_ascii=False)

        formatted = "Danh sách chuyến bay:\n"
        for f in flights:
            price = f"{f['price']:,}".replace(",", ".")
            formatted += f"- {f['airline']} | {f['departure']} → {f['arrival']} | {price}đ\n"

        return json.dumps({
            "raw": flights,
            "formatted": formatted
        }, ensure_ascii=False)

    except:
        return json.dumps({"raw": [], "formatted": "Lỗi"}, ensure_ascii=False)


# ================= TOOL 2 =================
@tool
def search_hotels(city: str, max_price_per_night: int = 9999999) -> str:
    """
    Tìm khách sạn
    """
    try:
        hotels = HOTELS_DB.get(city, [])

        filtered = [h for h in hotels if h["price_per_night"] <= max_price_per_night]

        if not filtered:
            price = f"{max_price_per_night:,}".replace(",", ".")
            return json.dumps({
                "raw": [],
                "formatted": f"Không tìm thấy khách sạn tại {city} với giá dưới {price}đ/đêm"
            }, ensure_ascii=False)

        filtered.sort(key=lambda x: x["rating"], reverse=True)

        formatted = "Khách sạn gợi ý:\n"
        for h in filtered:
            price = f"{h['price_per_night']:,}".replace(",", ".")
            formatted += f"- {h['name']} | {h['rating']} | {price}đ/đêm\n"

        return json.dumps({
            "raw": filtered,
            "formatted": formatted
        }, ensure_ascii=False)

    except:
        return json.dumps({"raw": [], "formatted": "Lỗi"}, ensure_ascii=False)


# ================= TOOL 3 =================
@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách dựa trên các khoản chi.
    
    Args:
        total_budget: Tổng ngân sách
        expenses: Chuỗi dạng 'vé:1000000,khách sạn:500000'
    
    Returns:
        Báo cáo chi phí và số tiền còn lại
    """
    try:
        items = expenses.split(",")
        expense_dict = {}

        for item in items:
            name, value = item.split(":")
            expense_dict[name.strip()] = int(value.strip())

        total = sum(expense_dict.values())
        remaining = total_budget - total

        result = "Chi tiết chi phí:\n"
        for k, v in expense_dict.items():
            price = f"{v:,}".replace(",", ".")
            result += f"- {k}: {price}đ\n"

        result += "----\n"
        result += f"Tổng chi: {total:,}".replace(",", ".") + "đ\n"
        result += f"Ngân sách: {total_budget:,}".replace(",", ".") + "đ\n"

        if remaining < 0:
            result += f"Vượt ngân sách {(-remaining):,}".replace(",", ".") + "đ"
        else:
            result += f"Còn lại: {remaining:,}".replace(",", ".") + "đ"

        return result

    except Exception:
        return "Lỗi format. Đúng: 'vé:1000000,khách sạn:500000'"