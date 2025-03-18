from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from sqlalchemy import create_engine, text
import re
from rasa_sdk.events import SlotSet
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
        # Tham số nhận vào
        type = tracker.get_slot("type")
        price = tracker.get_slot("price")
        ram = tracker.get_slot("ram")
        screen = tracker.get_slot("screen")
        cpu = tracker.get_slot("cpu")
        gpu = tracker.get_slot("gpu")
        storage = tracker.get_slot("storage")
        resolution = tracker.get_slot("resolution")

        # Xây dựng sql Query
        query = "SELECT p.product_name,c.price FROM product p JOIN configuration c ON p.idproduct = c.idproduct WHERE 1=1"
        params = {}
        response = ""

        # if name:
        #     query += " AND (p.brand LIKE :name OR p.product_name LIKE :name)"
        #     params["name"] = name
        #     logger.info(f"Giá trị type nhận được: {name}")

        if type:
            query += " AND p.type = :type"
            params["type"] = type
            logger.info(f"Giá trị type nhận được: {type}")

        if price:
            price_value = re.findall(r"\d+",price)
            logger.info(f"Giá trị price nhận được: {price_value}")

            query += " AND c.price <= :price"
            params["price"] = price
        if ram:
            numbers = re.findall(r'\d+', ram)
            logger.info(f"Giá trị ram nhận được: {numbers}")

            query += " AND c.ram = :ram"
            params["ram"] = numbers
        if screen:
            numbers = re.findall(r'\d+', screen)
            logger.info(f"Giá trị screen nhận được: {screen}")
            query += " AND c.screen = :screen"
            params["screen"] = numbers
        if cpu:
            logger.info(f"Giá trị cpu nhận được: {cpu}")
            query += " AND c.cpu = :cpu"
            params["cpu"] = cpu
        if gpu:
            logger.info(f"Giá trị gpu nhận được: {gpu}")
            query += " AND c.gpu = :gpu"
            params["gpu"] = gpu
        if storage:
            numbers = re.findall(r'\d+', storage)
            logger.info(f"Giá trị storage nhận được: {numbers}")
            query += " AND c.storage = :storage"
            params["storage"] = storage
        if resolution:
            logger.info(f"Giá trị resolution nhận được: {resolution}")
            query += " AND c.resolution = :resolution"
            params["resolution"] = resolution

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
                response += f"- {laptop[0]} (Giá: ${laptop[1]:,.0f})\n"
        else:
            response = "Xin lỗi, tôi không tìm thấy laptop phù hợp."

        dispatcher.utter_message(text=f"{response}!")

        return []

    class ActionClearSlots(Action):
        def name(self) -> Text:
            return "clear_slots"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            # Reset tất cả slots liên quan
            return [
                SlotSet("type", None),
                SlotSet("price", None),
                SlotSet("ram", None),
                SlotSet("screen", None),
                SlotSet("cpu", None),
                SlotSet("gpu", None),
                SlotSet("storage", None),
                SlotSet("resolution", None)
            ]