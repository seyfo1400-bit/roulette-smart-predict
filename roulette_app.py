import streamlit as st
import pandas as pd
from collections import Counter

st.set_page_config(page_title="Roulette Akıllı Tahmin", layout="wide")
st.title("🎲 Roulette Akıllı Tahmin & Analiz (Son 2 Sayıya Göre)")

# ---------- Sayı Girişi ----------
numbers_input = st.text_area(
    "Sayıları gir (0-36 arası, virgülle, alt alta veya boşlukla ayırabilirsin, maksimum 500 sayı):"
)

# ---------- Renk ve Bölge Verileri ----------
red_numbers = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
black_numbers = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}

def get_color(n):
    if n == 0: return "🟢 Yeşil"
    elif n in red_numbers: return "🔴 Kırmızı"
    elif n in black_numbers: return "⚫ Siyah"
    else: return "❓"

def get_zone(n):
    if n == 0: return "0"
    elif 1 <= n <= 12: return "1. Bölge"
    elif 13 <= n <= 24: return "2. Bölge"
    elif 25 <= n <= 36: return "3. Bölge"
    else: return "Bilinmiyor"

# ---------- Veri İşleme ----------
if numbers_input:
    numbers = [int(x) for x in numbers_input.replace("\n", ",").replace(" ", "").split(",") if x.strip().isdigit()]
    
    if len(numbers) > 500:
        st.warning("En fazla 500 sayı girebilirsiniz. Fazlası kesiliyor.")
        numbers = numbers[:500]

    df = pd.DataFrame(numbers, columns=["Sayı"])
    df["Renk"] = df["Sayı"].apply(get_color)
    df["Bölge"] = df["Sayı"].apply(get_zone)

    st.subheader("📌 Son 20 Girilen Sayı")
    st.write(df.tail(20))

    # ---------- Kullanıcı seçimi ----------
    first_num = st.number_input("Tahmin için son 2 sayıdan 1. sayı:", 0, 36, 10)
    second_num = st.number_input("Tahmin için son 2 sayıdan 2. sayı:", 0, 36, 0)

    # ---------- Son 2 sayıya göre olası takipçi sayılar ----------
    following = []
    for i in range(len(numbers)-2):
        if numbers[i] == first_num and numbers[i+1] == second_num:
            following.append(numbers[i+2])

    if following:
        st.subheader(f"🔎 ({first_num}, {second_num}) kombinasyonundan sonra gelen sayılar")
        follow_counts = pd.Series(following).value_counts().reset_index()
        follow_counts.columns = ["Sayı", "Geliş Sayısı"]
        follow_counts["Renk"] = follow_counts["Sayı"].apply(get_color)
        follow_counts["Bölge"] = follow_counts["Sayı"].apply(get_zone)
        follow_counts["Olasılık (%)"] = (follow_counts["Geliş Sayısı"] / follow_counts["Geliş Sayısı"].sum() * 100).round(2)
        st.table(follow_counts)
        st.bar_chart(follow_counts.set_index("Sayı")["Geliş Sayısı"])

        # ---------- Tahmin: en olası 3 sayı ----------
        follow_counts_sorted = follow_counts.sort_values("Olasılık (%)", ascending=False).head(3)
        st.subheader("🧠 Tahmin: En olası 3 sayı (son 2 sayıya göre)")
        st.table(follow_counts_sorted[["Sayı","Olasılık (%)","Renk","Bölge"]])
        
        # ---------- Renk ve Bölge Olasılıkları ----------
        st.subheader("🎨 Renk Olasılıkları")
        color_probs = follow_counts["Geliş Sayısı"].groupby(follow_counts["Renk"]).sum() / follow_counts["Geliş Sayısı"].sum() * 100
        color_probs = color_probs.round(2)
        st.table(color_probs.reset_index().rename(columns={"index":"Renk",0:"Olasılık (%)"}))

        st.subheader("📍 Bölge Olasılıkları")
        zone_probs = follow_counts["Geliş Sayısı"].groupby(follow_counts["Bölge"]).sum() / follow_counts["Geliş Sayısı"].sum() * 100
        zone_probs = zone_probs.round(2)
        st.table(zone_probs.reset_index().rename(columns={"index":"Bölge",0:"Olasılık (%)"}))

    else:
        st.info(f"({first_num}, {second_num}) kombinasyonundan sonra hiç sayı gelmemiş.")
else:
    st.info("Lütfen en az 2 sayı gir.")
