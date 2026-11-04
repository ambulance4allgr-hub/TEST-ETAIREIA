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
    "📝 Προσθήκη Διακομιδών",
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
    Με απόλυτο σεβασμό στην ανθρώπινη ζωή, η **Ambulance4all** αποτελεί το πρότυπο κέντρο διαχείρισης και εκτέλεσης επείγουσων και προγραμματισμένων ιατρικών διακομιδών. Συνδυάζοντας την τεχνολογική υπεροχή με την επιχειρησιακή ετοιμότητα, προσφέρουμε ολοκληρωμένες υπηρεσίες υγείας, αποτελώντας τον πλέον αξιόπιστο συνεργάτη για νοσηλευτικά ιδρύματα, ασφαλιστικούς φορείς και ιδιώτες.

    ### 🛡️ Πυλώνες της Υπεροχής μας
    * **⚡ Άμεση Ανταπόκριση 24/7:** Λειτουργούμε σε κατάσταση πλήρους επιχειρησιακής ετοιμότητας 365 ημέρες τον χρόνο, εξασφαλίζοντας ελάχιστους χρόνους αναμονής.
    * **🚑 Στόλος Υψηλών Προδιαγραφών:** Τα ιδιωτικά ασθενοφόρα μας είναι πλήρως εξοπλισμένα με ιατροτεχνολογικά συστήματα τελευταίας γενιάς, τηρώντας τα αυστηρότερα διεθνή πρωτόκολλα ασφαλείας.
    * **👨‍⚕️ Εξειδικευμένα Πληρώματα:** Στελεχωνόμαστε αποκλειστικά από πιστοποιημένους διασώστες, έμπειρους οδηγούς και εξειδικευμένο ιατρικό προσωπικό για τη βέλτιστη διαχείριση κάθε περιστατικού.
    * **🌐 Ψηφιακός Έλεγχος:** Επενδύουμε σε σύγχρονα συστήματα ζωντανής παρακολούθησης και διαχείρισης στόλου για τον απόλυτο συντονισμό των δρομολογίων.
    """)
    # --- 2. LIVE ΠΑΡΑΚΟΛΟΥΘΗΣΗ ΣΤΟΛΟΥ ---
elif menu == "⏱️ Live Παρακολούθηση Στόλου":
    st.title("⏱️ Ζωντανός Έλεγχος & Αντίστροφη Μέτρηση")
    st.subheader("Παρακολούθηση ενεργών δρομολογίων σε πραγματικό χρόνο")
    st.write("---")

    with st.expander("⚙️ Διαχείριση & Ονοματοδοσία Ασθενοφόρων"):
        st.info("Εδώ μπορείτε να μετονομάσετε τα οχήματα (π.χ. τα Κενά 5 και 6 όταν ενταχθούν νέα ασθενοφόρα).")
        c_name1, c_name2 = st.columns(2)
        with c_name1:
            st.text_input("Όχημα 1", key="name_1", on_change=save_data)
            st.text_input("Όχημα 2", key="name_2", on_change=save_data)
            st.text_input("Όχημα 3", key="name_3", on_change=save_data)
        with c_name2:
            st.text_input("Όχημα 4", key="name_4", on_change=save_data)
            st.text_input("Όχημα 5", key="name_5", on_change=save_data)
            st.text_input("Όχημα 6", key="name_6", on_change=save_data)

    # 100% Ασφαλής ψηφιακός ήχος (Standard Browser Beep) που δεν μπλοκάρεται
    def play_alert_sound():
        sound_code = """
        <script>
        try {
            var context = new (window.AudioContext || window.webkitAudioContext)();
            var osc = context.createOscillator();
            var gain = context.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(880, context.currentTime); // Ψηλή συχνότητα για καθαρό Beep
            gain.gain.setValueAtTime(0.6, context.currentTime);
            osc.connect(gain);
            gain.connect(context.destination);
            osc.start();
            setTimeout(function() { osc.stop(); }, 400); // Διάρκεια ήχου 0.4 δευτερόλεπτα
        } catch(e) {
            console.log("Audio error:", e);
        }
        </script>
        """
        st.components.v1.html(sound_code, height=0, width=0)

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
                            if not a["sound_played"]:
                                play_alert_sound()
                                a["sound_played"] = True
                            
                    st.button("⏹️ Τερματισμός / Καθαρισμός", key=f"stop_{i}", on_click=lambda idx=i: [st.session_state.amb[idx].update({"active": False, "target": None, "origin": "", "dest": "", "sound_played": False})], use_container_width=True)
                else:
                    a["crew"] = st.text_input("Πλήρωμα", value=a["crew"], key=f"crew_{i}", placeholder="π.χ. Κώστας / Γιάννης")
                    a["origin"] = st.text_input("Από", value=a["origin"], key=f"orig_{i}", placeholder="Σημείο Παραλαβής")
                    a["dest"] = st.text_input("Προς", value=a["dest"], key=f"dest_{i}", placeholder="Νοσοκομείο")
                    a["total_mins"] = st.number_input("Λεπτά Διαδρομής", min_value=1, max_value=240, value=int(a["total_mins"]), key=f"mins_{i}")
                    
                    def start_vehicle(idx=i):
                        st.session_state.amb[idx]["active"] = True
                        st.session_state.amb[idx]["target"] = datetime.now() + timedelta(minutes=st.session_state.amb[idx]["total_mins"])
                        st.session_state.amb[idx]["sound_played"] = False

                    st.button("▶️ Έναρξη Κίνησης", key=f"start_{i}", type="primary", on_click=start_vehicle, use_container_width=True)
                st.write("---")

    live_timers_core()
