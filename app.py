import streamlit as st
import time
from datetime import datetime, timedelta
import uuid
import json
import os

st.set_page_config(page_title="Ambulance4all | Κέντρο Επιχειρήσεων", layout="wide")

# --- ΑΡΧΕΙΑ ΜΟΝΙΜΗΣ ΑΠΟΘΗΚΕΥΣΗΣ ---
DATA_FILE = "ambulance_storage.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "names": ["Τ12", "Τ16", "Τ16Β", "Τ16Δ", "Κενό 5", "Κενό 6"],
        "trips": []
    }

def save_data():
    names_to_save = [
        st.session_state.get("name_1", "Τ12"),
        st.session_state.get("name_2", "Τ16"),
        st.session_state.get("name_3", "Τ16Β"),
        st.session_state.get("name_4", "Τ16Δ"),
        st.session_state.get("name_5", "Κενό 5"),
        st.session_state.get("name_6", "Κενό 6")
    ]
    data = {
        "names": names_to_save,
        "trips": st.session_state.trips_list
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

saved_data = load_data()

# --- ΑΡΧΙΚΟΠΟΙΗΣΗ ΜΝΗΜΗΣ (SESSION STATE) ---
if "name_1" not in st.session_state: st.session_state["name_1"] = saved_data["names"][0]
if "name_2" not in st.session_state: st.session_state["name_2"] = saved_data["names"][1]
if "name_3" not in st.session_state: st.session_state["name_3"] = saved_data["names"][2]
if "name_4" not in st.session_state: st.session_state["name_4"] = saved_data["names"][3]
if "name_5" not in st.session_state: st.session_state["name_5"] = saved_data["names"][4]
if "name_6" not in st.session_state: st.session_state["name_6"] = saved_data["names"][5]

if "amb" not in st.session_state:
    st.session_state.amb = {}
    for i in range(1, 7):
        st.session_state.amb[i] = {
            "crew": "", "origin": "", "dest": "", "target": None, "total_mins": 20, "active": False, "sound_played": False
        }

if "trips_list" not in st.session_state:
    st.session_state.trips_list = saved_data["trips"]

# --- ΠΛΕΥΡΙΚΟ ΜΕΝΟΥ (Η ΟΝΟΜΑΤΟΣΙΑ ΑΦΑΙΡΕΘΗΚΕ) ---
st.sidebar.markdown("### 🚑 Ambulance4all")
menu = st.sidebar.radio("Μεταβείτε στην ενότητα:", [
    "🏠 Εταιρικό Προφίλ", 
    "⏱️ Live Παρακολούθηση Στόλου", 
    "📝 Προσθήκη Διαδρομών",
    "📅 Ημερήσιο Πρόγραμμα (Ημερολόγιο)"
])

current_names = [
    st.session_state["name_1"].strip() or "Όχημα 1",
    st.session_state["name_2"].strip() or "Όχημα 2",
    st.session_state["name_3"].strip() or "Όχημα 3",
    st.session_state["name_4"].strip() or "Όχημα 4",
    st.session_state["name_5"].strip() or "Όχημα 5",
    st.session_state["name_6"].strip() or "Όχημα 6"
]

def delete_trip(trip_id):
    st.session_state.trips_list = [t for t in st.session_state.trips_list if t["id"] != trip_id]
    save_data()

# --- 1. ΕΤΑΙΡΙΚΟ ΠΡΟΦΙΛ ---
if menu == "🏠 Εταιρικό Προφίλ":
    st.markdown("<h1 style='text-align: center; color: #CD1818; font-size: 50px; font-weight: bold;'>🚑 Ambulance4all</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #333; font-weight: normal;'>Σύγχρονα Ασθενοφόρα & Ασφαλείς Διακομιδές</h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: #666; font-style: italic; margin-bottom: 30px;'>Αμεσότητα • Ασφάλεια • Επαγγελματική Φροντίδα</h5>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("""
    ### 🎯 Η Αποστολή μας
    Με απόλυτο σεβασμό στην ανθρώμινη ζωή, η **Ambulance4all** αποτελεί το πρότυπο κέντρο διαχείρισης και εκτέλεσης επειγουσών και προγραμματισμένων ιατρικών διακομιδών. Συνδυάζοντας την τεχνολογική υπεροχή με την επιχειρησιακή ετοιμότητα, προσφέρουμε ολοκληρωμένες υπηρεσίες υγείας, αποτελώντας τον πλέον αξιόπιστο συνεργάτη για νοσηλευτικά ιδρύματα, ασφαλιστικούς φορείς και ιδιώτες.

    ### 🛡️ Πυλώνες της Υπεροχής μας
    * **⚡ Άμεση Ανταπόκριση 24/7:** Λειτουργούμε σε κατάσταση πλήρους επιχειρησιακής ετοιμότητας 365 ημέρες τον χρόνο, εξασφαλίζοντας ελάχιστους χρόνους αναμονής.
    * **🚑 Στόλος Υψηλών Προδιαγραφών:** Τα ιδιωτικά ασθενοφόρα μας είναι πλήρως εξοπλισμένα με ιατροτεχνολογικά συστήματα τελευταίας γενιάς, τηρώντας τα αυστηρότερα διεθνή πρωτόκολλα ασφαλείας.
    * **👨‍⚕️ Εξειδικευμένα Πληρώματα:** Στελεχωνόμαστε αποκλειστικά από πιστοποιημένους διασώστες, έμπειρους οδηγούς και εξειδικευμένο ιατρικό προσωπικό για τη βέλτιστη διαχείριση κάθε περιστατικού.
    * **🌐 Ψηφιακός Έλεγχος:** Επενδύουμε σε σύγχρονα συστήματα ζωντανής παρακολούθησης και διαχείρισης στόλου για τον απόλυτο συντονισμό των δρομολογίων.
    """)
