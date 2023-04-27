

https://user-images.githubusercontent.com/66292369/214657905-d0662b63-b1b0-4a06-8805-c10d4d7e0227.mp4



# English Translation
If you want to view the English repo, visit [here](https://github.com/Trisnox/Lost-Saga-AFK-Auto-Solver/tree/english)

# Lost-Saga-AFK-Auto-Solver
Macro untuk menyelesaikan mtk yang disebabkan oleh afk. Sebagai alternatif untuk rtl.

Setelah script dijalankan, script akan screenshot setiap beberapa detik yang ditentukan, jika menemukan box mtk maka script ini akan membaca dan menjawab pertanyaan tersebut.

# Cara Pemakaian
Install [python](https://www.python.org/downloads/), versi yang mana saja boleh (rekomendasi: 3.7>). Untuk Windows 7, gunakan [versi 3.8.6](https://www.python.org/downloads/release/python-386/). Untuk Windows XP, gunakan [versi 3.4.3](https://www.python.org/downloads/release/python-343/)

Pergi ke [releases](https://github.com/Trisnox/Lost-Saga-AFK-Auto-Solver/releases) dan pilih versi, lalu ekstrak file. Pastikan semua package sudah di install, jika belum jalankan cmd di folder tersebut lalu ketik `pip install -U -r requirements.txt` untuk install semua package yang dibutuhkan. Setelah itu install juga [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) dan tambahkan ke PATH jika belum. Jika semua kebutuhan sudah terpenuhi, gunakan cmd di folder tersebut menggunakan admin lalu ketik `main.py`.

Setelah GUI muncul, atur beberapa pilihan yang sesuai dengan yang digunakan, dan setelah selesai mengatur, klik tombol `Mulai` atau F6 di keyboard.

# To-do Priority
- [High] Resolusi otomatis. Dikarenakan box mtk selalu memiliki ukuran yang sama, code harus di tulis ulang supaya tidak perlu menggunakan resolusi spesifik, hanya penempatannya saja yang berbeda.
- [Low] Failproof. Karena adanya versi baru, setelah di tes, 100% dari 300+ gambar hasil percobaan berhasil semua, mungkin butuh lebih banyak tes. Karena script ini mengulang mtk tersebut jika tidak bisa dibaca, ini mungkin tidak dibutuhkan, kecuali kemungkinan gagal bacanya tinggi maka akan dicoba dibuatkan failproof.
- [Low] One time usage. Selama dijalankan, hanya akan bekerja jika menekan tombol F7, dan bisa digunakan lagi setelah selesai hingga script dihentikan. Ini hanya digunakan untuk para pengguna jitbit macro untuk sinergi macro yang sempurna.
- [Low] (Jika memungkinkan) Bundle script ke dalam bentuk exe. Dengan ini, tidak perlu install python, cukup tesseract saja.

# QNA
Q: Tidak ada input (enter/text), tapi OCR berhasil.\
A: ~~Coba masuk HQ, ketik sesuatu, keluar. Setelah ini biasanya akan bekerja.~~ Setelah diteliti, jalankan script ini dulu, lalu setelah itu jalankan Lost Saga. Entah kenapa scriptnya tidak bisa input jika Lost Saga dijalankan duluan.

Q: Di test input, chat box keluar, tapi tidak ada input `abc123`.\
A: Jika sudah melakukan solusi di atas, ini bug jika memakai `pynput` tetapi masih bekerja jika digunakan untuk menjawab mtk, lebih baik pakai `directinput`.

Q: Script hanya print `OCR gagal mengidentifikasi seluruh nomor, mencoba ulang`\
A: Bisa jadi karena
   - Window Lost Saga kepotong. Jika pencet tombol `test screenshot`, ini adalah contoh [screenshot yang bagus](https://media.discordapp.net/attachments/1097099248329306122/1097156717210501130/image.png), dan ini adalah contoh [screenshot yang jelek](https://media.discordapp.net/attachments/1097099248329306122/1097156850127999128/image.png) (lihat bagaimana window bagian atas Lost Saga kepotong, ini dikarenakan resolusi Lost Saga lebih besar daripada resolusi desktop)
   - Menggunakan resolusi yang salah
   - Menggunakan mode window yang salah
   
   Masalah ini mungkin akan diperbaiki saat resolusi otomatis dirilis.

Q: Bisa dipakai di Lost Saga client bahasa lain?\
A: Hanya untuk Lost Saga bahasa indonesia/inggris. Jika ingin pakai di client lain, screenshot kotak afk ([biasanya terlihat seperti ini](https://user-images.githubusercontent.com/66292369/215278517-69c7bb1f-1e73-4344-ad33-2d9b5de5663d.png)), crop tombol `enter` lalu tukar dengan komponen yang ada di folder `img`. Jika masih tidak bisa mungkin harus modifikasi script.

Q: Error: `ModuleNotFoundError: No module named '...'`\
A: 2 kemungkinan.\
   1, belum install modul menggunakan `pip install -r requirements.txt`\
   2, punya lebih dari 1 versi python berbeda, bisa di cek menggunakan `py -0`, lalu gunakan versi specifik menggunakan `py -versi.python`, contoh: `py -3.10-64 main.py`.
  
   
