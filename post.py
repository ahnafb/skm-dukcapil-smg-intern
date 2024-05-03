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

# Data pilihan ages
ages_data = [
    "17-20",
    "21-25",
    "26-30",
    "31-35",
    "36-40",
    "41-45",
    "46-50",
    "51-55",
    "≥ 56"
]

# Insert data pilihan ages ke dalam koleksi 'ages'
db.ages.insert_many([{'range': ages} for ages in ages_data])

print("Data pilihan ages telah dimasukkan ke dalam database.")
