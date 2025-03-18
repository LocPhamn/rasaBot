from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from sqlalchemy import create_engine, text

DB_URI = "mysql+mysqlconnector://root:Locpro%401997@localhost:3306/ws_proj"

# Tạo engine kết nối database
engine = create_engine(DB_URI)

class ActionCustomAction(Action):
    def name(self) -> Text:
        return "action_custom_action"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        category = tracker.get_slot("category")
        price = tracker.get_slot("price")
        ram = tracker.get_slot("ram")
        screen_size = tracker.get_slot("screen_size")

        query = "SELECT brand, model, price FROM laptops WHERE 1=1"
        params = {}
        response = ""
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

        with engine.connect() as connection:
            try:
                results = connection.execute(text(query), params).fetchall()
            except:
                response = "không thể thực thi query!"
                dispatcher.utter_message(text=f"{response}!")
            # Xử lý kết quả trả về
        if results:
            response = "Dưới đây là những laptop phù hợp:\n"
            for laptop in results:
                response += f"- {laptop[0]} {laptop[1]} (Giá: {laptop[2]:,.0f} VND)\n"
        else:
            response = "Xin lỗi, tôi không tìm thấy laptop phù hợp."

        dispatcher.utter_message(text=f"{response}!")


        return []