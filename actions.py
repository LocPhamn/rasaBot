import pymysql
from sqlalchemy import create_engine, text

DB_URI = "mysql+pymysql://root:Locpro@1997@localhost/rasa_data?charset=utf8mb4"

try:
    engine = create_engine(DB_URI, future=True)
    connection = engine.connect()
    print("✅ Kết nối MySQL thành công!")
    connection.close()
except Exception as e:
    print(f"❌ Lỗi kết nối MySQL: {e}")
