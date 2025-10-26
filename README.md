# Sistem Pendukung Keputusan Kelayakan Penerima Beasiswa Menggunakan Algoritma Random Forest (Studi Kasus : Universitas Sanata Dharma)
- Membangun sistem klasifikasi kelayakan penerima beasiswa menggunakan algoritma Random Forest.
- Melakukan data preprocessing, pelatihan model, evaluasi akurasi, dan deployment berbasis GUI Python (Tkinter).
- Sistem menerima input data manual atau file excel dan menampilkan status kelayakan penerima beasiswa.
- Melakukan usability testing bersama pihak kemahasiswaan berdasarkan lima aspek usability: learnability, efficiency, memorability, errors, dan satisfaction.
---
# ⚙️ Tools & Library
- Python
- Data Pre Processing
- Usability Testing
- Supervised Learning
- Machine Learning Evaluation
- draw.io
- Microsoft Excel
- scikit-learn
- joblib
- Tkinter
---
# 🗹 Step
- Subsistem manajemen data:
  - Data pendaftar Sanata Dharma Student Fund (SDSF) dari tahun 2019 hingga 2024 dengan jumlah data 1251 baris.
- Subsistem manajemen model:
  - Data preprocessing (data cleaning, data transformation)
  - Pembagian data (80% data training, 20% data testing)
  - K-Fold Cross Validation
  - Feature selection
  - Modelling Random Forest
- Subsistem manajemen dialog:
  - Simpan hasil model dengan akurasi terbaik
  - Melakukan pengujian berupa data tunggal/individu dan berupa data kelompok/klasifikasi file
- Usability testing
---
# 💡 Percobaan Pengujian
- n_estimators (jumlah pohon): 10, 30, 50, 70, 100
- K-Fold: 3, 5, 9, 10, 11
- Feature selection: metode embedded
![alt text](https://github.com/adventaa/SPPK-KelayakanPenerimaBeasiswa/blob/main/Grafik%20Hasil%20Pengujian.png?raw=true)
---
# ✨ Hasil
- Akurasi terbaik dihasilkan oleh model sebesar 80.18% dengan  menggunakan pengujian k-fold = 11, jumlah tree = 100, dan dan atribut yang terpilih dalam feature selection yaitu 'Jumlah Indeks Prestasi Kumulatif(BS Prestasi)', 'Jumlah Gaji/penghasilan Bapak', 'Jumlah Gaji/penghasilan Ibu', 'Jumlah Tagihan Listrik', dan 'IPK 1 Smt Sebelum Daftar'.
- Usability testing oleh pengguna sistem yaitu Lembaga Kesejahteraan Mahasiswa didapatkan persentase yaitu 95% , dengan urutan tingkat keseimbangan dari aspek usability yaitu Learnability, Satisfaction, Efficiency, Memorability, Error Tolerant.
---
# 🖥️ Subsistem Manajemen Dialog
1. Halaman Modelling: berfungsi untuk membuat model berdasarkan hasil data preprocessing, input jumlah k-fold, dan input jumlah tree (pohon), sehingga menghasilkan akurasi dan model yang telah dibangun dapat disimpan agar dapat digunakan dalam tahap pengujian data.
![alt text](https://github.com/adventaa/SPPK-KelayakanPenerimaBeasiswa/blob/main/Hasil%20Halaman%20Modelling.png?raw=true)

3. Halaman Uji Data: berfungsi melakukan pengujian data untuk pengambilan keputusan dalam bentuk data individual atau data tunggal dan dalam bentuk data kelompok atau berupa file yang diinputkan. Pada pengujian data ini dilakukan dengan menggunakan model yang telah disimpan pada halaman modeling sehingga dapat menampilkan hasil keputusan.
![alt text](https://github.com/adventaa/SPPK-KelayakanPenerimaBeasiswa/blob/main/Halaman%20Uji%20Data%20Tunggal%20(Tidak%20Layak%20Menerima%20Beasiswa).png?raw=true)
![alt text](https://github.com/adventaa/SPPK-KelayakanPenerimaBeasiswa/blob/main/Halaman%20Uji%20Data%20Tunggal%20(Layak%20Menerima%20Beasiswa).png?raw=true)

- Simpan data tunggal
![alt text](https://github.com/adventaa/SPPK-KelayakanPenerimaBeasiswa/blob/main/Halaman%20Uji%20Data%20Tunggal%20(Hasil%20Simpan%20Uji%20Data%20Tunggal).png?raw=true)

- Memilih file pengujian data beasiswa periode selanjutnya: dengan memililh tombol 'Input File Excel Beasiswa SDSF' pada halaman Uji Data
![alt text](https://github.com/adventaa/SPPK-KelayakanPenerimaBeasiswa/blob/main/Pilih%20File%20Pengujian%20Data%20Beasiswa%20Periode%20Selanjutnya.png?raw=true)

- Menampilkan lokasi penyimpanan hasil klasifikasi data beasiswa periode selanjutnya: setelah memilih file excel yang berisi data beasiswa periode selanjutnya, maka sistem akan otomatis melakukan pengujian dengan hasil model yang sudah dilakukan diawal, sehingga data beasiswa periode selanjutnya langsung tersimpan ke dalam penyimpanan internal.
![alt text](https://github.com/adventaa/SPPK-KelayakanPenerimaBeasiswa/blob/main/Hasil%20Lokasi%20Penyimpanan%20File%20Beasiswa%20Periode%20Berikutnya.png?raw=true)

