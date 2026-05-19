import random
import hashlib
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class Kendaraan:
    def __init__(self, jenis):
        self.jenis = jenis.lower()
        if self.jenis == 'motor':
            self.kecepatan_rata_rata = 45.0
        elif self.jenis == 'mobil':
            self.kecepatan_rata_rata = 30.0
        else:
            self.kecepatan_rata_rata = 35.0

class Jalur:
    def __init__(self, nama_jalan, jarak_km, tingkat_kemacetan):
        self.nama_jalan = nama_jalan if nama_jalan else "Jalan Tanpa Nama"
        self.jarak_km = jarak_km
        self.tingkat_kemacetan = tingkat_kemacetan.lower()
        self.update_faktor_macet()

    def update_faktor_macet(self):
        if self.tingkat_kemacetan == 'lancar':
            self.faktor_macet = 1.0
        elif self.tingkat_kemacetan == 'padat':
            self.faktor_macet = 1.5
        elif self.tingkat_kemacetan == 'macet':
            self.faktor_macet = 2.5
        else:
            self.faktor_macet = 1.0

    def hitung_waktu_tempuh(self, kendaraan):
        waktu_jam = self.jarak_km / kendaraan.kecepatan_rata_rata
        waktu_menit = waktu_jam * self.faktor_macet * 60
        return waktu_menit

class Navigator:
    def __init__(self):
        self.daftar_jalur = []

    def set_rute(self, daftar_jalur):
        self.daftar_jalur = daftar_jalur

    def proses_perjalanan(self, kendaraan):
        waktu_total = 0
        total_jarak = 0
        kondisi_jalan = []
        detail_rute = []

        for jalur in self.daftar_jalur:
            waktu_segmen = jalur.hitung_waktu_tempuh(kendaraan)
            waktu_total += waktu_segmen
            total_jarak += jalur.jarak_km
            kondisi_jalan.append(jalur.tingkat_kemacetan)

            detail_rute.append({
                "jalan": jalur.nama_jalan,
                "jarak_km": round(jalur.jarak_km, 2),
                "kondisi": jalur.tingkat_kemacetan,
                "estimasi_menit": round(waktu_segmen)
            })

        lancar_count = kondisi_jalan.count('lancar')
        padat_count = kondisi_jalan.count('padat')
        macet_count = kondisi_jalan.count('macet')
        
        if macet_count > 0 and macet_count >= padat_count:
            status_overall = "Macet"
        elif padat_count > 0:
            status_overall = "Padat"
        else:
            status_overall = "Lancar"

        return {
            "estimasi_waktu_total_menit": round(waktu_total),
            "total_jarak_km": round(total_jarak, 2),
            "status_kepadatan": status_overall,
            "detail_rute": detail_rute
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/route', methods=['POST'])
def api_route():
    data = request.json
    jenis_kendaraan = data.get('kendaraan', 'motor')
    segments = data.get('segments', [])

    if not segments:
        return jsonify({"error": "Data rute kosong"}), 400

    kendaraan = Kendaraan(jenis_kendaraan)
    kondisi_opsi = ['lancar', 'padat', 'macet']
    
    list_objek_jalur = []
    for seg in segments:
        jarak_km = seg.get('distance', 0) / 1000.0
        if jarak_km <= 0:
            continue
            
        nama_jalan = seg.get('name', 'Jalan Tanpa Nama')
        hash_val = int(hashlib.md5(nama_jalan.encode()).hexdigest(), 16) % 100
        if hash_val < 60:
            kondisi = 'lancar'
        elif hash_val < 90:
            kondisi = 'padat'
        else:
            kondisi = 'macet'
        
        objek_jalur = Jalur(nama_jalan, jarak_km, kondisi)
        list_objek_jalur.append(objek_jalur)

    if not list_objek_jalur:
        return jsonify({"error": "Jarak terlalu pendek untuk diproses"}), 400

    navigator = Navigator()
    navigator.set_rute(list_objek_jalur)
    hasil = navigator.proses_perjalanan(kendaraan)

    hasil["kendaraan"] = kendaraan.jenis
    hasil["kecepatan_rata_rata"] = kendaraan.kecepatan_rata_rata
    
    return jsonify(hasil)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
