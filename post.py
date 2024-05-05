import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load .env file
load_dotenv()

# Read environment variables
connection_string = os.getenv("DB_CONNECTION_STRING")
db_name = os.getenv("DB_NAME")

# Set up MongoDB connection
client = MongoClient(connection_string)
db = client[db_name]

# Data pilihan pekerjaan
pekerjaan_data = [
    "PNS",
    "TNI",
    "POLRI",
    "SWASTA",
    "WIRAUSAHA",
    "Lainnya"
]

# Insert data pilihan pekerjaan ke dalam koleksi 'pekerjaans'
db.pekerjaans.insert_many([{'name': pekerjaan} for pekerjaan in pekerjaan_data])

print("Data pilihan pekerjaan telah dimasukkan ke dalam database.")
