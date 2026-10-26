import streamlit as st
import time
from datetime import datetime, timedelta
import uuid
import json
import os

st.set_page_config(page_title="Ambulance4all | Κέντρο Επιχειρήσεων", layout="wide")

# --- ΑΡΧΕΙΑ ΜΟΝΙΜΗΣ ΑΠΟΘΗΚΕΥΣΗΣ ---
DATA_FILE = "ambulance_data.json"

def load_data():
    """Φορτώνει τα δεδομένα από το αρχείο αν υπάρχει, αλλιώς επιστρέφει αρχικές τιμές"""
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
    """Αποθηκεύει τα ονόματα και τις διακομιδές μόνιμα στο αρχείο"""
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
        "trips": st.session_state.trips
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Φόρτωση των μόνιμων δεδομένων κατά την εκκίνηση
saved_data = load_data()

# --- ΑΡΧΙΚΟΠΟΙΗΣΗ SESSION STATE ---
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
            "crew": "", 
            "origin": "", 
            "dest": "", 
            "target": None, 
            "total_mins": 20, 
            "active": False
        }

if "trips" not in st.session_state:
    st.session_state.trips = saved_data["trips"]

# --- ΠΛΕΥΡΙΚΟ ΜΕΝΟΥ & ΔΙΑΧΕΙΡΙΣΗ ΟΝΟΜΑΤΩΝ ---
st.sidebar.markdown("### 🚑 Ambulance4all")
menu = st.sidebar.radio("Μεταβείτε στην ενότητα:", ["🏠 Εταιρικό Προφίλ", "⏱️ Live Παρακολούθηση Στόλου", "📋 Προγραμματισμός Διακομιδών"])

st.sidebar.write("---")
st.sidebar.markdown("### ⚙️ Ονοματοδοσία Στόλου")
st.sidebar.caption("Τροποποιήστε τα ονόματα των οχημάτων.")

st.sidebar.text_input("Όχημα 1", key="name_1", on_change=save_data)
st.sidebar.text_input("Όχημα 2", key="name_2", on_change=save_data)
st.sidebar.text_input("Όχημα 3", key="name_3", on_change=save_data)
st.sidebar.text_input("Όχημα 4", key="name_4", on_change=save_data)
st.sidebar.text_input("Όχημα 5", key="name_5", on_change=save_data)
st.sidebar.text_input("Όχημα 6", key="name_6", on_change=save_data)

# --- ΑΣΦΑΛΗΣ ΕΞΥΓΙΑΝΣΗ ΟΝΟΜΑΤΩΝ ---
raw_names = [
    st.session_state["name_1"].strip(),
    st.session_state["name_2"].strip(),
    st.session_state["name_3"].strip(),
    st.session_state["name_4"].strip(),
    st.session_state["name_5"].strip(),
    st.session_state["name_6"].strip()
]

current_names = []
seen = set()
for idx, name in enumerate(raw_names, 1):
    if not name or name in seen:
        fallback = f"Όχημα {idx}"
        current_names.append(fallback)
        seen.add(fallback)
    else:
        current_names.append(name)
        seen.add(name)

# --- ΣΥΝΑΡΤΗΣΕΙΣ LOGIC ---
def add_trip():
    p = st.session_state.get("f_patient", "").strip()
    f_loc = st.session_state.get("f_from", "").strip()
    t_loc = st.session_state.get("f_to", "").strip()
    
    if p and f_loc and t_loc:
        new_trip = {
            "id": str(uuid.uuid4()), 
            "date": str(st.session_state.get("f_date")), 
            "time": st.session_state.get("f_time", ""), 
            "end": st.session_state.get("f_end", ""), 
            "patient": p, 
            "from": f_loc, 
            "to": t_loc, 
            "amb": st.session_state.get("f_amb")
        }
        st.session_state.trips.append(new_trip)
        save_data()
        st.session_state.trip_success = True
        st.session_state["f_patient"] = ""
        st.session_state["f_from"] = ""
        st.session_state["f_to"] = ""
        st.session_state["f_time"] = ""
        st.session_state["f_end"] = ""
    else:
        st.session_state.trip_success = False

def start_amb(i):
    a = st.session_state.amb[i]
    if a["origin"] and a["dest"]:
        a["active"] = True
        a["target"] = datetime.now() + timedelta(minutes=a["total_mins"])

def stop_amb(i):
    st.session_state.amb[i]["active"] = False
    st.session_state.amb[i]["target"] = None
    st.session_state.amb[i]["origin"] = ""
    st.session_state.amb[i]["dest"] = ""

def delete_trip(trip_id):
    st.session_state.trips = [t for t in st.session_state.trips if t["id"] != trip_id]
    save_data()

# --- 1. ΕΤΑΙΡΙΚΟ ΠΡΟΦΙΛ ---
if menu == "🏠 Εταιρικό Προφίλ":
    st.markdown("<h1 style='text-align: center; color: #CD1818; font-size: 50px; font-weight: bold;'>🚑 Ambulance4all</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #333; font-weight: normal;'>Ιδιωτικά Ασθενοφόρα & Σύγχρονες Ιατρικές Διακομιδές</h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: #666; font-style: italic; margin-bottom: 30px;'>Αμεσότητα • Ασφάλεια • Επαγγελματική Φροντίδα</h5>", unsafe_allow_html=True)
    st.write("---")
    st.markdown(f"""
    ### 🎯 Η Αποστολή μας
    Με απόλυτο σεβασμό στην ανθρώμινη ζωή, η **Ambulance4all** αποτελεί το πρότυπο κέντρο διαχείρισης και εκτέλεσης επειγουσών και προγραμματισμένων ιατρικών διακομιδών. Συνδυάζοντας την τεχνολογική υπεροχή με την επιχειρησιακή ετοιμότητα, προσφέρουμε ολοκληρωμένες υπηρεσίες υγείας, αποτελώντας τον πλέον αξιόπιστο συνεργάτη για νοσηλευτικά ιδρύματα, ασφαλιστικούς φορείς και ιδιώτες.

    ### 🛡️ Πυλώνες της Υπεροχής μας
    * **⚡ Άμεση Ανταπόκριση 24/7:** Λειτουργούμε σε κατάσταση πλήρους επιχειρησιακής ετοιμότητας 365 ημέρες τον χρόνο, εξασφαλίζοντας ελάχιστους χρόνους αναμονής.
    * **🚑 Στόλος Υψηλών Προδιαγραφών:** Τα ιδιωτικά ασθενοφόρα μας (συμπεριλαμβανομένων των κορυφαίων μονάδων **{current_names[0]}, {current_names[1]}, {current_names[2]}, {current_names[3]}**) είναι πλήρως εξοπλισμένα με ιατροτεχνολογικά συστήματα τελευταίας γενιάς.
    * **👨‍⚕️ Εξειδικευμένα Πληρώματα:** Στελεχωνόμαστε αποκλειστικά από πιστοποιημένους διασώστες, έμπειρους οδηγούς και εξειδικευμένο ιατρικό προσωπικό για τη βέλτιστη διαχείριση κάθε περιστατικού.
    * **🌐 Ψηφιακός Έλεγχος:** Επενδύουμε σε συστήματα ζωντανής παρακολούθησης και διαχείρισης στόλου για τον απόλυτο συντονισμό των δρομολογίων.
    """)

# --- 2. LIVE ΠΑΡΑΚΟΛΟΥΘΗΣΗ ΣΤΟΛΟΥ ---
elif menu == "⏱️ Live Παρακολούθηση Στόλου":
    st.title("⏱️ Ζωντανός Έλεγχος Στόλου & Κίνησης")
    
    # ΕΝΣΩΜΑΤΩΣΗ GOOGLE MAPS ΜΕ LIVE TRAFFIC LAYER (ΚΙΝΗΣΗ ΣΤΟΥΣ ΔΡΟΜΟΥΣ)
    st.subheader("🗺️ Ζωντανός Χάρτης Κίνησης (Google Maps Traffic)")
    # Το embedding URL περιλαμβάνει την παράμετρο layer=t για την αυτόματη εμφάνιση της κίνησης
    google_maps_html = """
    <iframe 
        width="100%" 
        height="450" 
        style="border:0; border-radius:10px;" 
        loading="lazy" 
        allowfullscreen 
        src="https://google.com">
    </iframe>
    """
    st.components.v1.html(google_maps_html, height=460)
    
    st.write("---")
    st.subheader("🚑 Κατάσταση & Χρονόμετρα Οχημάτων")

    @st.fragment(run_every=1.0)
    def live_timers_core():
        cols = st.columns(3)
        for i in range(1, 7):
            current_col = cols[(i-1) % 3]
            a = st.session_state.amb[i]
            name = current_names[i-1]
            
            with current_col:
                st.markdown(f"### 🚑 {name}")
                if a["active"]:
                    if a["crew"]: st.markdown(f"**👥 Πλήρωμα:** {a['crew']}")
                    st.markdown(f"📍 **Διαδρομή:** {a['origin']} ➔ {a['dest']}")
                    
                    if a["target"] is not None:
                        remaining = max(0, int((a["target"] - datetime.now()).total_seconds()))
                        total_secs = a["total_mins"] * 60
                        prog = 1 - (remaining / total_secs) if total_secs > 0 else 0
                        st.progress(min(max(prog, 0.0), 1.0))
                        
                        if remaining > 0:
                            m, s = divmod(remaining, 60)
                            st.markdown(f"<div style='font-size: 38px; font-weight: bold; color: #CD1818; font-family: monospace; background-color: #F8F9FA; padding: 5px 15px; border-radius: 5px; display: inline-block;'>⏳ {m:02d}:{s:02d}</div>", unsafe_allow_html=True)
                        else:
                            st.success("✅ Το όχημα έφτασε!")
                            
                    st.button("⏹️ Τερματισμός", key=f"stop_{i}", on_click=stop_amb, args=(i,), use_container_width=True)
                else:
                    a["crew"] = st.text_input("Πλήρωμα", value=a["crew"], key=f"crew_{i}", placeholder="π.χ. Κώστας / Γιάννης")
                    a["origin"] = st.text_input("Από", value=a["origin"], key=f"orig_{i}", placeholder="Σημείο Παραλαβής")
                    a["dest"] = st.text_input("Προς", value=a["dest"], key=f"dest_{i}", placeholder="Νοσοκομείο")
                    a["total_mins"] = st.number_input("Λεπτά", min_value=1, max_value=240, value=int(a["total_mins"]), key=f"mins_{i}")
                    st.button("▶️ Έναρξη Κίνησης", key=f"start_{i}", type="primary", on_click=start_amb, args=(i,), use_container_width=True)
