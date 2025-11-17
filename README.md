✨🎤 Karaoke CLI Python 🎤✨

Sebuah proyek oleh Baihaqi Abdul Hakim

Ini adalah skrip Python sederhana yang mengubah terminal Anda menjadi mesin karaoke. Skrip ini memutar file audio .mp3 dan menampilkan lirik dari file .lrc secara sinkron, lengkap dengan animasi progresif dan pewarnaan yang meriah di command line.

Demo Tampilan

Bayangkan tampilan ini di terminal Anda, di mana baris aktif "terisi" warnanya seiring lagu berjalan:

✨🎤 Karaoke CLI Python 🎤✨
Lagu: fajasekali.mp3
Tekan Ctrl+C untuk keluar.
========================================

... 🎶 Build by Baihaqi Abdul Hakim 🎶 ...


[Lirik sebelumnya, tampil dalam warna-warni cerah]
Dan terjadi lagi...

[Baris aktif: bagian KUNING/PUTIH tebal adalah progres, ABU-ABU adalah sisa]
Kisah lama yang terula...ng kembali


Fitur Utama

🎵 Pemutaran Audio: Menggunakan pygame.mixer untuk memutar file .mp3.

📜 Sinkronisasi Lirik: Mem-parsing file .lrc standar untuk mencocokkan lirik dengan timestamp musik.

✨ Animasi Progresif: Lirik yang sedang aktif dianimasi huruf per huruf (diwarnai) sesuai dengan durasi baris tersebut, memberikan efek "karaoke" yang nyata.

🎨 Penuh Warna (ANSI):

Lirik aktif yang sedang berjalan akan berkedip-kedip (Kuning, Putih, Cyan).

Lirik yang sudah selesai akan diberi warna cerah acak (Merah, Hijau, Biru, dll.).

Sisa lirik pada baris aktif (yang belum dinyanyikan) berwarna Abu-abu.

🖥️ Tampilan CLI Murni: Berjalan sepenuhnya di dalam terminal Anda tanpa GUI.

Persyaratan (Requirements)

Python 3

pygame (untuk memutar audio)

Cara Instalasi

Clone Repositori (Opsional)
Jika ini adalah repositori, clone:

git clone [URL_REPO_ANDA]
cd [NAMA_REPO]


Atau cukup unduh file script python (.py) ini.

Install Pygame
Anda harus menginstal pygame menggunakan pip:

pip install pygame


Cara Penggunaan

Pastikan Anda memiliki file lagu (.mp3) dan file lirik (.lrc) yang sudah sinkron.

Buka terminal atau command prompt Anda.

Jalankan skrip dengan format:

python [nama_skrip].py [file_lirik.lrc] [file_lagu.mp3]


Contoh:
Jika nama skrip Anda karaoke_py.py, dan Anda punya file fajasekali.lrc dan fajasekali.mp3:

python karaoke_py.py fajasekali.lrc fajasekali.mp3


Nikmati musik dan nyanyikan liriknya!

Tekan Ctrl + C untuk keluar dari program kapan saja.
