# Import MongoClient dari pymongo
from pymongo import MongoClient

# Buat koneksi ke MongoDB
connection_string = "mongodb+srv://ahnafb:nanaf2730@cluster0.qzd2yiy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(connection_string)

# Pilih database
db = client.db_VT30DATA

# Data pilihan jenis layanan
jenis_layanan_data = [
    "Pelayanan Akta Perkawinan",
    "Pelayanan Akta Kelahiran",
    "Pelayanan Akta Kematian",
    "KTP Elektronik",
    "Kartu Keluarga (KK)",
    "Kartu Identitas Anak (KIA)"
]

# Insert data pilihan jenis layanan ke dalam koleksi 'jenis_layanan'
db.jenis_layanan.insert_many([{'pilihan_layanan': layanan} for layanan in jenis_layanan_data])

print("Data jenis layanan telah dimasukkan ke dalam database.")
