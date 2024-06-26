from flask import (Flask, render_template, jsonify, request, redirect, url_for, send_file)
from pymongo import MongoClient
import jwt
import hashlib
import csv
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from bson import ObjectId
import pandas as pd 
from flask_cors import CORS 
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load .env file
load_dotenv()

# Read environment variables
connection_string = os.getenv("DB_CONNECTION_STRING")
db_name = os.getenv("DB_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")

# Set up MongoDB connection
client = MongoClient(connection_string)
db = client[db_name]

def hitung_skor(pertanyaan):
    skor = 0
    for nilai in pertanyaan:
        if nilai == 'Sangat Sesuai' or nilai == 'Sangat Mudah' or nilai == 'Sangat Cepat' or nilai == 'Gratis' or nilai == 'Sangat Sesuai' or nilai == 'Sangat Kompeten' or nilai == 'Sangat sopan dan sangat ramah' or nilai == 'Sangat baik' or nilai == 'Dikelola dengan baik' or nilai == 'Sangat Puas':
            skor += 10
        elif nilai == 'Sesuai' or nilai == 'Mudah' or nilai == 'Cepat' or nilai == 'Murah' or nilai == 'Sesuai' or nilai == 'Kompeten' or nilai == 'Sopan dan ramah' or nilai == 'Baik' or nilai == 'Berfungsi kurang maksimal' or nilai == 'Puas':
            skor += 7.5
        elif nilai == 'Kurang Sesuai' or nilai == 'Kurang Mudah' or nilai == 'Kurang Cepat' or nilai == 'Cukup Mahal' or nilai == 'Kurang Sesuai' or nilai == 'Kurang Kompeten' or nilai == 'Kurang sopan dan kurang ramah' or nilai == 'Cukup' or nilai == 'Ada tetapi tidak berfungsi' or nilai == 'Kurang Puas':
            skor += 5
        elif nilai == 'Tidak Sesuai' or nilai == 'Tidak Mudah' or nilai == 'Tidak Cepat' or nilai == 'Sangat Mahal' or nilai == 'Tidak Sesuai' or nilai == 'Tidak Kompeten' or nilai == 'Tidak sopan dan tidak ramah' or nilai == 'Buruk' or nilai == 'Tidak ada' or nilai == 'Tidak Puas':
            skor += 2.5
    return skor

@app.route('/')
def home():
    # Ambil data jenis layanan dari database
    services = db.services.find()
    genders = db.genders.find()
    ages = db.ages.find() 
    pendidikans = db.pendidikans.find()     
    pekerjaans = db.pekerjaans.find()
    questions = db.questions.find()
    # Kirim data ke template HTML
    return render_template('index.html', services=services, genders=genders, ages=ages, pendidikans=pendidikans, pekerjaans=pekerjaans, questions=questions)

@app.route('/datadiri', methods=['GET'])
def show_datadiri():
    sample_receive = request.args.get('sample_give')
    print(sample_receive)
    return jsonify({'msg': 'GET request complete!'})

@app.route('/datadiri', methods=['POST'])
def save_datadiri():
    # sample_receive = request.form.get('sample_give')
    # print(sample_receive)
    # nama_receive = request.form.get("nama_give")
    # * Jenis Layanan *
    layanan_receive = request.form.get("layanan_give")

    # * Profile *
    kelamin_receive = request.form.get("kelamin_give")
    usia_receive = request.form.get("usia_give")
    pendidikan_receive = request.form.get("pendidikan_give")
    pekerjaan_receive = request.form.get("pekerjaan_give")
    if pekerjaan_receive == "Lainnya":
        pekerjaan_receive = request.form.get("pekerjaan_lainnya")

    # * Form Pertanyaan * 
    p1_receive = request.form.get("p1_give")
    p2_receive = request.form.get("p2_give")
    p3_receive = request.form.get("p3_give")
    p4_receive = request.form.get("p4_give")
    p5_receive = request.form.get("p5_give")
    p6_receive = request.form.get("p6_give")
    p7_receive = request.form.get("p7_give")
    p8_receive = request.form.get("p8_give")
    p9_receive = request.form.get("p9_give")
    p10_receive = request.form.get("p10_give")

    # * Form Kritik & Saran *
    kritik_receive = request.form.get("kritik")
    saran_receive = request.form.get("saran")

    # * Skor *
    pertanyaan = [p1_receive, p2_receive, p3_receive, p4_receive, p5_receive, p6_receive, p7_receive, p8_receive, p9_receive, p10_receive]
    skor = hitung_skor(pertanyaan)

    # * Timestamp *
    tanggal_dibuat = datetime.now().strftime("%Y-%m-%d || %H:%M:%S")  # Ubah ke format string

    doc = {
        # * Jenis Layanan *
        'layanan': layanan_receive,
        
        # * Profil *
        # 'nama' : nama_receive,
        'jenis_kelamin': kelamin_receive,
        'usia': usia_receive,
        'pendidikan': pendidikan_receive, 
        'pekerjaan': pekerjaan_receive, 
        'pekerjaanLainnya': pekerjaan_receive,

        # * Pertanyaan *
        'nomor1': p1_receive,
        'nomor2': p2_receive,
        'nomor3': p3_receive,
        'nomor4': p4_receive,
        'nomor5': p5_receive,
        'nomor6': p6_receive,
        'nomor7': p7_receive,
        'nomor8': p8_receive,
        'nomor9': p9_receive,
        'nomor10': p10_receive,

        # * Kritik & Saran *
        'boxKritik': kritik_receive,
        'boxSaran': saran_receive, 

        # * Skor *
        'pertanyaan': pertanyaan,
        'skor': skor,
        
        # * Timestamp * 
        'waktu_dibuat': tanggal_dibuat,

    }
    db.TData30.insert_one(doc)
    return jsonify({'msg': 'POST request complete!'})

@app.route('/admin-page', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        jenis_layanan_selected = request.form.get('jenis_layanan')
        if jenis_layanan_selected == 'all':
            datadiris = db.TData30.find()  # Memuat semua data jika dipilih "Semua Jenis Layanan"
        else:
            datadiris = db.TData30.find({'layanan': jenis_layanan_selected})  # Memuat data sesuai dengan jenis layanan yang dipilih
        return render_template('table_rows.html', datadiris=datadiris)  # Mengirim kembali data tabel yang diperbarui
    else:
        datadiris = db.TData30.find()  # Mengambil semua data dari koleksi datadiri
        services = db.services.find()  # Memuat semua data layanan untuk ditampilkan di halaman admin
        genders = db.genders.find()  # Memuat semua data jenis kelamin untuk ditampilkan di halaman admin
        return render_template('admin-page.html', datadiris=datadiris, services=services, genders=genders)

@app.route('/statistik_dashboard')
def statistik():
    return render_template('statistik_dashboard.html')

# !!!!!!! Form Page Tampil CRUD
@app.route('/form_dashboard')
def form():
    services = db.services.find()  
    genders = db.genders.find()
    ages = db.ages.find() 
    pendidikans = db.pendidikans.find()
    pekerjaans = db.pekerjaans.find()
    questions = db.questions.find()
    return render_template('form_dashboard.html', services=services, genders=genders, ages=ages, pendidikans=pendidikans, pekerjaans=pekerjaans, questions=questions)

# !!!!!!! Form page ->> CRUD Jenis Layanan
@app.route('/add_service', methods=['POST'])
def add_service():
    service_name = request.form['service_name']
    db.services.insert_one({'name': service_name})
    return jsonify({'message': 'Jenis Layanan berhasil ditambahkan!'})

@app.route('/edit_service', methods=['POST'])
def edit_service():
    service_id = request.form['service_id']
    new_name = request.form['new_name']
    db.services.update_one({'_id': ObjectId(service_id)}, {'$set': {'name': new_name}})
    return jsonify({'message': 'Jenis Layanan berhasil di-update!'})

@app.route('/delete_service', methods=['POST'])
def delete_service():
    service_id = request.form['service_id']
    db.services.delete_one({'_id': ObjectId(service_id)})
    return jsonify({'message': 'Jenis Layanan berhasil dihapus!'})  

# !!!!!!! Form page ->> CRUD Jenis Kelamin
@app.route('/add_gender', methods=['POST'])
def add_gender():
    gender_name = request.form['gender_name']
    db.genders.insert_one({'name': gender_name})
    return jsonify({'message': 'Jenis Kelamin berhasil ditambahkan!'})

@app.route('/edit_gender', methods=['POST'])
def edit_gender():
    gender_id = request.form['gender_id']
    new_name = request.form['new_name']
    db.genders.update_one({'_id': ObjectId(gender_id)}, {'$set': {'name': new_name}})
    return jsonify({'message': 'Jenis Kelamin berhasil di-update!'})

@app.route('/delete_gender', methods=['POST'])
def delete_gender():
    gender_id = request.form['gender_id']
    db.genders.delete_one({'_id': ObjectId(gender_id)})
    return jsonify({'message': 'Jenis Kelamin berhasil dihapus!'})

# !!!!!!! Form page ->> CRUD Usia
# Route untuk menambah usia
@app.route('/add_age', methods=['POST'])
def add_age():
    age_range = request.form['age_range']
    db.ages.insert_one({'range': age_range})
    return jsonify({'message': 'Usia berhasil ditambahkan!'})

# Route untuk mengedit usia
@app.route('/edit_age', methods=['POST'])
def edit_age():
    age_id = request.form['age_id']
    new_range = request.form['new_range']
    db.ages.update_one({'_id': ObjectId(age_id)}, {'$set': {'range': new_range}})
    return jsonify({'message': 'Usia berhasil di-update!'})

# Route untuk menghapus usia
@app.route('/delete_age', methods=['POST'])
def delete_age():
    age_id = request.form['age_id']
    db.ages.delete_one({'_id': ObjectId(age_id)})
    return jsonify({'message': 'Usia berhasil dihapus!'})

# !!!!!!! Form page ->> CRUD Pendidikan
@app.route('/add_pendidikan', methods=['POST'])
def add_pendidikan():
    pendidikan_name = request.form['pendidikan_name']
    db.pendidikans.insert_one({'name': pendidikan_name})
    return jsonify({'message': 'Pendidikan berhasil ditambahkan!'})

# Route untuk mengedit pendidikan
@app.route('/edit_pendidikan', methods=['POST'])
def edit_pendidikan():
    pendidikan_id = request.form['pendidikan_id']
    new_name = request.form['new_name']
    db.pendidikans.update_one({'_id': ObjectId(pendidikan_id)}, {'$set': {'name': new_name}})
    return jsonify({'message': 'Pendidikan berhasil di-update!'})

# Route untuk menghapus pendidikan
@app.route('/delete_pendidikan', methods=['POST'])
def delete_pendidikan():
    pendidikan_id = request.form['pendidikan_id']
    db.pendidikans.delete_one({'_id': ObjectId(pendidikan_id)})
    return jsonify({'message': 'Pendidikan berhasil dihapus!'})

# !!!!!!! Form page ->> CRUD Pendidikan
# Route untuk menambah pekerjaan
@app.route('/add_pekerjaan', methods=['POST'])
def add_pekerjaan():
    pekerjaan_name = request.form['pekerjaan_name']
    db.pekerjaans.insert_one({'name': pekerjaan_name})
    return jsonify({'message': 'Pekerjaan berhasil ditambahkan!'})

# Route untuk mengedit pekerjaan
@app.route('/edit_pekerjaan', methods=['POST'])
def edit_pekerjaan():
    pekerjaan_id = request.form['pekerjaan_id']
    new_name = request.form['new_name']
    db.pekerjaans.update_one({'_id': ObjectId(pekerjaan_id)}, {'$set': {'name': new_name}})
    return jsonify({'message': 'Pekerjaan berhasil di-update!'})

# Route untuk menghapus pekerjaan
@app.route('/delete_pekerjaan', methods=['POST'])
def delete_pekerjaan():
    pekerjaan_id = request.form['pekerjaan_id']
    db.pekerjaans.delete_one({'_id': ObjectId(pekerjaan_id)})
    return jsonify({'message': 'Pekerjaan berhasil dihapus!'})

# !!! FORM PERTANYAAN CRUD
# Route untuk menambah pertanyaan
@app.route('/add_question', methods=['POST'])
def add_question():
    # Ambil data dari form
    question_text = request.form['question_text']
    options = [
        {'option_text': request.form['option1_text'], 'value': float(request.form['option1_value'])},
        {'option_text': request.form['option2_text'], 'value': float(request.form['option2_value'])},
        {'option_text': request.form['option3_text'], 'value': float(request.form['option3_value'])},
        {'option_text': request.form['option4_text'], 'value': float(request.form['option4_value'])}
    ]

    # Masukkan pertanyaan ke dalam database
    db.questions.insert_one({
        'question_text': question_text,
        'options': options
    })

    return jsonify({'message': 'Question added successfully!'})

# !!! FORM PERTANYAAN CRUD EDIT
# Route untuk mengedit pertanyaan
@app.route('/edit_question', methods=['POST'])
def edit_question():
    # Ambil data dari form
    question_id = request.form['question_id']
    question_text = request.form['question_text']
    options = [
        {'option_text': request.form['option1_text'], 'value': float(request.form['option1_value'])},
        {'option_text': request.form['option2_text'], 'value': float(request.form['option2_value'])},
        {'option_text': request.form['option3_text'], 'value': float(request.form['option3_value'])},
        {'option_text': request.form['option4_text'], 'value': float(request.form['option4_value'])}
    ]

    # Update pertanyaan di dalam database
    db.questions.update_one(
        {'_id': ObjectId(question_id)},
        {'$set': {
            'question_text': question_text,
            'options': options
        }}
    )

    return jsonify({'message': 'Question updated successfully!'})


# !!!!!! end of admin page

# ! Version1 Excel
@app.route('/export-excel', methods=['GET'])
def export_excel():
    # Ambil jenis layanan dari parameter URL
    jenis_layanan = request.args.get('jenis_layanan')

    # Ambil data dari MongoDB sesuai dengan jenis layanan yang dipilih
    if jenis_layanan == 'all':
        data = list(db.TData30.find({}, {'_id': 0}))  # Mengabaikan kolom _id
    else:
        data = list(db.TData30.find({'layanan': jenis_layanan}, {'_id': 0}))  # Mengabaikan kolom _id

    # Buat dataframe dari data MongoDB
    df = pd.DataFrame(data)

    # Menyesuaikan header
    custom_header = {
        'layanan': 'Jenis Layanan',
        'jenis_kelamin': 'Jenis Kelamin',
        'usia': 'Usia',
        'pendidikan': 'Pendidikan',
        'pekerjaan': 'Pekerjaan',
        'pekerjaanLainnya': 'Pekerjaan Lainnya',
        'nomor1': 'Nomor 1',
        'nomor2': 'Nomor 2',
        'nomor3': 'Nomor 3',
        'nomor4': 'Nomor 4',
        'nomor5': 'Nomor 5',
        'nomor6': 'Nomor 6',
        'nomor7': 'Nomor 7',
        'nomor8': 'Nomor 8',
        'nomor9': 'Nomor 9',
        'nomor10': 'Nomor 10',
        'boxKritik': 'Kritik',
        'boxSaran': 'Saran',
        'skor': 'Skor'
    }
    df = df.rename(columns=custom_header)

    # Nama file Excel sesuai dengan jenis layanan
    if jenis_layanan == 'all':
        filename = 'all-data.xlsx'
    else:
        filename = jenis_layanan.replace(' ', '-') + '-data.xlsx'

    # Tulis data ke file Excel
    df.to_excel(filename, index=False)

    # Kirim file Excel ke pengguna
    return send_file(filename, as_attachment=True)

# ! Start of Login
@app.route("/login", methods=['GET'])
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@app.route("/sign_up/save", methods=["POST"])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # id
        "password": password_hash,                                  # password
        "profile_name": username_receive,                           # user's name is set to their id by default
        "profile_pic": "",                                          # profile image file name
        "profile_pic_real": "profile_pics/profile_placeholder.png", # a default profile image
        "profile_info": ""                                          # a profile description
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route("/sign_in", methods=["POST"])
def sign_in():
    # Sign in
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    result = db.users.find_one(
        {
            "username": username_receive,
            "password": pw_hash,
        }
    )
    if result:
        payload = {
            "id": username_receive,
            # the token will be valid for 24 hours
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
    # Let's also handle the case where the id and
    # password combination cannot be found
    else:
        return jsonify(
            {
                "result": "fail",
                "msg": "We could not find a user with that id/password combination",
            }
        )
# ! End of Login

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)