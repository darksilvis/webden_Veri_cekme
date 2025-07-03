import requests
from bs4 import BeautifulSoup

url = "https://www.imdb.com/chart/top"

# Güncel User-Agent header
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(url, headers=headers)
print("HTTP Durumu:", response.status_code)  # 200 olmalı

soup = BeautifulSoup(response.content, "html.parser")

try:
    min_rating = float(input("Minimum Rating'i giriniz (0-10 arası): "))
except ValueError:
    print("Geçersiz sayı formatı!")
    exit()

# Güncel CSS seçiciler
filmler = soup.select("li.ipc-metadata-list-summary-item")
print(f"Toplam {len(filmler)} film bulundu")  # Debug için

for sira, film in enumerate(filmler, 1):
    try:
        # Başlık ve yıl bilgisi
        baslik_blok = film.select_one("h3.ipc-title__text")
        if not baslik_blok: continue

        baslik_text = baslik_blok.text.split(maxsplit=1)[1]  # Sıra numarasını kaldır
        baslik, yil = baslik_text.rsplit(' ', 1)  # Yıl bilgisini ayır
        yil = yil.strip('()')

        # Rating bilgisi
        rating_blok = film.select_one("span.ipc-rating-star")
        if not rating_blok: continue

        rating = float(rating_blok.text.split()[0])

        # Filtreleme ve yazdırma
        if rating >= min_rating:
            print(f"{sira}. {baslik} ({yil}) - Rating: {rating:.1f}")

    except Exception as e:
        print(f"Hata oluştu: {e} - Film atlandı")

print("\nFiltreleme tamamlandı!")