import tkinter as tk
import tkinter.font as tkFont
import os
import numpy as np
import pandas as pd
import openpyxl
import joblib
from datetime import datetime
from tkinter import ttk, messagebox, filedialog
from Modelling import ModelingTab
from sklearn.metrics import (confusion_matrix, accuracy_score, classification_report)

class UjiDataTab:
    def __init__(self, notebook, modeling_tab):

        # Buat font bold
        bold_font = tkFont.Font(weight="bold", size=10)

        self.frame = ttk.Frame(notebook)
        self.modeling_tab = modeling_tab  # Akses data dari halaman modeling

        self.form_frame = ttk.Frame(self.frame)
        self.form_frame.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Tombol Simpan Data Tunggal
        self.btn_simpan_data = ttk.Button(self.form_frame, text="Simpan Data Tunggal", command=self.simpan_data_tunggal)
        self.btn_simpan_data.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Tombol Isi Ulang Data
        self.btn_ulang = ttk.Button(self.form_frame, text="Isi Ulang Data", command=self.isi_ulang_data)
        self.btn_ulang.grid(row=0, column=4, padx=10, pady=5, sticky="w")
        
        # Label & Input 
        self.form_frame = ttk.Frame(self.frame)
        self.form_frame.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        # Input Semester
        ttk.Label(self.form_frame, text="Semester").grid(row=5, column=1, padx=5, pady=10, sticky="w")
        self.semester_entry = ttk.Entry(self.form_frame, width=20)
        self.semester_entry.grid(row=5, column=10, padx=5, pady=2, sticky="w")

        # Input IPK saat mendaftar
        ttk.Label(self.form_frame, text="IPK Saat Mendaftar").grid(row=10, column=1, padx=5, pady=10, sticky="w")
        self.ipk_entry = ttk.Entry(self.form_frame, width=20)
        self.ipk_entry.grid(row=10, column=10, padx=5, pady=2, sticky="w")

        # Input Penghasilan Bapak
        ttk.Label(self.form_frame, text="Jumlah Penghasilan/Gaji Bapak").grid(row=15, column=1, padx=5, pady=10, sticky="w")
        self.bapak_entry = ttk.Entry(self.form_frame, width=20)
        self.bapak_entry.grid(row=15, column=10, padx=5, pady=2, sticky="w")

        # Input Penghasilan Ibu
        ttk.Label(self.form_frame, text="Jumlah Penghasilan/Gaji Ibu").grid(row=20, column=1, padx=5, pady=10, sticky="w")
        self.ibu_entry = ttk.Entry(self.form_frame, width=20)
        self.ibu_entry.grid(row=20, column=10, padx=5, pady=2, sticky="w")

        # Input Tagihan Listrik
        ttk.Label(self.form_frame, text="Jumlah Tagihan Listrik").grid(row=25, column=1, padx=5, pady=10, sticky="w")
        self.listrik_entry = ttk.Entry(self.form_frame, width=20)
        self.listrik_entry.grid(row=25, column=10, padx=5, pady=2, sticky="w")

        # Input Tanggungan Orang Tua
        ttk.Label(self.form_frame, text="Jumlah Tanggungan Orang Tua Yang Masih Studi").grid(row=30, column=1, padx=5, pady=10, sticky="w")
        self.tanggungan_entry = ttk.Entry(self.form_frame, width=20)
        self.tanggungan_entry.grid(row=30, column=10, padx=5, pady=2, sticky="w")
        
        # Input Tunggakan
        ttk.Label(self.form_frame, text="Jumlah Tunggakan Pembayaran Kuliah").grid(row=35, column=1, padx=5, pady=10, sticky="w")
        self.tunggakan_entry = ttk.Entry(self.form_frame, width=20)
        self.tunggakan_entry.grid(row=35, column=10, padx=5, pady=2, sticky="w")

        # Input IPK 1 Semeseter Sebelum
        ttk.Label(self.form_frame, text="IPK 1 Semester Sebelum Daftar").grid(row=40, column=1, padx=5, pady=10, sticky="w")
        self.ipk_sebelum_entry = ttk.Entry(self.form_frame, width=20)
        self.ipk_sebelum_entry.grid(row=40, column=10, padx=5, pady=2, sticky="w")
        
        # Input Jumlah Saudara
        ttk.Label(self.form_frame, text="Jumlah Saudara").grid(row=45, column=1, padx=5, pady=10, sticky="w")
        self.saudara_entry = ttk.Entry(self.form_frame, width=20)
        self.saudara_entry.grid(row=45, column=10, padx=5, pady=2, sticky="w")

        # Tombol Proses
        self.btn_proses = ttk.Button(self.form_frame, text="Proses", command=self.proses_data)
        self.btn_proses.grid(row=5, column=50, padx=185, pady=2, sticky="w")

        # Label Hasil Keputusan
        self.keputusan_label = ttk.Label(self.form_frame, text="Hasil Keputusan")
        self.keputusan_label.grid(row=10, column=50, padx=180, pady=2, sticky="w")

        # Display Box Menampilkan Hasil keputusan
        self.keputusan_display = tk.Text(self.form_frame, height=3, width=30, state="disabled")
        self.keputusan_display.grid(row=15, column=50, padx=100, pady=2, sticky="w")

        # Label klasifikasi file
        self.klasifikasi_label = ttk.Label(self.form_frame, text="Klasifikasi File")
        self.klasifikasi_label.grid(row=35, column=50, padx=180, pady=2, sticky="w")

        # Tombol klasifikasi file
        self.btn_klasifikasi = ttk.Button(self.form_frame, text="Input File Excel Beasiswa SDSF", command=self.klasifikasi_file)
        self.btn_klasifikasi.grid(row=40, column=50, padx=135, pady=2, sticky="w")
        
        langkah_teks = (
            "Langkah-langkah :\n"
            "1. Setelah membuat model, masukkan data pada form di atas untuk uji data tunggal\n"
            "2. Klik tombol 'Proses' untuk melihat hasil keputusan data tunggal\n"
            "3. Klik tombol 'Simpan Data Tunggal' jika ingin menyimpan hasil keputusan data tunggal\n"
            "4. Klik tombol 'Isi Ulang Data' untuk mengisi kembali data pada form\n"
            "5. Jika ingin uji data kelompok, klik 'Input File Excel Beasiswa SDSF'"
        )
        label_langkah = ttk.Label(self.form_frame, text=langkah_teks, justify="left")
        label_langkah.grid(row=75, column=1, sticky="w", padx=5, pady=10)

        
    # Fungsi Isi Ulang Data
    def isi_ulang_data(self):
        # Hapus isi data di setiap kolom
        self.semester_entry.delete(0, "end")
        self.ipk_entry.delete(0, "end")
        self.ipk_sebelum_entry.delete(0, "end")
        self.bapak_entry.delete(0, "end")
        self.ibu_entry.delete(0, "end")
        self.listrik_entry.delete(0, "end")
        self.tunggakan_entry.delete(0, "end")
        self.tanggungan_entry.delete(0, "end")
        self.saudara_entry.delete(0, "end")

        # Hapus hasil keputusan di display box
        self.keputusan_display.config(state="normal")  # Buka akses untuk edit
        self.keputusan_display.delete("1.0", tk.END)   # Hapus teks lama
        self.keputusan_display.config(state="disabled")  # Kunci kembali agar tidak bisa diedit


    # Fungsi Menyimpan Data Inputan 
    def simpan_data_tunggal(self):
        # Nama file excel berdasarkan waktu
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"data_input_{timestamp}.xlsx"
        hasil_keputusan = self.proses_data()

        # Mengambil data dari form input
        data = [
            ["Semester", "IPK", "IPK 1 Semester Sebelum Daftar", "Penghasilan Bapak",
            "Penghasilan Ibu", "Jumlah Tagihan Listrik", "Jumlah Tunggakan",
            "Jumlah Tanggungan Orang Tua", "Jumlah Saudara", "Hasil Keputusan"],  # Header
            [self.semester_entry.get(), self.ipk_entry.get(), self.ipk_sebelum_entry.get(),
            self.bapak_entry.get(), self.ibu_entry.get(), self.listrik_entry.get(),
            self.tunggakan_entry.get(), self.tanggungan_entry.get(), self.saudara_entry.get(), hasil_keputusan]
        ]

        # Buat file Excel baru
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Data Input"

        # Masukkan data ke dalam sheet
        for row in data:
            sheet.append(row)

        try:
            # Simpan file Excel
            workbook.save(file_path)
            workbook.close()
            messagebox.showinfo("Sukses", f"Data berhasil disimpan ke {file_path}!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan data: {str(e)}")

    
    # Fungsi Proses Data
    def proses_data(self):
        try:
            # Muat model dari hasil model yang telah disimpan dari halaman modeling
            # model_path = "model_beasiswa.pkl"
            # model = joblib.load(model_path)

            # # Muat preprocessing dari halaman modeling
            # scaler_path = "scaler.pkl"
            # scaler = joblib.load(scaler_path) 

            model_data = joblib.load("model_beasiswa.pkl")
            model = model_data["model"]
            # selector = model_data["selector"]
            scaler = model_data["scaler"]
            selected_features = model_data["selected_features"]

            # Ambil data dari input form
            data_input = [
                float(self.semester_entry.get()),
                float(self.ipk_entry.get()),
                float(self.bapak_entry.get()),
                float(self.ibu_entry.get()),
                float(self.listrik_entry.get()),
                float(self.tanggungan_entry.get()),
                float(self.tunggakan_entry.get()),
                float(self.ipk_sebelum_entry.get()),
                float(self.saudara_entry.get())
            ]

            # Data frame yang akan di proses
            feature_names = [
                "Jumlah Semester Tempuh",
                "Jumlah Indeks Prestasi Kumulatif(BS Prestasi)",
                "Jumlah Gaji/penghasilan Bapak",
                "Jumlah Gaji/penghasilan Ibu",
                "Jumlah Tagihan Listrik",
                "Jumlah Tanggungan Yang Masih Studi",
                "Jumlah tunggakan pembayaran kuliah",
                "IPK 1 Smt Sebelum Daftar",
                "Jumlah Saudara"
            ]

            # Konversi ke dalam array numpy agar sesuai format input model
            # data_input_array = np.array([data_input]).reshape(1, -1)

        
            # Preprocessing 
            # data_input_array = scaler.transform(data_input_array)


            # Mengubah data input menjadi data frame sesuai dengan kolom di feature_names
            data_input = pd.DataFrame([data_input], columns=feature_names)

            # Menerapkan scaler ke data_input
            data_scaled_array = scaler.transform(data_input)

            data_scaled_data = pd.DataFrame(data_scaled_array,columns=feature_names)

            # Seleksi fitur menggunakan transform
            data_transformed = data_scaled_data[selected_features].values
            
            # Mendapatkan hasil prediksi dari model yang sudah dibuat dan mengambil nilai pertama dari array hasil prediksi
            hasil_prediksi = model.predict(data_transformed)[0]

            # Menentukan hasil berdasarkan prediksi
            hasil_keputusan = "Layak Menerima Beasiswa" if hasil_prediksi == 1 else "Tidak Layak Menerima Beasiswa"

            # Menampilkan hasil prediksi di display Box
            self.keputusan_display.config(state="normal")  # Buka akses untuk edit
            self.keputusan_display.delete("1.0", tk.END)  # Hapus teks lama
            self.keputusan_display.insert(tk.END, hasil_keputusan)  # Masukkan hasil baru
            self.keputusan_display.config(state="disabled")  # Kunci kembali agar tidak bisa diedit
            return hasil_keputusan

        except ValueError:
            messagebox.showerror("Error", "Harap masukkan angka yang valid!")
        except FileNotFoundError:
            messagebox.showerror("Error", "Model belum tersedia! Silakan latih dan simpan model terlebih dahulu.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")


    # Fungsi klasifikasi file dari file yang sudah dipilih
    def klasifikasi_file(self):
        try:
            # Memilih dataset dari file lokal
            file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
            if not file_path:
                return  # Jika pengguna batal memilih file, keluar dari fungsi
            
            # Muat model dan scaler yang telah disimpan
            model_data = joblib.load("model_beasiswa.pkl")
            model = model_data["model"]
            # selector = model_data["selector"]
            scaler = model_data["scaler"]
            selected_features = model_data["selected_features"]

            print("Model dan scaler berhasil dimuat.")

            # Baca file yang sudah dipilih
            df = pd.read_excel(file_path)

            # Memastikan dataset memiliki kolom fitur yang sesuai dengan data training
            expected_columns = [
                "Jumlah Semester Tempuh", "Jumlah Indeks Prestasi Kumulatif(BS Prestasi)",
                "Jumlah Gaji/penghasilan Bapak", "Jumlah Gaji/penghasilan Ibu",
                "Jumlah Tagihan Listrik", "Jumlah Tanggungan Yang Masih Studi",
                "Jumlah tunggakan pembayaran kuliah", "IPK 1 Smt Sebelum Daftar", "Jumlah Saudara"
            ]

            for col in expected_columns:
                if col not in df.columns:
                    messagebox.showerror("Error", f"Kolom {col} tidak ditemukan dalam file! Pastikan format sesuai.")
                    return

            # Memilih kolom dari df berdasarkan nama kolom di expected_columns
            df_input = df[expected_columns]

            # Preprocessing (scaling)
            df_scaled_array = scaler.transform(df_input)

            # Konversi kembali ke DataFrame untuk bisa pakai nama kolom
            df_scaled_df = pd.DataFrame(df_scaled_array, columns=expected_columns)

            # Ambil hanya kolom yang dipilih
            df_transformed = df_scaled_df[selected_features].values  # hasil akhirnya tetap array untuk predict

            # Prediksi menggunakan model
            predictions = model.predict(df_transformed)

            # Probabilitas hasil prediksi untuk per baris
            # prediction_probs = model.predict_proba(df_scaled)

            # Menambahkan hasil prediksi ke DataFrame setelah melakukan uji model
            df["Hasil Klasifikasi"] = ["Layak Menerima Beasiswa" if pred == 1 else "Tidak Layak Menerima Beasiswa" for pred in predictions]

            # Menampilkan probabilitas tertinggi dari setiap prediksi per baris
            # df["Tingkat Akurasi (%)"] = (prediction_probs.max(axis=1) * 100).round(2)

            # Hitung akurasi keseluruhan data test yang sudah diujian dengan model yang sudah dibuat
            if "Status" in df.columns:
                Y_true = df["Status"]  # Ambil label asli
                
                # Konversi Y_true ke numerik jika masih dalam format teks
                if Y_true.dtype == 'O':  # Jika tipe datanya objek (string)
                    Y_true = Y_true.map({'T': 0, 'Y': 1})  
                
                accuracy = accuracy_score(Y_true, predictions)  # Hitung akurasi

                # Menampilkan confusion matrix & classification report
                conf_matrix = confusion_matrix(Y_true, predictions)
                class_report = classification_report(Y_true, predictions)

                print(f"\nAkurasi Pengujian: {accuracy:.4f}")
                print("\nConfusion Matrix:")
                print(conf_matrix)
                print("\nClassification Report:")
                print(class_report)

                # Tambahkan hasil akurasi keseluruhan ke file Excel
                # df["Akurasi Pengujian"] = f"{accuracy:.4f}"

                messagebox.showinfo("Sukses", f"Pengujian selesai!\nAkurasi Pengujian: {accuracy:.4f}")

            else:
                messagebox.showinfo("Informasi", "Dataset tidak memiliki kolom 'Status', hanya klasifikasi yang dilakukan.")

            # Simpan hasil klasifikasi ke file baru
            hasil_file_path = file_path.replace(".xlsx", "_hasil.xlsx")
            df.to_excel(hasil_file_path, index=False)

            # Menampilkan pesan sukses
            messagebox.showinfo("Sukses", f"Hasil klasifikasi disimpan di:\n{hasil_file_path}")

        except FileNotFoundError:
            messagebox.showerror("Error", "Model atau scaler belum tersedia! Silakan latih dan simpan model terlebih dahulu.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
