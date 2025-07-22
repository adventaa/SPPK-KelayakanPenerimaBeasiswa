import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split, KFold, GridSearchCV, cross_val_score
from sklearn.feature_selection import mutual_info_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (confusion_matrix, accuracy_score, classification_report)
from sklearn.tree import export_text
from sklearn.feature_selection import SelectFromModel

class ModelingTab:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)

        # Mengatur grid agar otomatis menyesuaikan ukuran layar
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)  # Untuk tampilan data
        self.frame.grid_rowconfigure(3, weight=1)  # Untuk hasil preprocessing

        # Button tampil data
        self.btn_tampil_data = ttk.Button(self.frame, text="Tampilkan Data", command=self.load_data)
        self.btn_tampil_data.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Frame untuk teks dan scrollbars (data_display)
        self.data_frame = ttk.Frame(self.frame)
        self.data_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        # Scrollbar vertikal untuk data_display
        self.data_v_scroll = tk.Scrollbar(self.data_frame, orient=tk.VERTICAL)
        self.data_v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Scrollbar horizontal untuk data_display
        self.data_h_scroll = tk.Scrollbar(self.data_frame, orient=tk.HORIZONTAL)
        self.data_h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # Display box hasil tampil data
        self.data_display = tk.Text(self.data_frame, height=10, width=50, wrap="none",
                                    yscrollcommand=self.data_v_scroll.set,
                                    xscrollcommand=self.data_h_scroll.set)
        self.data_display.pack(fill=tk.BOTH, expand=True)

        # Hubungkan scrollbar ke data_display
        self.data_v_scroll.config(command=self.data_display.yview)
        self.data_h_scroll.config(command=self.data_display.xview)

        # Button preprocessing data
        self.btn_preprocessing = ttk.Button(self.frame, text="Data Preprocessing", command=self.preprocess_data)
        self.btn_preprocessing.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        # Frame untuk teks dan scrollbars (preprocess_display)
        self.preprocess_frame = ttk.Frame(self.frame)
        self.preprocess_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        # Scrollbar vertikal untuk preprocess_display
        self.preprocess_v_scroll = tk.Scrollbar(self.preprocess_frame, orient=tk.VERTICAL)
        self.preprocess_v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Scrollbar horizontal untuk preprocess_display
        self.preprocess_h_scroll = tk.Scrollbar(self.preprocess_frame, orient=tk.HORIZONTAL)
        self.preprocess_h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # Display box hasil preprocessing data
        self.preprocess_display = tk.Text(self.preprocess_frame, height=10, width=50, wrap="none",
                                          yscrollcommand=self.preprocess_v_scroll.set,
                                          xscrollcommand=self.preprocess_h_scroll.set)
        self.preprocess_display.pack(fill=tk.BOTH, expand=True)

        # Hubungkan scrollbar ke preprocess_display
        self.preprocess_v_scroll.config(command=self.preprocess_display.yview)
        self.preprocess_h_scroll.config(command=self.preprocess_display.xview)

        # Label & Input untuk K-fold dan Tree
        self.form_frame = ttk.Frame(self.frame)
        self.form_frame.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        ttk.Label(self.form_frame, text="Jumlah K-fold").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.kfold_entry = ttk.Entry(self.form_frame, width=5)
        self.kfold_entry.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(self.form_frame, text="Jumlah Tree").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.tree_entry = ttk.Entry(self.form_frame, width=5)
        self.tree_entry.grid(row=2, column=1, padx=5, pady=2, sticky="w")

        # Button Proses
        self.btn_proses = ttk.Button(self.form_frame, text="Proses", command=self.process_model)
        self.btn_proses.grid(row=2, column=2, padx=100, pady=5, sticky="w")

        # Label Akurasi 
        self.accuracy_label = ttk.Label(self.form_frame, text="Akurasi")
        self.accuracy_label.grid(row=0, column=4, padx=120, pady=5, sticky="w")

        # Display Box Menampilkan Hasil Akurasi
        self.accuracy_display = tk.Text(self.form_frame, height=2, width=10, state="disabled")
        self.accuracy_display.grid(row=2, column=4, padx=100, pady=5, sticky="w")

        # Button simpan model
        self.btn_simpan_model = ttk.Button(self.form_frame, text="Simpan Model", command=self.save_model)
        self.btn_simpan_model.grid(row=2, column=6, padx=100, pady=5, sticky="w")

        # Tombol untuk menampilkan aturan pohon dari Random Forest
        # self.btn_lihat_rules = ttk.Button(self.form_frame, text="Lihat Rules", command=self.show_tree_rules)
        # self.btn_lihat_rules.grid(row=2, column=7, padx=10, pady=5, sticky="w")



    # Fungsi untuk menampilkan data beasiswa dari excel
    def load_data(self):
        # Hapus data lama
        self.data_display.delete(1.0, tk.END)  
        try:
            # Baca data
            data = pd.read_excel('Beasiswa-SDSF.xlsx')
            self.data_display.insert(tk.END, data.to_string(index=False))  # Tampilkan data
        except Exception as e:
            self.data_display.insert(tk.END, f"Gagal memuat data: {e}\n")


    # Fungsi untuk preprocessing data dan menampilkan hasil preprocessing
    def preprocess_data(self):
        self.preprocess_display.delete(1.0, tk.END)  # Hapus tampilan sebelumnya
        try:
            # Baca data
            data = pd.read_excel('Beasiswa-SDSF.xlsx')

            # == PREPROCESSING DATA ==
            # Data cleaning
            data_drop = data.dropna().reset_index(drop=True)

            # Menghapus kolom yang tidak diperlukan
            data_beasiswa = data_drop.drop(columns=[
                'No', 'Nama Beasiswa', 'Periode', 'Prodi',
                'Id Mahasiswa', 'Propinsi Asal', 'Propinsi Asal Sekolah',
                'IPK 1 Smt Setelah Daftar'
            ])

            # Hapus baris dengan "Jumlah Tanggungan Yang Masih Studi" > 10
            data_beasiswa = data_beasiswa.drop(data_beasiswa[data_beasiswa["Jumlah Tanggungan Yang Masih Studi"] > 10].index)
            data_beasiswa = data_beasiswa.reset_index(drop=True)

            # Data transformation: Encoding kolom 'Status'
            label_encoder = LabelEncoder()
            data_beasiswa['Status'] = label_encoder.fit_transform(data_beasiswa['Status'])

            # Data normalization dengan MinMaxScaler
            scaler = MinMaxScaler()
            kolom_normalisasi = [
                'Jumlah Semester Tempuh',
                'Jumlah Indeks Prestasi Kumulatif(BS Prestasi)',
                'Jumlah Gaji/penghasilan Bapak',
                'Jumlah Gaji/penghasilan Ibu',
                'Jumlah Tagihan Listrik',
                'Jumlah Tanggungan Yang Masih Studi',
                'Jumlah tunggakan pembayaran kuliah',
                'IPK 1 Smt Sebelum Daftar',
                'Jumlah Saudara'
            ]

            data_beasiswa[kolom_normalisasi] = scaler.fit_transform(data_beasiswa[kolom_normalisasi])

            # Jumlah round untuk menampilkan jumlah angka dibelakang koma
            # data_beasiswa = data_beasiswa.round(6)

            # desimal_per_kolom = {
            #     'Jumlah Semester Tempuh': 2,
            #     'Jumlah Indeks Prestasi Kumulatif(BS Prestasi)': 4,
            #     'Jumlah Gaji/penghasilan Bapak': 2,
            #     'Jumlah Gaji/penghasilan Ibu': 2,
            #     'Jumlah Tagihan Listrik': 1,
            #     'Jumlah Tanggungan Yang Masih Studi': 2,
            #     'Jumlah tunggakan pembayaran kuliah': 3,
            #     'IPK 1 Smt Sebelum Daftar': 4,
            #     'Jumlah Saudara': 1
            # }

            # for kolom, desimal in desimal_per_kolom.items():
            #     data_beasiswa[kolom] = data_beasiswa[kolom].apply(lambda x: round(x, desimal))

            # Simpan scaler
            joblib.dump(scaler, "scaler.pkl")
            
            # Tampilkan hasil preprocessing di GUI
            self.preprocess_display.insert(tk.END, data_beasiswa.to_string(index=False))

            # Simpan hasil preprocessing
            self.processed_data = data_beasiswa

            print("Preprocessing Selesai!")

        except Exception as e:
            self.preprocess_display.insert(tk.END, f"Error saat preprocessing: {e}\n")
        

    # Fungsi untuk proses model menggunakan data hasil preprocessing + jumlah k fold + jumlah tree
    def process_model(self):
        try:
            # Validasi data
            if self.processed_data is None:
                print("Harap jalankan preprocessing terlebih dahulu!")
                return
            
            # Ambil nilai dari entry GUI
            num_folds = int(self.kfold_entry.get())
            num_estimators = int(self.tree_entry.get())
            print(f"🔹 Memulai Model Training dengan K-Fold={num_folds}, Trees={num_estimators}...")

            # Ambil data dari processed_data
            data_beasiswa = self.processed_data
            X = data_beasiswa.drop('Status', axis=1)
            Y = data_beasiswa['Status']

            # Split data (80% Train, 20% Test)
            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

            # K-Fold cross-validation
            kfold = KFold(n_splits=num_folds, shuffle=True, random_state=42)
            for train_index, test_index in kfold.split(X):
                X_train, X_test = X.iloc[train_index], X.iloc[test_index]
                Y_train, Y_test = Y.iloc[train_index], Y.iloc[test_index]

            # Feature Selection
            selector = SelectFromModel(RandomForestClassifier(n_estimators=num_estimators, random_state=42, criterion='entropy'))
            selector.fit(X_train, Y_train)

            # Transformasi fitur
            X_train_selected = selector.transform(X_train)
            X_test_selected = selector.transform(X_test)
            selected_features = X.columns[selector.get_support()]
            self.selected_features = list(selected_features)  # Simpan untuk disimpan di model
            print("Fitur Terpilih:", self.selected_features)

            # Train model akhir dengan fitur yang sudah terpilih
            model = RandomForestClassifier(n_estimators=num_estimators, random_state=42, criterion='entropy')
            model.fit(X_train_selected, Y_train)
            predictions = model.predict(X_test_selected)

            # Simpan model ke dalam objek self
            self.model = model
            self.selector = selector
            selected_features = X_train.columns[selector.get_support()].tolist()

            # Evaluasi model
            from sklearn.metrics import (
                accuracy_score, confusion_matrix, classification_report
            )
            accuracy = accuracy_score(Y_test, predictions)
            print(f"\nAccuracy: {accuracy:.4f}")
            print("\nConfusion Matrix:\n", confusion_matrix(Y_test, predictions))
            print("\nClassification Report:\n", classification_report(Y_test, predictions))

            # Tampilkan akurasi di GUI
            self.accuracy_display.config(state="normal")
            self.accuracy_display.delete(1.0, tk.END)
            self.accuracy_display.insert(tk.END, f"{accuracy:.4f}")
            self.accuracy_display.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", "Masukkan angka yang valid untuk K-Fold dan Tree!")
            print(f"Error: {e}")


    # Fungsi untuk menyimpan hasil model yang sudah dibuat
    def save_model(self):
        try:
            #  hasattr adalah fungsi untuk memeriksa sebuah objek memiliki atribut tertentu
            #  untuk memeriksa self.model sudah ada sebelum disimpan, jika tidak ada maka muncul pesan error
            if not hasattr(self, 'model') or self.model is None:
                messagebox.showerror("Error", "Model belum dibuat! Jalankan proses training terlebih dahulu.")
                return
            
            # Menyimpan model
            
            simpan_model = {
                "model" : self.model,
                # "selector" : self.selector,
                "scaler" : joblib.load("scaler.pkl"),
                "selected_features" : self.selected_features
            }

            joblib.dump(simpan_model, "model_beasiswa.pkl")
            
            # Menampilkan pesan berhasil
            messagebox.showinfo("Sukses", f"Model berhasil disimpan!")
            print(f"Model disimpan di: {simpan_model}")
            

        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan model: {str(e)}")
            print(f"Gagal menyimpan model: {str(e)}")

    # Fungsi untuk menampilkan aturan dari decision tree pertama
    # def show_tree_rules(self):
    #     try:
    #         if not hasattr(self, 'model') or self.model is None:
    #             messagebox.showerror("Error", "Model belum dibuat! Jalankan proses training terlebih dahulu.")
    #             return

    #         # Ambil rules dari tree pertama di random forest
    #         rules = export_text(self.model.estimators_[1],
    #                             feature_names=list(self.processed_data.drop('Status', axis=1).columns))

    #         # Buat jendela popup untuk menampilkan rules
    #         rule_window = tk.Toplevel()
    #         rule_window.title("Rule Random Forest")

    #         # Gunakan ScrolledText agar bisa scroll panjang
    #         text_area = tk.Text(rule_window, wrap=tk.WORD, width=100, height=30)
    #         text_area.insert(tk.END, rules)
    #         text_area.pack(fill=tk.BOTH, expand=True)

    #         # Scrollbar vertikal
    #         scrollbar = ttk.Scrollbar(rule_window, command=text_area.yview)
    #         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    #         text_area.config(yscrollcommand=scrollbar.set)

    #     except Exception as e:
    #         messagebox.showerror("Error", f"Gagal menampilkan aturan pohon: {str(e)}")
