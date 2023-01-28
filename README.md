

https://user-images.githubusercontent.com/66292369/214657905-d0662b63-b1b0-4a06-8805-c10d4d7e0227.mp4



# Lost-Saga-AFK-Auto-Solver
Macro untuk menyelesaikan mtk yang disebabkan oleh afk. Sebagai alternatif untuk rtl.

Setelah script dijalankan, script akan screenshot setiap beberapa detik yang ditentukan, jika menemukan box mtk maka script ini akan membaca dan menjawab pertanyaan tersebut.

# Cara Pemakaian
Pergi ke [releases](https://github.com/Trisnox/Lost-Saga-AFK-Auto-Solver/releases) dan pilih versi, lalu ekstrak file. Pastikan semua package sudah di install, jika belum jalankan cmd di folder tersebut lalu ketik `pip install -U -r requirements.txt` untuk install semua package yang dibutuhkan. Setelah itu install juga [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) dan tambahkan ke PATH jika belum. Jika semua kebutuhan sudah terpenuhi, gunakan cmd di folder tersebut menggunakan admin lalu ketik `main.py`.

Setelah GUI muncul, atur beberapa pilihan yang sesuai dengan yang digunakan, dan setelah selesai mengatur, klik tombol `Mulai` atau F6 di keyboard.

# To-do
- Resolusi otomatis

# QNA
Q: Tidak ada input (enter/text), tapi OCR berhasil.
A: Coba masuk HQ, ketik sesuatu, keluar. Setelah ini biasanya akan bekerja.

Q: Di test input, chat box keluar, tapi tidak ada input `abc123`.
A: Jika sudah melakukan solusi di atas, ini bug jika memakai `pynput` tetapi masih bekerja jika digunakan untuk menjawab mtk, lebih baik pakai `directinput`.

Q: Bisa dipakai di lost saga client bahasa lain?
A: Hanya untuk lost saga bahasa indonesia/inggris. Jika ingin pakai di client lain, screenshot kotak afk (biasanya terlihat seperti ini), crop tombol `enter` lalu tukar dengan komponen yang ada di folder `img`. Kalo masih tidak bisa mungkin harus modifikasi script.

Q: Error: `ModuleNotFoundError: No module named '...'`
A: 2 kemungkinan.\
   1, belum install modul menggunakan `pip install -r requirements.txt`\
   2, punya lebih dari 1 versi python berbeda, bisa di cek menggunakan `py -0`, lalu gunakan versi specifik menggunakan `py -versi.python`, contoh: `py -3.10-64 main.py`.
  
   