import streamlit as st
import time
from datetime import datetime, timedelta
import uuid

st.set_page_config(page_title="Κέντρο Επιχειρήσεων & Διακομιδών", layout="wide")

# --- ΠΛΕΥΡΙΚΟ ΜΕΝΟΥ ---
st.sidebar.markdown("### 🚑 Μενού Διαχείρισης")
menu = st.sidebar.radio("Μεταβείτε στην ενότητα:", ["🏠 Εταιρικό Προφίλ", "⏱️ Live Παρακολούθηση Στόλου", "📋 Προγραμματισμός Διακομιδών"])

# --- ΑΡΧΙΚΟΠΟΙΗΣΗ DATA (SESSION STATE) ---
if "names" not in st.session_state:
    # 4 ενεργά και 2 κενά για μελλοντικά οχήματα
    st.session_state.names = ["Τ12", "Τ16", "Τ16Β", "Τ16Δ", "Κενό 5", "Κενό 6"]

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
        # Καθαρισμός φορμών
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
    st.markdown("<h1 style='text-align: center; color: #CD1818; font-size: 46px; font-weight: bold;'>🚑 Σύγχρονο Κέντρο Ιατρικών Διακομιδών</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #444; font-style: italic; margin-bottom: 30px;'>Αμεσότητα • Ασφάλεια • Επαγγελματική Φροντίδα</h4>", unsafe_allow_html=True)
    st.write("---")
    
    st.markdown("""
    ### 🎯 Η Αποστολή μας
    Με απόλυτο σεβασμό στην ανθρώμινη ζωή, η εταιρεία μας αποτελεί το πρότυπο κέντρο διαχείρισης και εκτέλεσης επειγουσών και προγραμματισμένων ιατρικών διακομιδών. Συνδυάζοντας την τεχνολογική υπεροχή με την επιχειρησιακή ετοιμότητα, προσφέρουμε ολοκληρωμένες υπηρεσίες υγείας, αποτελώντας τον πλέον αξιόπιστο συνεργάτη για νοσηλευτικά ιδρύματα, ασφαλιστικούς φορείς και ιδιώτες.

    ### 🛡️ Πυλώνες της Υπεροχής μας
    
    * **⚡ Άμεση Ανταπόκριση 24/7:** Λειτουργούμε σε κατάσταση πλήρους επιχειρησιακής ετοιμότητας 365 ημέρες τον χρόνο, εξασφαλίζοντας ελάχιστους χρόνους αναμονής.
    * **🚑 Στόλος Υψηλών Προδιαγραφών:** Τα οχήματά μας (συμπεριλαμβανομένων των κορυφαίων μονάδων **Τ12, Τ16, Τ16Β, Τ16Δ**) είναι πλήρως εξοπλισμένα με ιατροτεχνολογικά συστήματα τελευταίας γενιάς.
    * **👨‍⚕️ Εξειδικευμένα Πληρώματα:** Στελεχωνόμαστε αποκλειστικά από πιστοποιημένους διασώστες, έμπειρους οδηγούς και εξειδικευμένο ιατρικό προσωπικό για τη βέλτιστη διαχείριση κάθε περιστατικού.
    * **🌐 Ψηφιακός Έλεγχος:** Επενδύουμε σε συστήματα ζωντανής παρακολούθησης και διαχείρισης στόλου για τον απόλυτο συντονισμό των δρομολογίων.
    """)

# --- 2. LIVE ΠΑΡΑΚΟΛΟΥΘΗΣΗ ΣΤΟΛΟΥ ---
elif menu == "⏱️ Live Παρακολούθηση Στόλου":
    st.title("⏱️ Ζωντανός Έλεγχος & Αντίστροφη Μέτρηση")
    st.subheader("Παρακολούθηση ενεργών δρομολογίων σε πραγματικό χρόνο")
    
    with st.expander("⚙️ Διαχείριση & Ονοματοδοσία Ασθενοφόρων (Προσθήκη Νέων Οχημάτων)"):
        st.info("Εδώ μπορείτε να μετονομάσετε τα 'Κενά' κουτιά όταν ενταχθούν τα 2 νέα ασθενοφόρα σας.")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.session_state.names[0] = st.text_input("Όνομα 1", st.session_state.names[0])
            st.session_state.names[1] = st.text_input("Όνομα 2", st.session_state.names[1])
        with c2:
            st.session_state.names[2] = st.text_input("Όνομα 3", st.session_state.names[2])
            st.session_state.names[3] = st.text_input("Όνομα 4", st.session_state.names[3])
        with c3:
            st.session_state.names[4] = st.text_input("Όνομα 5 (Κενό)", st.session_state.names[4])
            st.session_state.names[5] = st.text_input("Όνομα 6 (Κενό)", st.session_state.names[5])

    # Απομονωμένο Fragment: Ανανεώνεται ΜΟΝΟ η αντίστροφη μέτρηση ανά 1 δευτερόλεπτο
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
                st.success("✅ Το όχημα έφτασε στον προορισμό του!")

    # Δημιουργία Grid 3 στηλών για να βλέπουμε και τα 6 οχήματα «με μια ματιά»
    cols = st.columns(3)
    for i in range(1, 7):
        current_col = cols[(i-1) % 3]
        a = st.session_state.amb[i]
        name = st.session_state.names[i-1]
        
        with current_col:
            st.markdown(f"### 🚑 {name}")
            
            if a["active"]:
                if a["crew"]: st.markdown(f"**👥 Πλήρωμα:** {a['crew']}")
                st.markdown(f"📍 **Διαδρομή:** {a['origin']} ➔ {a['dest']}")
                
                # Εδώ «κουμπώνει» το ζωντανό ρολόι
                live_countdown_widget(i)
                
                st.button("⏹️ Ολοκλήρωση / Τερματισμός", key=f"stop_{i}", on_click=stop_amb, args=(i,), use_container_width=True)
            else:
                # Τα πεδία εισαγωγής μένουν σταθερά και δεν επηρεάζονται από το timer
                a["crew"] = st.text_input("Πλήρωμα", value=a["crew"], key=f"crew_{i}", placeholder="π.χ. Κώστας / Γιάννης")
                a["origin"] = st.text_input("Από", value=a["origin"], key=f"orig_{i}", placeholder="Σημείο Παραλαβής")
                a["dest"] = st.text_input("Προς", value=a["dest"], key=f"dest_{i}", placeholder="Νοσοκομείο / Κλινική")
                a["total_mins"] = st.number_input("Εκτιμώμενος Χρόνος (Λεπτά)", min_value=1, max_value=240, value=int(a["total_mins"]), key=f"mins_{i}")
                st.button("▶️ Έναρξης Κίνησης", key=f"start_{i}", type="primary", on_click=start_amb, args=(i,), use_container_width=True)
            st.write("---")

# --- 3. ΠΡΟΓΡΑΜΜΑ ΔΙΑΚΟΜΙΔΩΝ ---
elif menu == "📋 Προγραμματισμός Διακομιδών":
    st.title("📋 Προγραμματισμός & Καταγραφή Διακομιδών")
    
    # 2 Στήλες: Αριστερά η Φόρμα, Δεξιά η προβολή ανά Ασθενοφόρο
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
        st.selectbox("Ανάθεση σε Ασθενοφόρο", st.session_state.names, key="f_amb")
        
        st.button("💾 Αποθήκευση στο Πρόγραμμα", type="primary", on_click=add_trip, use_container_width=True)
        
        if st.session_state.get("trip_success") is True:
            st.success("✔️ Η διακομιδή καταχωρήθηκε με επιτυχία!")
            st.session_state.trip_success = None
        elif st.session_state.get("trip_success") is False:
            st.error("❌ Σφάλμα: Συμπληρώστε Ασθενή, Από και Προς.")
            st.session_state.trip_success = None

    with view_col:
        st.subheader("📅 Προγραμματισμένα Δρομολόγια ανά Όχημα")
        
        # Δημιουργία Tabs (καρτελών) για κάθε ένα από τα 6 ασθενοφόρα ξεχωριστά
        tabs = st.tabs([f"🚑 {name}" for name in st.session_state.names])
        
        for index, amb_name in enumerate(st.session_state.names):
            with tabs[index]:
                # Φιλτράρισμα και ταξινόμηση βάσει ημερομηνίας/ώρας
                amb_trips = [t for t in st.session_state.trips if t['amb'] == amb_name]
                amb_trips = sorted(amb_trips, key=lambda x: (str(x['date']), str(x['time'])))
                
                if not amb_trips:
                    st.info(f"Δεν υπάρχουν καταχωρημένες διακομιδές για το όχημα {amb_name}.")
                else:
                    for trip in amb_trips:
                        with st.container(border=True):
