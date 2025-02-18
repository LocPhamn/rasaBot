from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from sqlalchemy import create_engine, text

# Sử dụng kết nối MySQL từ tracker_store
DB_URI = "mysql+mysqlconnector://root:Locpro%401997@localhost:3306/rasa_data"

# Tạo engine kết nối database
engine = create_engine(DB_URI)

class ActionRecommendLaptop(Action):
    def name(self):
        return "action_recommend_laptop"

    def run(self, dispatcher, tracker, domain):
        # Lấy dữ liệu từ slots
        category = tracker.get_slot("category")
        price = tracker.get_slot("price")
        ram = tracker.get_slot("ram")
        screen_size = tracker.get_slot("screen_size")

        # Tạo câu truy vấn động dựa trên entities
        query = "SELECT brand, model, price FROM laptops WHERE 1=1"
        params = {}

        if category:
            query += " AND category = :category"
            params["category"] = category
        if price:
            price_value = float(price.replace(" triệu", "")) * 1000000  # Chuyển "triệu" thành VND
            query += " AND price <= :price"
            params["price"] = price_value
        if ram:
            query += " AND ram = :ram"
            params["ram"] = ram
        if screen_size:
            screen_value = float(screen_size.replace(" inch", ""))  # Chuyển "inch" thành số thực
            query += " AND screen_size = :screen_size"
            params["screen_size"] = screen_value

        # Kết nối MySQL và chạy truy vấn
        with engine.connect() as connection:
            results = connection.execute(text(query), params).fetchall()

        # Xử lý kết quả trả về
        if results:
            response = "Dưới đây là những laptop phù hợp:\n"
            for laptop in results:
                response += f"- {laptop[0]} {laptop[1]} (Giá: {laptop[2]:,.0f} VND)\n"
        else:
            response = "Xin lỗi, tôi không tìm thấy laptop phù hợp."

        dispatcher.utter_message(response)
        return []
