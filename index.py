import pygame
import sys
import re
import time
import os
import random  

# Kita definisikan warna-warna cerah untuk lirik yang sudah selesai
BRIGHT_COLORS = [
    '\033[91m',  # Merah Cerah
    '\033[92m',  # Hijau Cerah
    '\033[94m',  # Biru Cerah
    '\033[95m',  # Magenta Cerah
    '\033[96m',  # Cyan Cerah
]
# Warna untuk "kelap-kelip" pada lirik aktif
ACTIVE_COLORS = [
    '\033[1m\033[93m',  # Kuning Cerah (Tebal)
    '\033[1m\033[97m',  # Putih Cerah (Tebal)
    '\033[1m\033[96m',  # Cyan Cerah (Tebal)
]
GREY = '\033[90m'   # Abu-abu untuk sisa teks
RESET = '\033[0m'  # Reset kembali ke warna normal
BOLD = '\033[1m'   # Tebal


def parse_lrc(filepath):
    lyrics = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                # Mencari timestamp ganda [mm:ss.cc][mm:ss.cc]...
                timestamps = re.findall(r'\[(\d{2}):(\d{2})\.(\d{2})\]', line)
                text = re.sub(r'\[.*?\]', '', line).strip()
                
                if text: # Hanya proses jika ada lirik
                    for ts in timestamps:
                        minutes, seconds, cents = int(ts[0]), int(ts[1]), int(ts[2])
                        time_ms = (minutes * 60 * 1000) + (seconds * 1000) + (cents * 10)
                        lyrics.append({'time_ms': time_ms, 'text': text})
    
        lyrics.sort(key=lambda x: x['time_ms'])
        
        # Hapus duplikat waktu (jika ada lirik yang sama persis di waktu yang sama)
        unique_lyrics = []
        if lyrics:
            unique_lyrics.append(lyrics[0])
            for i in range(1, len(lyrics)):
                if lyrics[i]['time_ms'] != lyrics[i-1]['time_ms']:
                    unique_lyrics.append(lyrics[i])
        lyrics = unique_lyrics

        for i in range(len(lyrics)):
            if i < len(lyrics) - 1:
                duration = lyrics[i+1]['time_ms'] - lyrics[i]['time_ms']
                # Jika durasi terlalu singkat (misal karena lirik instrumental), beri default
                lyrics[i]['duration_ms'] = max(200, duration) 
            else:
                lyrics[i]['duration_ms'] = 5000  # Durasi default untuk baris terakhir
                
        return lyrics
    except FileNotFoundError:
        print(f"Error: File lirik '{filepath}' tidak ditemukan.")
        return None
    except Exception as e:
        print(f"Error saat mem-parsing LRC: {e}")
        return None

# 2. Program Utama
def main():
    if len(sys.argv) != 3:
        print("Penggunaan: python karaoke_py.py lirik.lrc lagu.mp3")
        sys.exit(1)
        
    lrc_file, mp3_file = sys.argv[1], sys.argv[2]
    
    lyrics = parse_lrc(lrc_file)
    if not lyrics:
        sys.exit(1)

    try:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(mp3_file)
    except pygame.error as e:
        print(f"Error saat memuat file MP3: {e}")
        sys.exit(1)

    # ### PERUBAHAN ###: Header dibuat lebih "heboh"
    print(f"{BOLD}{random.choice(BRIGHT_COLORS)}✨🎤 Karaoke CLI Python 🎤✨{RESET}")
    print(f"Lagu: {BOLD}{os.path.basename(mp3_file)}{RESET}")
    print("Tekan Ctrl+C untuk keluar.")
    print("=" * 40)
    print(f"\n... 🎶 {BOLD}Build by Baihaqi Abdul Hakim{RESET} 🎶 ...\n")

    pygame.mixer.music.play()
    
    first_lyric_time = lyrics[0]['time_ms'] if lyrics else float('inf')
    last_active_index = -1

    try:
        while pygame.mixer.music.get_busy():
            current_time = pygame.mixer.music.get_pos()

            if current_time < first_lyric_time:
                # Tampilkan pesan "Menunggu..." dengan efek "loading"
                dots = '.' * (int(time.time() * 2) % 4)
                print(f"\r{GREY}Menunggu musik{dots}{' ' * 20}{RESET}", end="", flush=True)
                time.sleep(0.1)
                continue

            active_index = -1
            for i, line in enumerate(lyrics):
                if current_time >= line['time_ms']:
                    active_index = i
                else:
                    break
            
            if active_index != -1:
                if active_index != last_active_index:
                    if last_active_index != -1:
                        prev_line_text = lyrics[last_active_index]['text']
                        # ### PERUBAHAN ###: Finalisasi baris sebelumnya dengan WARNA ACAK
                        color = random.choice(BRIGHT_COLORS)
                        print(f"\r{BOLD}{color}{prev_line_text}{RESET}{' ' * 20}")
                    
                    if last_active_index == -1:
                        # Membersihkan pesan "Menunggu..." saat lirik pertama muncul
                        print('\r' + ' ' * 40 + '\r', end='')

                    last_active_index = active_index

                # --- PERUBAHAN DI SINI (LOGIKA ANIMASI) ---
                line = lyrics[active_index]
                full_text = line['text']
                
                # Kalkulasi progres animasi
                line_start_time = line['time_ms']
                line_duration = max(1, line['duration_ms'])
                elapsed_in_line = current_time - line_start_time
                progress = min(1.0, elapsed_in_line / line_duration)
                chars_to_show = int(len(full_text) * progress)
                
                # Membangun string yang akan ditampilkan
                animated_text = full_text[:chars_to_show]
                remaining_text = full_text[chars_to_show:]
    
                # Pilih warna aktif secara acak di setiap frame
                active_color = random.choice(ACTIVE_COLORS)
                
                # Gabungkan teks (Tebal/Warna-warni) + (Abu-abu sisa)
                display_line = f"{active_color}{animated_text}{RESET}{GREY}{remaining_text}{RESET}"
                
                # Cetak dengan padding spasi untuk menimpa sisa baris sebelumnya
                print(f"\r{display_line}{' ' * 20}", end="", flush=True)

            time.sleep(0.05) # Loop sedikit lebih cepat untuk "kelap-kelip" yang lebih halus

    except KeyboardInterrupt:
        print() 
        print("\nKaraoke dihentikan.")
    finally:
        # Finalisasi baris terakhir setelah loop selesai
        if last_active_index != -1:
            final_line_text = lyrics[last_active_index]['text']
            # ### PERUBAHAN ###: Finalisasi baris terakhir juga dengan WARNA ACAK
            color = random.choice(BRIGHT_COLORS)
            print(f"\r{BOLD}{color}{final_line_text}{RESET}{' ' * 20}")
            
        pygame.mixer.music.stop()
        pygame.quit()
        print(f"\n{BOLD}{random.choice(BRIGHT_COLORS)}🎉 Selesai! 🎉{RESET}")


if __name__ == '__main__':
    main()
    
    # python index.py fajasekali.lrc fajasekali.mp3