# Laporan Dokumentasi Prototipe "Smart Traffic Navigator"

**Nama Proyek:** Smart Traffic Navigator (Fokus Area: Kota Medan)  
**Anggota Tim:** M. Apif Saipudin & Rasya Rizki Atala  
**Tech Stack:** Python (Flask), HTML5, JavaScript (Fetch API), TailwindCSS, Leaflet.js

---

## 1. Arsitektur Sistem

Aplikasi ini dibangun menggunakan arsitektur **Client-Server**.
*   **Backend (Server):** Dibangun menggunakan framework **Flask (Python)**. Bertugas memproses logika bisnis, mengelola *Object-Oriented Programming* (OOP) untuk perhitungan rute, dan menyimulasikan data lalu lintas.
*   **Frontend (Client):** Berjalan di *browser* pengguna. Dibangun menggunakan **HTML**, di-styling menggunakan **Tailwind CSS** agar terlihat profesional dan modern, serta **Vanilla JavaScript** untuk interaktivitas (Peta dan HTTP Requests).

---

## 2. Pemenuhan Syarat Konsep OOP (Python Backend)

Proyek ini sepenuhnya menerapkan prinsip *Object Oriented Programming* melalui tiga *Class* utama yang saling berinteraksi di dalam file `app.py`:

1.  **Class `Kendaraan`**
    *   **Atribut:** `jenis` (Motor/Mobil), `kecepatan_rata_rata`
    *   **Fungsi:** Menyimpan profil dasar kendaraan. Motor diset pada kecepatan rata-rata 45 km/j, sedangkan Mobil pada 30 km/j.

2.  **Class `Jalur`**
    *   **Atribut:** `nama_jalan`, `jarak_km`, `tingkat_kemacetan`, `faktor_macet`
    *   **Method:** `hitung_waktu_tempuh(kendaraan)`
    *   **Fungsi:** Menyimpan detail per segmen jalan raya. Method perhitungannya menggunakan rumus: `(Jarak / Kecepatan_Kendaraan) * Faktor_Macet * 60 Menit`. (Faktor macet: Lancar=1.0x, Padat=1.5x, Macet=2.5x).

3.  **Class `Navigator`**
    *   **Atribut:** `daftar_jalur` (Kumpulan objek `Jalur`)
    *   **Method:** `proses_perjalanan(kendaraan)`
    *   **Fungsi:** Bertindak sebagai *controller* utama. Menerima susunan rute, memproses seluruh objek `Jalur` di dalamnya secara berurutan, lalu menghitung total *Estimated Time of Arrival* (ETA), total jarak tempuh, dan mayoritas status kepadatan lalu lintas.

---

## 3. Integrasi Peta & API Eksternal (Frontend)

Untuk memberikan pengalaman seperti aplikasi navigasi sesungguhnya tanpa memakan biaya API berbayar (seperti Google Maps API), sistem ini memadukan 3 teknologi terbuka (*Open Source*):

1.  **Leaflet.js:**
    *   Digunakan untuk me-render kanvas peta interaktif yang difokuskan pada koordinat **Kota Medan**. Mendukung fitur klik bebas (*free-click*), *zoom*, dan *panning*.
2.  **Nominatim API (OpenStreetMap):**
    *   **Fungsi Reverse-Geocoding:** Ketika pengguna mengklik lokasi manapun di atas peta, sistem secara otomatis menerjemahkan titik koordinat (Latitude/Longitude) tersebut menjadi alamat teks/nama jalan nyata (misal: "Jalan Jamin Ginting, Medan").
3.  **OSRM (Open Source Routing Machine) API:**
    *   **Fungsi Dynamic Routing:** Setelah asal dan tujuan ditentukan, OSRM digunakan untuk mencari jalur jalan aspal yang menghubungkan dua titik tersebut. OSRM mengembalikan bentuk geometri jalan (*GeoJSON*) sehingga garis rute tidak lurus menembus bangunan, melainkan berbelok mengikuti bentuk jalan asli. OSRM juga memecah rute menjadi beberapa segmen/belokan (kumpulan jalan).

---

## 4. Alur Kerja Aplikasi (Workflow)

Berikut adalah urutan proses dari interaksi *user* hingga mendapatkan hasil akhir:

1.  **Input Pengguna:** Pengguna mengklik *Titik Asal* dan *Titik Tujuan* di peta secara bebas, lalu memilih *Jenis Kendaraan*.
2.  **Pencarian Rute (Client-Side):** JavaScript memanggil OSRM API untuk mencari rute jalan aspal.
3.  **Pengiriman Data (AJAX):** Rute yang didapat (yang berisi daftar segmen jalan dan jaraknya) dikirimkan ke Endpoint API Backend `POST /api/route` dalam format JSON.
4.  **Pemrosesan OOP (Server-Side):**
    *   Backend menerima daftar jalan tersebut.
    *   Secara dinamis, backend membuat objek `Jalur` untuk *setiap* belokan/segmen, dan menyuntikkan **simulasi kepadatan lalu lintas** (*randomized traffic state*: Lancar/Padat/Macet).
    *   Semua objek `Jalur` dimasukkan ke dalam objek `Navigator`.
    *   `Navigator` menghitung total waktu berdasarkan kendaraan dan mengembalikan hasilnya ke *Client*.
5.  **Rendering Hasil (Client-Side):** 
    *   Peta menggambar garis rute menggunakan data geometri.
    *   Dashboard menampilkan Total ETA, Total Jarak, Kepadatan, dan rincian detail setiap jalan (lengkap dengan indikator warna kemacetan per segmen) secara *real-time* tanpa *reload* halaman (*Single Page Application experience*).

---

## 5. Pembaruan Desain (UI/UX)

*   **Profesional & Minimalis:** Desain dirombak menggunakan framework **Tailwind CSS**. 
*   **Penggantian Ikon:** Seluruh emoji (`🚗`, `🚥`, dll) telah diganti menggunakan **SVG Icons** berdefinisi tinggi yang lebih relevan dan elegan untuk keperluan presentasi tingkat akademik (Tugas Akhir).
*   **Responsivitas:** Layout otomatis menyesuaikan diri baik saat dibuka di layar laptop yang lebar maupun layar *smartphone* yang sempit (berubah dari layout menyamping menjadi menyusun ke bawah).
