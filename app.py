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
                data = json.load(f)
                if "dynamic_inc" not in data: data["dynamic_inc"] = {}
                if "dynamic_exp" not in data: data["dynamic_exp"] = {}
                return data
        except:
            pass
    return {
         "names": ["T12", "T16", "T16B", "T16Δ", "Κενό 5", "Κενό 6", "Κενό 7", "Κενό 8", "Κενό 9"],
        "trips": [],
        "dynamic_inc": {},
        "dynamic_exp": {}
    }

def save_data():
    names_to_save = [
        st.session_state.get("name_1", "T12"),
        st.session_state.get("name_2", "T16"),
        st.session_state.get("name_3", "T16B"),
        st.session_state.get("name_4", "T16Δ"),
        st.session_state.get("name_5", "Κενό 5"),
        st.session_state.get("name_6", "Κενό 6"),
        st.session_state.get("name_7", "Κενό 7"),
        st.session_state.get("name_8", "Κενό 8"),
        st.session_state.get("name_9", "Κενό 9")
    ]
    data = {
        "names": names_to_save,
        "trips": st.session_state.trips_list,
        "dynamic_inc": st.session_state.get("dynamic_inc", {}),
        "dynamic_exp": st.session_state.get("dynamic_exp", {})
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

saved_data = load_data()

# --- ΑΡΧΙΚΟΠΟΙΗΣΗ ΜΝΗΜΗΣ (SESSION STATE) ---
# Φορτώνουμε τη λίστα των ονομάτων από το αρχείο, αν δεν υπάρχει βάζουμε τα έτοιμα 9
current_names = saved_data.get("names", ["T12", "T16", "T16B", "T16Δ", "Κενό 5", "Κενό 6", "Κενό 7", "Κενό 8", "Κενό 9"])

# Αν η λίστα στο αρχείο έχει λιγότερα από 9 ονόματα, της προσθέτουμε τα κενά που λείπουν
while len(current_names) < 9:
    current_names.append(f"Κενό {len(current_names) + 1}")

# Αρχικοποίηση στη μνήμη (Session State) για όλα τα 9 ασθενοφόρα αυτόματα
for idx in range(1, 10):
    var_name = f"name_{idx}"
    if var_name not in st.session_state:
        st.session_state[var_name] = current_names[idx - 1]

if "amb" not in st.session_state:
    st.session_state.amb = {}
    for i in range(1, 10):
        st.session_state.amb[i] = {
            "crew": "", "origin": "", "dest": "", "target": None, "total_mins": 20, "active": False, "sound_played": False
        }

if "trips_list" not in st.session_state:
    st.session_state.trips_list = saved_data.get("trips", [])

if "dynamic_inc" not in st.session_state: 
    st.session_state.dynamic_inc = saved_data.get("dynamic_inc", {})
if "dynamic_exp" not in st.session_state: 
    st.session_state.dynamic_exp = saved_data.get("dynamic_exp", {})
if "trips_list" not in st.session_state:
    st.session_state.trips_list = saved_data["trips"]
    if "dynamic_inc" not in st.session_state: st.session_state.dynamic_inc = saved_data.get("dynamic_inc", {})
if "dynamic_exp" not in st.session_state: st.session_state.dynamic_exp = saved_data.get("dynamic_exp", {})

# --- ΠΛΕΥΡΙΚΟ ΜΕΝΟΥ ---
st.sidebar.markdown("### 🚑 Ambulance4all")
menu = st.sidebar.radio("Μεταβείτε στην ενότητα:", [
    "🏠 Εταιρικό Προφίλ", 
    "⏱️ Live Παρακολούθηση Στόλου", 
    "📝 Προσθήκη Διαδρομών",
    "📅 Ημερήσιο Πρόγραμμα (Ημερολόγιο)",
    "📈 Έσοδα - Έξοδα Εταιρείας",
    "💰 Ημερήσιο Ταμείο Ασθενοφόρων",
    "👥 Διαθέσιμοι Διασώστες",
    "🤝 Συνεργάτες"
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
            st.text_input("Όνομα 7", key="name_7", on_change=save_data)
            st.text_input("Όνομα 8", key="name_8", on_change=save_data)
            st.text_input("Όνομα 9", key="name_9", on_change=save_data)

    def play_alert_sound():
        sound_code = """
        <script>
        try {
            var context = new (window.AudioContext || window.webkitAudioContext)();
            var osc = context.createOscillator();
            var gain = context.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(880, context.currentTime);
            gain.gain.setValueAtTime(0.6, context.currentTime);
            osc.connect(gain);
            gain.connect(context.destination);
            osc.start();
            setTimeout(function() { osc.stop(); }, 400);
        } catch(e) {
            console.log("Audio error:", e);
        }
        </script>
        """
        st.components.v1.html(sound_code, height=0, width=0)

    @st.fragment(run_every=1.0)
    def live_timers_core():
        cols = st.columns(3)
        for i in range(1, 10):
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

# --- 3. ΠΡΟΣΘΗΚΗ ΔΙΑΔΡΟΜΩΝ ---
elif menu == "📝 Προσθήκη Διαδρομών":
    st.title("📝 Καταχώρηση Νέας Διακομιδής")
    st.subheader("Συμπληρώστε τα πλήρη στοιχεία για το ημερήσιο πρόγραμμα")
    st.write("---")
    
    with st.form("new_trip_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            patient = st.text_input("👤 Ονοματεπώνυμο Ασθενούς", placeholder="π.χ. Γεώργιος Παπαδόπουλος")
            trip_date = st.date_input("📅 Ημερομηνία Διακομιδής", value=datetime.now().date())
            
            c_time1, c_time2 = st.columns(2)
            with c_time1:
                time_start = st.text_input("🕒 Ώρα Έναρξης", placeholder="π.χ. 09:30")
            with c_time2:
                time_end = st.text_input("🏁 Ώρα Λήξης / Άφιξης", placeholder="π.χ. 10:15")
                
            c_age, c_weight = st.columns(2)
            with c_age:
                age = st.text_input("🎂 Ηλικία Ασθενούς", placeholder="π.χ. 75")
            with c_weight:
                weight = st.text_input("⚖️ Βάρος (kg)", placeholder="π.χ. 80")
                
            reason = st.text_input("🩺 Λόγος Διακομιδής", placeholder="π.χ. Επανέλεγχος / Εξιτήριο")
            cost = st.text_input("💶 Κόστος Διακομιδής (€)", placeholder="π.χ. 50")
            
        with c2:
            loc_from = st.text_input("📍 Τοποθεσία Παραλαβής (Από)", placeholder="π.χ. Οικία / Κλινική Α")
            loc_to = st.text_input("🏢 Τοποθεσία Προορισμού (Προς)", placeholder="π.χ. Νοσοκομείο Β")
            home_info = st.text_input("🏠 Πληροφορίες Οικίας", placeholder="π.χ. 2ος όροφος, στενό ασανσέρ")
            pickup_mode = st.text_input("🪑 Τρόπος Παραλαβής", value="Φορείο", placeholder="π.χ. Φορείο, Καρέκλα, κλπ.")
            assigned_amb = st.selectbox("🚑 Επιλογή Ασθενοφόρου", current_names)
            notes = st.text_area("💬 Σχόλια / Επιπλέον Πληροφορίες", placeholder="π.χ. Χρειάζεται οξυγόνο κατά τη διαδρομή")
            
        submit_btn = st.form_submit_button("💾 Αποθήκευση στο Πρόγραμμα", use_container_width=True)
        
        if submit_btn:
            if patient.strip() and loc_from.strip() and loc_to.strip():
                new_trip = {
                    "id": str(uuid.uuid4()), 
                    "date": str(trip_date),
                    "time": time_start,
                    "end": time_end,
                    "patient": patient,
                    "age": age,
                    "weight": weight,
                    "reason": reason,
                    "from": loc_from,
                    "to": loc_to,
                    "home_info": home_info,
                    "pickup_mode": pickup_mode,
                    "cost": cost,
                    "notes": notes,
                    "amb": assigned_amb
                }
                st.session_state.trips_list.append(new_trip)
                save_data()
                st.success("✔️ Η διακομιδή καταχωρήθηκε μόνιμα με όλα τα στοιχεία!")
                st.rerun()
            else:
                st.error("❌ Σφάλμα: Τα πεδία Ονοματεπώνυμο, Από και Προς είναι υποχρεωτικά.")
# --- 4. ΗΜΕΡΗΣΙΟ ΠΡΟΓΡΑΜΜΑ (ΗΜΕΡΟΛΟΓΙΟ) ---
elif menu == "📅 Ημερήσιο Πρόγραμμα (Ημερολόγιο)":
    st.title("📅 Ημερήσιο Πρόγραμμα Διακομιδών")
    st.subheader("Επιλέξτε ημερομηνία για να δείτε το αναλυτικό πλάνο των οχημάτων")
    
    # Μπάρα ημερολογίου στο πάνω μέρος της σελίδας
    selected_date = st.date_input("📆 Επιλογή Ημερομηνίας Προβολής:", datetime.now().date())
    st.write("---")
    
    st.markdown(f"### 📋 Πλάνο Διαδρομών για την ημέρα: **{selected_date.strftime('%d/%m/%Y')}**")
    
    # Δημιουργία των 6 Tabs με τα ονόματα των ασθενοφόρων σας
    tabs = st.tabs([f"🚑 {name}" for name in current_names])
    
    for index, amb_name in enumerate(current_names):
        with tabs[index]:
            # Φιλτράρισμα: Κρατάμε τις διαδρομές του συγκεκριμένου οχήματος για την επιλεγμένη ημέρα
            amb_trips = [
                t for t in st.session_state.trips_list 
                if t['amb'] == amb_name and t['date'] == str(selected_date)
            ]
            
            # Ταξινόμηση των διακομιδών βάσει της ώρας έναρξης
            amb_trips = sorted(amb_trips, key=lambda x: str(x['time']))
            
            if not amb_trips:
                st.info(f"Δεν υπάρχουν προγραμματισμένες διακομιδές για το όχημα {amb_name} στις {selected_date.strftime('%d/%m/%Y')}.")
            else:
                for trip in amb_trips:
                    # Καθαρό, οργανωμένο κουτί (Container) για κάθε ασθενή με όλα τα νέα πεδία
                    with st.container(border=True):
                        c_header1, c_header2 = st.columns(2)
                        with c_header1:
                            st.markdown(f"👤 **Ασθενής:** <span style='font-size:19px; font-weight:bold; color:#CD1818;'>{trip['patient']}</span>", unsafe_allow_html=True)
                        with c_header2:
                            if trip.get('cost'):
                                st.markdown(f"<h4 style='text-align:right; color:#2E7D32; margin:0;'>💶 {trip['cost']} €</h4>", unsafe_allow_html=True)
                        
                        # Πίνακας με τα ιατρικά και επιχειρησιακά στοιχεία
                        col_info1, col_info2 = st.columns(2)
                        with col_info1:
                            st.markdown(f"🕒 **Ώρα:** {trip['time']} έως {trip['end']}")
                            st.markdown(f"📍 **Διαδρομή:** **{trip['from']}** ➔ **{trip['to']}**")
                            st.markdown(f"🩺 **Λόγος:** {trip.get('reason', '-')}")
                            if trip.get('home_info'):
                                st.markdown(f"🏠 **Οικία:** {trip['home_info']}")
                        with col_info2:
                            st.markdown(f"🎂 **Ηλικία:** {trip.get('age', '-')} ετών | ⚖️ **Βάρος:** {trip.get('weight', '-')} kg")
                            st.markdown(f"🪑 **Τρόπος Παραλαβής:** {trip.get('pickup_mode', '-')}")
                            if trip.get('notes'):
                                st.markdown(f"💬 **Σχόλια:** *{trip['notes']}*")
                        
                        st.write("#")
                        st.button("🗑️ Διαγραφή Διαδρομής", key=f"del_{trip['id']}", on_click=delete_trip, args=(trip['id'],), type="secondary")

# --- 6. ΗΜΕΡΗΣΙΟ ΤΑΜΕΙΟ ΑΣΘΕΝΟΦΟΡΩΝ ---
elif menu == "💰 Ημερήσιο Ταμείο Ασθενοφόρων":
    st.title("💰 Ημερήσιο Ταμείο Ασθενοφόρων")
    st.subheader("Αναλυτική καταγραφή εσόδων και εξόδων με δυναμικές γραμμές")
    
    selected_date = st.date_input("📆 Επιλογή Ημερομηνίας Ταμείου:", datetime.now().date(), key="t_date")
    st.write("---")
    
    st.markdown(f"### 📊 Οικονομικός Έλεγχος Στόλου: **{selected_date.strftime('%d/%m/%Y')}**")
    
    key_inc_main = f"inc_{selected_date}"
    key_exp_main = f"exp_{selected_date}"
    
    if key_inc_main not in st.session_state.dynamic_inc: st.session_state.dynamic_inc[key_inc_main] = {}
    if key_exp_main not in st.session_state.dynamic_exp: st.session_state.dynamic_exp[key_exp_main] = {}
        
    cols = st.columns(3)
    
    for i in range(1, 7):
        current_col = cols[(i-1) % 3]
        amb_name = current_names[i-1]
        
        if amb_name not in st.session_state.dynamic_inc[key_inc_main]:
            st.session_state.dynamic_inc[key_inc_main][amb_name] = [{"label": "Έκτακτο 1", "val": "0"}]
        if amb_name not in st.session_state.dynamic_exp[key_exp_main]:
            st.session_state.dynamic_exp[key_exp_main][amb_name] = [{"label": "Πετρέλαιο", "val": "0"}]
            
        amb_trips = [
            t for t in st.session_state.trips_list 
            if t['amb'] == amb_name and t['date'] == str(selected_date)
        ]
        auto_income = sum(float(t.get('cost', 0) or 0) for t in st.session_state.trips_list if t['amb'] == amb_name and t['date'] == str(selected_date))
                
        with current_col:
            with st.container(border=True):
                st.markdown(f"### 🚑 {amb_name}")
                st.markdown(f"**📈 Έσοδα Προγράμματος:** {auto_income:,.2f} € *(από {len(amb_trips)} διακ.)*")
                st.write("---")
                
                st.markdown("**💶 Επιλέον Έκτακτα Έσοδα**")
                tot_extra_inc = 0.0
                
                for idx, item in enumerate(st.session_state.dynamic_inc[key_inc_main][amb_name]):
                    c_lbl, c_val = st.columns(2)
                    with c_lbl:
                        item["label"] = st.text_input(f"Αιτιολογία", value=item["label"], key=f"lbl_inc_{key_inc_main}_{amb_name}_{idx}", label_visibility="collapsed", placeholder="Όνομα Ασθενούς")
                    with c_val:
                        item["val"] = st.text_input(f"Ποσό", value=item["val"], key=f"val_inc_{key_inc_main}_{amb_name}_{idx}", label_visibility="collapsed", placeholder="Ποσό")
                    
                    v_clean = str(item["val"]).replace("€", "").replace(",", ".").strip()
                    try: tot_extra_inc += float(v_clean) if v_clean else 0.0
                    except ValueError: pass
                
                if st.button("➕ Προσθήκη Γραμμής Εσόδου", key=f"btn_add_inc_{key_inc_main}_{amb_name}", use_container_width=True):
                    st.session_state.dynamic_inc[key_inc_main][amb_name].append({"label": "", "val": "0"})
                    save_data()
                    st.rerun()
                
                st.write("---")
                st.markdown("**⛽ Έξοδα Βάρδιας**")
                tot_exp = 0.0
                
                for idx, item in enumerate(st.session_state.dynamic_exp[key_exp_main][amb_name]):
                    c_lbl, c_val = st.columns(2)
                    with c_lbl:
                        item["label"] = st.text_input(f"Έξοδο", value=item["label"], key=f"lbl_exp_{key_exp_main}_{amb_name}_{idx}", label_visibility="collapsed", placeholder="π.χ. Οξυγόνο")
                    with c_val:
                        item["val"] = st.text_input(f"Ποσό", value=item["val"], key=f"val_exp_{key_exp_main}_{amb_name}_{idx}", label_visibility="collapsed", placeholder="Ποσό")
                    
                    v_clean = str(item["val"]).replace("€", "").replace(",", ".").strip()
                    try: tot_exp += float(v_clean) if v_clean else 0.0
                    except ValueError: pass
                
                if st.button("➕ Προσθήκη Γραμμής Εξόδου", key=f"btn_add_exp_{key_exp_main}_{amb_name}", use_container_width=True):
                    st.session_state.dynamic_exp[key_exp_main][amb_name].append({"label": "", "val": "0"})
                    save_data()
                    st.rerun()
                
                # Εξασφάλιση μόνιμης αποθήκευσης σε κάθε κύκλο της εφαρμογής
                save_data()
                
                total_income = auto_income + tot_extra_inc
                total_net = total_income - tot_exp
                
                st.write("---")
                st.markdown(f"**Συνολικά Έσοδα:** {total_income:,.2f} € | **Συνολικά Έξοδα:** {tot_exp:,.2f} €")
                st.markdown(f"🏁 **Καθαρή Παράδοση:** <span style='font-size: 24px; font-weight: bold; color: #CD1818;'>{total_net:,.2f} €</span>", unsafe_allow_html=True)
            st.write("##")

# --- 7. ΔΙΑΘΕΣΙΜΟΙ ΔΙΑΣΩΣΤΕΣ ---
elif menu == "👥 Διαθέσιμοι Διασώστες":
    st.title("👥 Μητρώο & Διαθεσιμότητα Διασωστών")
    st.info("Αυτή η ενότητα θα υλοποιηθεί στα επόμενα βήματα.")

# --- 8. ΣΥΝΕΡΓΑΤΕΣ ---
elif menu == "🤝 Συνεργάτες":
    st.title("🤝 Συνεργάτες Εταιρείας")
    st.info("Αυτή η ενότητα θα υλοποιηθεί στα επόμενα βήματα.")

