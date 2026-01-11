import pandas as pd
import os

data = [
    {
        "No": 1,
        "店舗名": "NONBEI YOKOCHO",
        "タイプ": "Bar / Izakaya",
        "キーワード": "レトロ,体験,一杯,安心",
        "URL": "https://example.com/nonbei",
        "説明": "昭和の雰囲気が残る飲み屋街。狭い店内で地元の人と触れ合える。",
        "住所": "1-25-10 Shibuya, Shibuya-ku, Tokyo",
        "記入者": "Admin"
    },
    {
        "No": 2,
        "店舗名": "Cosmic Cafe",
        "タイプ": "Cafe",
        "キーワード": "トレンド,甘い休憩,静か,未知の一歩",
        "URL": "https://example.com/cosmic",
        "説明": "宇宙をテーマにしたコンセプトカフェ。異次元の体験ができる。",
        "住所": "1-1-1 Udagawacho, Shibuya-ku, Tokyo",
        "記入者": "Staff A"
    },
    {
        "No": 3,
        "店舗名": "Shibuya Sky",
        "タイプ": "Sightseeing",
        "キーワード": "トレンド,体験,にぎやか,安心",
        "URL": "https://shibuyastream.jp",
        "説明": "渋谷を一望できる展望台。スクランブル交差点を上から見下ろせる。",
        "住所": "2-24-12 Shibuya, Shibuya-ku, Tokyo",
        "記入者": "Staff B"
    },
    {
        "No": 4,
        "店舗名": "Ura-Shibu Records",
        "タイプ": "Shop",
        "キーワード": "レトロ,体験,静か,未知の一歩",
        "URL": "https://example.com/records",
        "説明": "裏渋谷にあるアナログレコード専門店。マニアックな選曲が魅力。",
        "住所": "10-1 Shinsencho, Shibuya-ku, Tokyo",
        "記入者": "Admin"
    },
    {
        "No": 5,
        "店舗名": "Neo Sushi Tokyo",
        "タイプ": "Restaurant",
        "キーワード": "トレンド,食,にぎやか,安心",
        "URL": "https://example.com/neosushi",
        "説明": "伝統的な寿司を現代風にアレンジ。SNS映えするメニューが多い。",
        "住所": "5-5-5 Jinnan, Shibuya-ku, Tokyo",
        "記入者": "Staff A"
    },
     {
        "No": 6,
        "店舗名": "Hidden Shrine",
        "タイプ": "Sightseeing",
        "キーワード": "レトロ,静か,未知の一歩,体験",
        "URL": "https://example.com/shrine",
        "説明": "ビルの谷間にひっそりと佇む神社。都会の喧騒を忘れられる。",
        "住所": "3-3-3 Shibuya, Shibuya-ku, Tokyo",
        "記入者": "Admin"
    }
]

df = pd.DataFrame(data)
os.makedirs('data', exist_ok=True)
df.to_excel('data/shibuya_spots.xlsx', index=False)
print("data/shibuya_spots.xlsx created successfully.")
