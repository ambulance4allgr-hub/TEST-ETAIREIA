import streamlit as st
import time
from datetime import datetime, timedelta

# Ρύθμιση της σελίδας να ανοίγει σε πλατύ παράθυρο
st.set_page_config(page_title="Κέντρο Ελέγχου Εταιρείας", layout="wide")

# --- ΠΛΑΪΝΟ ΜΕΝΟΥ ---
st.sidebar.title("Μενού Εφαρμογής")
menu = st.sidebar.radio("Επιλέξτε Ενότητα:", ["🚑 Live Παρακολούθηση", "📋 Πρόγραμμα Διακομιδών"])

# Αρχικοποίηση μνήμης για τα ασθενοφόρα
if "amb" not in st.session_state:
    st.session_state.amb = {
        i: {"name": f"Ασθενοφόρο {i}", "crew": "", "origin": "", "dest": "", "target": None, "total_mins": 0, "active": False}
        for i in range(1, 5)
    }

# Αρχικοποίηση μνήμης για τις διακομιδές
if "trips" not in st.session_state:
    st.session_state.trips = []

# ==========================================
# ΕΝΟΤΗΤΑ 1: LIVE ΠΑΡΑΚΟΛΟΥΘΗΣΗ
# ==========================================
if menu == "🚑 Live Παρακολούθηση":
    st.title("🚑 Κέντρο Παρακολούθησης Ασθενοφόρων")
    
    @st.fragment(run_every=1.0)
    def draw_ambulances():
        for i in range(1, 5):
            a = st.session_state.amb[i]
            with st.container(border=True):
                if not a["active"]:
                    c1, c2, c3, c4, c5 = st.columns([1.2, 1.2, 1, 1, 0.8])
                    with c1:
                        a["name"] = st.text_input("Όνομα", value=a["name"], key=f"name_{i}")
                    with c2:
                        a["crew"] = st.text_input("Πλήρωμα", value=a["crew"], key=f"crew_{i}", placeholder="Ονόματα")
                    with c3:
                        a["origin"] = st.text_input("Από πού", key=f"o{i}", placeholder="π.χ. Αγία Όλγα")
                    with c4:
                        a["dest"] = st.text_input("Πού", key=f"d{i}", placeholder="π.χ. Ευαγγελισμός")
                    with c5:
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
                            st.markdown(f"<div style='font-size: 35px; font-weight: bold; text-align: center; color: #FF4B4B; font-family: monospace;'>{m}:{s:02d}</div>", unsafe_allow_html=True)
                        else:
                            st.success("✅ Έφτασε!")
                    with col_btn:
                        st.write("")
                        if st.button("⏹", key=f"stop{i}", use_container_width=True):
                            a["active"] = False
                            a["target"] = None
                            st.rerun()
    
    draw_ambulances()

# ==========================================
# ΕΝΟΤΗΤΑ 2: ΠΡΟΓΡΑΜΜΑ ΔΙΑΚΟΜΙΔΩΝ
# ==========================================
elif menu == "📋 Πρόγραμμα Διακομιδών":
    st.title("📋 Πρόγραμμα Διακομιδών")
    
    # Φόρμα προσθήκης νέας διακομιδής
    with st.expander("➕ Προσθήκη Νέας Διακομιδής", expanded=True):
        with st.form("new_trip_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                patient = st.text_input("Όνομα Ασθενούς")
                trip_time = st.text_input("Ώρα (π.χ. 14:30)")
            with c2:
                from_loc = st.text_input("Από (Νοσοκομείο/Διεύθυνση)")
                to_loc = st.text_input("Προς (Νοσοκομείο/Διεύθυνση)")
            with c3:
                amb_choice = st.selectbox("Ασθενοφόρο", [f"Ασθενοφόρο {i}" for i in range(1, 5)])
                notes = st.text_input("Σημειώσεις (π.χ. Οξυγόνο, φορεία)")
                
            submitted = st.form_submit_button("Καταχώρηση", type="primary")
            if submitted:
                if patient and from_loc and to_loc:
                    st.session_state.trips.append({
                        "time": trip_time,
                        "patient": patient,
                        "from": from_loc,
                        "to": to_loc,
                        "amb": amb_choice,
                        "notes": notes
                    })
                    st.success("Η διακομιδή καταχωρήθηκε!")
                else:
                    st.error("Συμπλήρωσε τουλάχιστον: Ασθενή, Από και Προς.")

    st.divider()
    
    # Εμφάνιση των διακομιδών
    if not st.session_state.trips:
        st.info("Δεν υπάρχουν προγραμματισμένες διακομιδές.")
    else:
        st.subheader("Ενεργές Διακομιδές")
        
        # Ταξινόμηση με βάση την ώρα
        sorted_trips = sorted(st.session_state.trips, key=lambda x: x['time'])
        
        for idx, trip in enumerate(sorted_trips):
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([1, 3, 3, 1.5])
                
                with col1:
                    st.markdown(f"### 🕒 {trip['time']}")
                with col2:
                    st.markdown(f"**👤 Ασθενής:** {trip['patient']}")
                    st.caption(f"📝 {trip['notes'] if trip['notes'] else 'Χωρίς σημειώσεις'}")
                with col3:
                    st.markdown(f"🏥 **Από:** {trip['from']}")
                    st.markdown(f"🏁 **Προς:** {trip['to']}")
                with col4:
                    st.info(f"🚑 {trip['amb']}")
                    if st.button("✅ Ολοκληρώθηκε", key=f"done_{idx}", use_container_width=True):
                        # Αφαίρεση της συγκεκριμένης διακομιδής
                        st.session_state.trips.remove(trip)
                        st.rerun()
