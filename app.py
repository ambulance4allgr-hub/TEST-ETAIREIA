import streamlit as st
import time
from datetime import datetime, timedelta
import uuid

st.set_page_config(page_title="Κέντρο Ελέγχου Εταιρείας", layout="wide")

st.sidebar.title("Μενού Εφαρμογής")
menu = st.sidebar.radio("Επιλέξτε Ενότητα:", ["🏠 Αρχική", "🚑 Live Παρακολούθηση", "📋 Πρόγραμμα Διακομιδών"])

if "amb" not in st.session_state:
    st.session_state.amb = {}
    for i in range(1, 5):
        st.session_state.amb[i] = {"name": f"Ασθενοφόρο {i}", "crew": "", "origin": "", "dest": "", "target": None, "total_mins": 0, "active": False}

if "trips" not in st.session_state:
    st.session_state.trips = []

if menu == "🏠 Αρχική":
    st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🚑 Καλώς ήρθατε στην Εταιρεία μας</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Πρωτοπόροι στις Διακομιδές και την Άμεση Ανταπόκριση</h3>", unsafe_allow_html=True)
    st.write("")
    st.info("Η εταιρεία μας δεσμεύεται να παρέχει τις πιο ασφαλείς, γρήγορες και αξιόπιστες υπηρεσίες διακομιδών. Με χρόνια εμπειρίας και έναν από τους πιο σύγχρονους στόλους ασθενοφόρων, είμαστε πάντα δίπλα σας όποτε μας χρειαστείτε, 24 ώρες το 24ωρο, 7 ημέρες την εβδομάδα.")
    st.write("---")
    st.subheader("Γιατί να μας επιλέξετε;")
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.markdown("### ⚡ Άμεση Ανταπόκριση")
            st.write("Είμαστε έτοιμοι να ανταποκριθούμε στο περιστατικό σας άμεσα. Ο χρόνος για εμάς είναι ζωή.")
    with col2:
        with st.container(border=True):
            st.markdown("### 🚑 Σύγχρονος Στόλος")
            st.write("Διαθέτουμε πλήρως εξοπλισμένα ασθενοφόρα, τηρώντας όλα τα πρότυπα ασφαλείας και υγιεινής.")
    with col3:
        with st.container(border=True):
            st.markdown("### 👨‍⚕️ Έμπειρο Προσωπικό")
            st.write("Το πλήρωμά μας αποτελείται από έμπειρους διασώστες και οδηγούς, έτοιμους να προσφέρουν τη φροντίδα που αξίζετε.")
    st.write("---")
    st.success("Χρησιμοποιήστε το μενού στα αριστερά για να μεταβείτε στην Παρακολούθηση των Ασθενοφόρων ή στο Πρόγραμμα Διακομιδών.")

elif menu == "🚑 Live Παρακολούθηση":
    st.title("🚑 Κέντρο Παρακολούθησης Ασθενοφόρων")
    @st.fragment(run_every=1.0)
    def draw_ambulances():
        for i in range(1, 5):
            a = st.session_state.amb[i]
            with st.container(border=True):
                if not a["active"]:
                    c1, c2, c3, c4, c5, c6 = st.columns([1.5, 0.8, 1, 1, 0.8, 0.8])
                    with c1:
                        new_name = st.text_input("Όνομα", value=a["name"], key=f"name_{i}")
                    with c2:
                        st.write("")
                        st.write("")
                        if st.button("💾", key=f"save_name_{i}", help="Αποθήκευση ονόματος"):
                            a["name"] = new_name
                            st.rerun()
                    with c3:
                        a["crew"] = st.text_input("Πλήρωμα", value=a["crew"], key=f"crew_{i}", placeholder="Ονόματα")
                    with c4:
                        a["origin"] = st.text_input("Από πού", key=f"o{i}", placeholder="π.χ. Αγία Όλγα")
                    with c5:
                        a["dest"] = st.text_input("Πού", key=f"d{i}", placeholder="π.χ. Ευαγγελισμός")
                    with c6:
                        mins = st.number_input("Λεπτά", min_value=1, max_value=180, value=15, key=f"m{i}")
                        if st.button("▶", key=f"btn{i}", use_container_width=True, type="primary"):
                            if a["origin"] and a["dest"]:
                                a["total_mins"] = mins
                                a["target"] = datetime.now() + timedelta(minutes=mins)
                                a["active"] = True
                                st.rerun()
                            else:
                                st.warning("Συμπλήρωσε διαδρομή.")
                else:
                    col_info, col_prog, col_timer, col_btn = st.columns([2, 1.5, 1.2, 0.8])
                    with col_info:
                        st.markdown(f"**🚑 {a['name']}**")
                        if a["crew"]:
                            st.caption(f"👥 {a['crew']}")
                        st.caption(f"📍 {a['origin']} ➔ {a['dest']}")
                    with col_prog:
                        st.write("") 
                        remaining = max(0, int((a["target"] - datetime.now()).total_seconds()))
                        total_secs = a["total_mins"] * 60
                        prog = 1 - (remaining / total_secs) if total_secs > 0 else 0
                        st.progress(min(max(prog, 0.0), 1.0))
                    with col_timer:
                        if remaining > 0:
                            m, s = divmod(remaining, 60)
                            st.markdown(f"<div style='font-size: 35px; font-weight: bold; text-align: center; color: #FF4B4B; font-family: monospace;'>{m:02d}:{s:02d}</div>", unsafe_allow_html=True)
                        else:
                            st.success("✅ Έφτασε!")
                    with col_btn:
                        st.write("")
                        if st.button("⏹", key=f"stop{i}", use_container_width=True):
                            a["active"] = False
                            a["target"] = None
                            st.rerun()
    draw_ambulances()

elif menu == "📋 Πρόγραμμα Διακομιδών":
    st.title("📋 Πρόγραμμα Διακομιδών")
    
    with st.form("trip_form", clear_on_submit=True):
        patient = st.text_input("Όνομα Ασθενούς")
        trip_date = st.date_input("Ημερομηνία")
        trip_time = st.text_input("Ώρα Έναρξης (π.χ. 14:30)")
        trip_end = st.text_input("Ώρα Τέλους (π.χ. 15:15)")
        from_loc = st.text_input("Από (Νοσοκομείο/Διεύθυνση)")
        to_loc = st.text_input("Προς (Νοσοκομείο/Διεύθυνση)")
        amb_choice = st.text_input("Ασθενοφόρο (Γράψε το όνομα)")
        notes = st.text_input("Σημειώσεις")
        
        if st.form_submit_button("Καταχώρηση", type="primary"):
            if patient and from_loc and to_loc and amb_choice:
                # Αποθήκευση χωρίς κενά
                new_trip = {"id": str(uuid.uuid4()), "date": str(trip_date), "time": trip_time, "end": trip_end, "patient": patient, "from": from_loc, "to": to_loc, "amb": amb_choice, "notes": notes}
                st.session_state.trips.append(new_trip)
                st.success("Η διακομιδή καταχωρήθηκε!")
            else:
                st.error("Συμπλήρωσε όλα τα πεδία.")

    st.divider()
    
    if not st.session_state.trips:
        st.info("Δεν υπάρχουν προγραμματισμένες διακομιδές.")
    else:
        st.subheader("Ενεργές Διακομιδές")
        sorted_trips = sorted(st.session_state.trips, key=lambda x: (x['date'], x['time']))
        
        for trip in sorted_trips:
            with st.container(border=True):
                st.markdown(f"### 🕒
