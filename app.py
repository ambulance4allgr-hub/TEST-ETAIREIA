import streamlit as st
import time
from datetime import datetime, timedelta
import uuid

st.set_page_config(page_title="ambulance4all | Κέντρο Επιχειρήσεων", layout="wide")

# --- ΑΡΧΙΚΟΠΟΙΗΣΗ DATA (SESSION STATE) ---
if "name_1" not in st.session_state: st.session_state["name_1"] = "Τ12"
if "name_2" not in st.session_state: st.session_state["name_2"] = "Τ16"
if "name_3" not in st.session_state: st.session_state["name_3"] = "Τ16Β"
if "name_4" not in st.session_state: st.session_state["name_4"] = "Τ16Δ"
if "name_5" not in st.session_state: st.session_state["name_5"] = "Κενό 5"
if "name_6" not in st.session_state: st.session_state["name_6"] = "Κενό 6"

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
    st.session_state.trips = []

# --- ΠΛΕΥΡΙΚΟ ΜΕΝΟΥ & ΔΙΑΧΕΙΡΙΣΗ ΟΝΟΜΑΤΩΝ ---
st.sidebar.markdown("### 🚑 ambulance4all")
menu = st.sidebar.radio("Μεταβείτε στην ενότητα:", ["🏠 Εταιρικό Προφίλ", "⏱️ Live Παρακολούθηση Στόλου", "📋 Προγραμματισμός Διακομιδών"])

st.sidebar.write("---")
st.sidebar.markdown("### ⚙️ Ονοματοδοσία Στόλου")
st.sidebar.caption("Τροποποιήστε τα ονόματα των οχημάτων ανά πάσα στιγμή.")

st.sidebar.text_input("Όχημα 1", key="name_1")
st.sidebar.text_input("Όχημα 2", key="name_2")
st.sidebar.text_input("Όχημα 3", key="name_3")
st.sidebar.text_input("Όχημα 4", key="name_4")
st.sidebar.text_input("Όχημα 5", key="name_5")
st.sidebar.text_input("Όχημα 6", key="name_6")

# --- ΑΣΦΑΛΗΣ ΕΞΥΓΙΑΝΣΗ ΟΝΟΜΑΤΩΝ (FAIL-SAFE) ---
# Διασφαλίζει ότι δεν θα υπάρξουν κενά ή διπλότυπα ονόματα που κρασάρουν τα Tabs
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
    # Αν το όνομα είναι κενό ή έχει ήδη χρησιμοποιηθεί, δώσε ένα έγκυρο μοναδικό όνομα
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
            "date": st.session_state.get("f_date"), 
            "time": st.session_state.get("f_time", ""), 
            "end": st.session_state.get("f_end", ""), 
            "patient": p, 
            "from": f_loc, 
            "to": t_loc, 
            "amb": st.session_state.get("f_amb")
        }
        st.session_state.trips.append(new_trip)
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

# --- 1. ΕΤΑΙΡΙΚΟ ΠΡΟΦΙΛ (ΑΡΧΙΚΗ ΣΕΛΙΔΑ) ---
if menu == "🏠 Εταιρικό Προφίλ":
    st.markdown("<h1 style='text-align: center; color: #CD1818; font-size: 50px; font-weight: bold;'>🚑 ambulance4all</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #333; font-weight: normal;'>Ιδιωτικά Ασθενοφόρα & Σύγχρονες Ιατρικές Διακομιδές</h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: #666; font-style: italic; margin-bottom: 30px;'>Αμεσότητα • Ασφάλεια • Επαγγελματική Φροντίδα</h5>", unsafe_allow_html=True)
    st.write("---")
    st.markdown(f"""
    ### 🎯 Η Αποστολή μας
    Με απόλυτο σεβασμό στην ανθρώμινη ζωή, η **ambulance4all** αποτελεί το πρότυπο κέντρο διαχείρισης και εκτέλεσης επειγουσών και προγραμματισμένων ιατρικών διακομιδών. Συνδυάζοντας την τεχνολογική υπεροχή με την επιχειρησιακή ετοιμότητα, προσφέρουμε ολοκληρωμένες υπηρεσίες υγείας, αποτελώντας τον πλέον αξιόπιστο συνεργάτη για νοσηλευτικά ιδρύματα, ασφαλιστικούς φορείς και ιδιώτες.

    ### 🛡️ Πυλώνες της Υπεροχής μας
    * **⚡ Άμεση Ανταπόκριση 24/7:** Λειτουργούμε σε κατάσταση πλήρους επιχειρησιακής ετοιμότητας 365 ημέρες τον χρόνο, εξασφαλίζοντας ελάχιστους χρόνους αναμονής.
    * **🚑 Στόλος Υψηλών Προδιαγραφών:** Τα ιδιωτικά ασθενοφόρα μας (συμπεριλαμβανομένων των κορυφαίων μονάδων **{current_names[0]}, {current_names[1]}, {current_names[2]}, {current_names[3]}**) είναι πλήρως εξοπλισμένα με ιατροτεχνολογικά συστήματα τελευταίας γενιάς.
    * **👨‍⚕️ Εξειδικευμένα Πληρώματα:** Στελεχωνόμαστε αποκλειστικά από πιστοποιημένους διασώστες, έμπειρους οδηγούς και εξειδικευμένο ιατρικό προσωπικό για τη βέλτιστη διαχείριση κάθε περιστατικού.
    * **🌐 Ψηφιακός Έλεγχος:** Επενδύουμε σε συστήματα ζωντανής παρακολούθησης και διαχείρισης στόλου για τον απόλυτο συντονισμό των δρομολογίων.
    """)

# --- 2. LIVE ΠΑΡΑΚΟΛΟΥΘΗΣΗ ΣΤΟΛΟΥ ---
elif menu == "⏱️ Live Παρακολούθηση Στόλου":
    st.title("⏱️ Ζωντανός Έλεγχος & Αντίστροφη Μέτρηση")
    st.subheader("Παρακολούθηση ενεργών δρομολογίων σε πραγματικό χρόνο")

    @st.fragment(run_every=1.0)
    def live_countdown_widget(i):
        a = st.session_state.amb[i]
        if a["active"] and a["target"] is not None:
            remaining = max(0, int((a["target"] - datetime.now()).total_seconds()))
            total_secs = a["total_mins"] * 60
            prog = 1 - (remaining / total_secs) if total_secs > 0 else 0
            st.progress(min(max(prog, 0.0), 1.0))
            if remaining > 0:
                m, s = divmod(remaining, 60)
                st.markdown(f"<div style='font-size: 38px; font-weight: bold; color: #CD1818; font-family: monospace; background-color: #F8F9FA; padding: 5px 15px; border-radius: 5px; display: inline-block;'>⏳ {m:02d}:{s:02d}</div>", unsafe_allow_html=True)
            else:
                st.success("✅ Το όχημα έφτασε!")

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
                live_countdown_widget(i)
                st.button("⏹️ Τερματισμός", key=f"stop_{i}", on_click=stop_amb, args=(i,), use_container_width=True)
            else:
                a["crew"] = st.text_input("Πλήρωμα", value=a["crew"], key=f"crew_{i}", placeholder="π.χ. Κώστας / Γιάννης")
                a["origin"] = st.text_input("Από", value=a["origin"], key=f"orig_{i}", placeholder="Σημείο Παραλαβής")
                a["dest"] = st.text_input("Προς", value=a["dest"], key=f"dest_{i}", placeholder="Νοσοκομείο")
                a["total_mins"] = st.number_input("Λεπτά", min_value=1, max_value=240, value=int(a["total_mins"]), key=f"mins_{i}")
                st.button("▶️ Έναρξη Κίνησης", key=f"start_{i}", type="primary", on_click=start_amb, args=(i,), use_container_width=True)
            st.write("---")

# --- 3. ΠΡΟΓΡΑΜΜΑ ΔΙΑΚΟΜΙΔΩΝ ---
elif menu == "📋 Προγραμματισμός Διακομιδών":
    st.title("📋 Προγραμματισμός & Καταγραφή Διακομιδών")
    form_col, view_col = st.columns([1, 1.6], gap="large")
    
    with form_col:
        st.subheader("📝 Καταχώρηση Νέας Διακομιδής")
        st.text_input("Όνομα Ασθενούς", key="f_patient", placeholder="π.χ. Γεώργιος Παπαδόπουλος")
        st.date_input("Ημερομηνία", key="f_date")
        c_time1, c_time2 = st.columns(2)
        with c_time1: st.text_input("Ώρα Έναρξης", key="f_time", placeholder="π.χ. 09:30")
        with c_time2: st.text_input("Ώρα Τέλους", key="f_end", placeholder="π.χ. 10:15")
        st.text_input("Τοποθεσία Παραλαβής (Από)", key="f_from")
        st.text_input("Τοποθεσία Προορισμού (Προς)", key="f_to")
        st.selectbox("Ανάθεση σε Ασθενοφόρο", current_names, key="f_amb")
        st.button("💾 Αποθήκευση στο Πρόγραμμα", type="primary", on_click=add_trip, use_container_width=True)
        
        if st.session_state.get("trip_success") is True:
            st.success("✔️ Η διακομιδή καταχωρήθηκε!")
            st.session_state.trip_success = None
        elif st.session_state.get("trip_success") is False:
            st.error("❌ Σφάλμα: Συμπληρώστε Ασθενή, Από και Προς.")
            st.session_state.trip_success = None

    with view_col:
        st.subheader("📅 Προγραμματισμένα Δρομολόγια ανά Όχημα")
        tabs = st.tabs([f"🚑 {name}" for name in current_names])
        for index, amb_name in enumerate(current_names):
            with tabs[index]:
                amb_trips = [t for t in st.session_state.trips if t['amb'] == amb_name]
                amb_trips = sorted(amb_trips, key=lambda x: (str(x['date']), str(x['time'])))
                if not amb_trips:
                    st.info(f"Δεν υπάρχουν διακομιδές για το όχημα {amb_name}.")
                else:
                    for trip in amb_trips:
