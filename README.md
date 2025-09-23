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
# ✨ Hasil
- Akurasi terbaik dihasilkan oleh model sebesar 80.18% dengan  menggunakan pengujian k-fold = 11, jumlah tree = 100, dan dan atribut yang terpilih dalam feature selection yaitu 'Jumlah Indeks Prestasi Kumulatif(BS Prestasi)', 'Jumlah Gaji/penghasilan Bapak', 'Jumlah Gaji/penghasilan Ibu', 'Jumlah Tagihan Listrik', dan 'IPK 1 Smt Sebelum Daftar'.
- Usability testing oleh pengguna sistem yaitu Lembaga Kesejahteraan Mahasiswa didapatkan persentase yaitu 95% , dengan urutan tingkat keseimbangan dari aspek usability yaitu Learnability, Satisfaction, Efficiency, Memorability, Error Tolerant.

