from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from sqlalchemy import create_engine, text
import re
import logging
logger = logging.getLogger(__name__)

DB_URI = "mysql+mysqlconnector://root:Locpro%401997@localhost:3306/es_proj"

# Tạo engine kết nối database
engine = create_engine(DB_URI)

class LaptopSuggestion(Action):
    def name(self) -> Text:
        return "laptop_suggestion"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        type = tracker.get_slot("type")
        price = tracker.get_slot("price")
        ram = tracker.get_slot("ram")
        screen = tracker.get_slot("screen")
        cpu = tracker.get_slot("cpu")
        gpu = tracker.get_slot("gpu")
        storage = tracker.get_slot("storage")
        resolution = tracker.get_slot("resolution")

        query = "SELECT p.product_name,c.price FROM product p JOIN configuration c ON p.idproduct = c.idproduct WHERE 1=1"
        params = {}
        response = ""
        if type:
            query += " AND p.type = :type"
            params["type"] = type
        # if price:
        #     match = re.search(r'\d+', price)
        #     price_value = int(match.group(0))
        #     dispatcher.utter_message(text=f"{price_value}!")

            # query += " AND c.price <= :price"
            # params["price"] = price
        # if ram:
        #     numbers = re.findall(r'\d+', ram)
        #     query += " AND c.ram = :ram"
        #     params["ram"] = numbers
        # if screen:
        #     screen_value = float(screen.replace(" inch", ""))  # Chuyển "inch" thành số thực
        #     query += " AND c.screen = :screen"
        #     params["screen"] = screen_value
        # if cpu:
        #     query += " AND c.cpu = :cpu"
        #     params["cpu"] = cpu
        # if gpu:
        #     query += " AND c.gpu = :gpu"
        #     params["gpu"] = gpu
        # if storage:
        #     query += " AND c.storage = :storage"
        #     params["storage"] = storage
        # if resolution:
        #     query += " AND c.resolution = :resolution"
        #     params["resolution"] = resolution


        # with engine.connect() as connection:
        #     try:
        #         results = connection.execute(text(query), params).fetchall()
        #     except:
        #         response = "không thể thực thi query!"
        #         dispatcher.utter_message(text=f"{response}!")
        #     # Xử lý kết quả trả về
        # if results:
        #     response = "Dưới đây là những laptop phù hợp:\n"
        #     for laptop in results:
        #         response += f"- {laptop[0]} (Giá: {laptop[1]:,.0f} $)\n"
        # else:
        #     response = "Xin lỗi, tôi không tìm thấy laptop phù hợp."
        match = re.search(r'\d+', type)
        type_value = int(match.group(0))
        logger.info(f"Giá trị price nhận được: {type}")

        if type:
            dispatcher.utter_message(text=f"{type}!")
            logger.info(f"Giá trị price nhận được: {type_value}")
        if price:
            match = re.search(r'\d+', price)
            price_value = int(match.group(0))
            dispatcher.utter_message(text=f"{price_value}!")
        if ram:
            dispatcher.utter_message(text=f"{ram}!")
        if screen:
            dispatcher.utter_message(text=f"{screen}!")

        if cpu:
            dispatcher.utter_message(text=f"{cpu}!")

        if gpu:
            dispatcher.utter_message(text=f"{gpu}!")

        if storage:
            dispatcher.utter_message(text=f"{storage}!")

        if resolution:
            dispatcher.utter_message(text=f"{resolution}!")

        return []