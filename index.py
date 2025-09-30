import pygame
import sys
import re
import time
import os

def parse_lrc(filepath):
    lyrics = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.search(r'\[(\d{2}):(\d{2})\.(\d{2})\](.*)', line)
                if match:
                    minutes, seconds, cents = int(match.group(1)), int(match.group(2)), int(match.group(3))
                    text = match.group(4).strip()
                    time_ms = (minutes * 60 * 1000) + (seconds * 1000) + (cents * 10)
                    if text:
                        lyrics.append({'time_ms': time_ms, 'text': text})
        
        lyrics.sort(key=lambda x: x['time_ms'])
        
        for i in range(len(lyrics)):
            if i < len(lyrics) - 1:
                duration = lyrics[i+1]['time_ms'] - lyrics[i]['time_ms']
                lyrics[i]['duration_ms'] = duration
            else:
                lyrics[i]['duration_ms'] = 5000 
                
        return lyrics
    except FileNotFoundError:
        print(f"Error: File lirik '{filepath}' tidak ditemukan.")
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

    # Header dicetak sekali saja
    print("🎤 Karaoke CLI (Scrolling) dengan Python 🎤")
    print(f"Lagu: {os.path.basename(mp3_file)}")
    print("Tekan Ctrl+C untuk keluar.")
    print("=" * 40)
    print("\n... bersiap ...")

    pygame.mixer.music.play()
    
    first_lyric_time = lyrics[0]['time_ms'] if lyrics else float('inf')
    last_active_index = -1

    try:
        while pygame.mixer.music.get_busy():
            current_time = pygame.mixer.music.get_pos()

            if current_time < first_lyric_time:
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
                        # Finalisasi baris sebelumnya dengan warna putih
                        print(f"\r\033[97m{prev_line_text}\033[0m{' ' * 20}")
                    
                    if last_active_index == -1:
                        print('\r' + ' ' * 20 + '\r', end='')

                    last_active_index = active_index

                # --- PERUBAHAN DI SINI ---
                # Animasi baris aktif (kuning) tanpa karakter tambahan
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
                
                # Gabungkan teks kuning (yang sudah muncul) dan abu-abu (sisa)
                display_line = f"\033[1m\033[93m{animated_text}\033[0m\033[90m{remaining_text}\033[0m"
                
                # Cetak dengan padding spasi untuk menimpa sisa baris sebelumnya
                print(f"\r{display_line}{' ' * 20}", end="", flush=True)

            time.sleep(0.05)

    except KeyboardInterrupt:
        print() 
        print("\nKaraoke dihentikan.")
    finally:
        # Finalisasi baris terakhir setelah loop selesai
        if last_active_index != -1:
            final_line_text = lyrics[last_active_index]['text']
            print(f"\r\033[97m{final_line_text}\033[0m{' ' * 20}")
            
        pygame.mixer.music.stop()
        pygame.quit()
        print("Selesai.")


if __name__ == '__main__':
    main()