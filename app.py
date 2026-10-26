import streamlit as st
import time
from datetime import datetime, timedelta
import uuid

st.set_page_config(page_title="Κέντρο Ελέγχου Εταιρείας", layout="wide")
st.sidebar.title("Μενού Εφαρμογής")
menu = st.sidebar.radio("Επιλέξτε Ενότητα:", ["🏠 Αρχική", "🚑 Live Παρακολούθηση", "📋 Πρόγραμμα Διακομιδών"])

if "names" not in st.session_state:
    st.session_state.names = ["Τ12", "Τ16", "Τ16Β", "Τ16Δ", "Κενό 5", "Κενό 6"]

if "amb" not in st.session_state:
    st.session_state.amb = {}
    for i in range(1, 7):
        st.session_state.amb[i] = {"crew": "", "origin": "", "dest": "", "target": None, "total_mins": 0, "active": False}

if "trips" not in st.session_state:
    st.session_state.trips = []

def add_trip():
    p = st.session_state.get("f_patient", "")
    f_loc = st.session_state.get("f_from", "")
    t_loc = st.session_state.get("f_to", "")
    if p and f_loc and t_loc:
        new_trip = {"id": str(uuid.uuid4()), "date": str(st.session_state.get("f_date")), "time": st.session_state.get("f_time", ""), "end": st.session_state.get("f_end", ""), "patient": p, "from": f_loc, "to": t_loc, "amb": st.session_state.get("f_amb"), "notes": st.session_state.get("f_notes", "")}
        st.session_state.trips.append(new_trip)
        st.session_state.trip_success = True
    else:
        st.session_state.trip_success = False

def start_amb(i):
    a = st.session_state.amb[i]
    if a["origin"] and a["dest"]:
        a["total_mins"] = st.session_state.get(f"m_{i}", 15)
        a["target"] = datetime.now() + timedelta(minutes=a["total_mins"])
        a["active"] = True

def stop_amb(i):
    st.session_state.amb[i]["active"] = False
    st.session_state.amb[i]["target"] = None

def delete_trip(trip_id):
    st.session_state.trips = [t for t in st.session_state.trips if t["id"] != trip_id]

if menu == "🏠 Αρχική":
    st.markdown("<h1 style='text-align: center; color: #FF4B4B; font-size: 50px;'>🚑 Καλώς ήρθατε</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #555;'>Ηγετική Παρουσία στις Υπηρεσίες Υγείας και Διακομιδών</h3>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("""
    ### 🏆 Το Όραμά μας
    Στην εταιρεία μας, δεσμευόμαστε στην παροχή υπηρεσιών διακομιδής και άμεσης ανταπόκρισης υψηλών προδιαγραφών. Θέτουμε ως προτεραιότητα την ασφάλεια, την αξιοπιστία και την άριστη εξυπηρέτηση των ασθενών, αποτελώντας τον αξιόπιστο συνεργάτη των νοσηλευτικών ιδρυμάτων και των οικογενειών.
    ### 🚑 Σύγχρονος Στόλος & Τεχνολογία
    Επενδύουμε διαρκώς στον εκσυγχρονισμό του εξοπλισμού μας. Ο στόλος των ασθενοφόρων μας τηρεί τις αυστηρότερες προδιαγραφές ασφαλείας και είναι εξοπλισμένος με προηγμένα συστήματα ιατρικής υποστήριξης.
    ### 👨‍⚕️ Εξειδικευμένο Ανθρώπινο Δυναμικό
    Η δύναμή μας έγκειται στους ανθρώπους μας. Τα πληρώματα στελεχώνονται αποκλειστικά από πιστοποιημένους διασώστες και έμπειρους οδηγούς. Με υψηλό αίσθημα ευθύνης διαχειρίζονται κάθε περιστατικό με ακρίβεια και σεβασμό.
    ### ⏱️ Διαθεσιμότητα 24/7
    Οι υπηρεσίες μας βρίσκονται σε πλήρη επιχειρησιακή ετοιμότητα 24 ώρες το 24ωρο, 365 ημέρες τον χρόνο.
    """)

elif menu == "🚑 Live Παρακολούθηση":
    st.title("🚑 Κέντρο Παρακολούθησης Ασθενοφόρων")
    
    with st.expander("⚙️ Επεξεργασία Ονομάτων"):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.session_state.names[0] = st.text_input("Όνομα 1", st.session_state.names[0])
            st.session_state.names[1] = st.text_input("Όνομα 2", st.session_state.names[1])
        with c2:
            st.session_state.names[2] = st.text_input("Όνομα 3", st.session_state.names[2])
            st.session_state.names[3] = st.text_input("Όνομα 4", st.session_state.names[3])
        with c3:
            st.session_state.names[4] = st.text_input("Όνομα 5", st.session_state.names[4])
            st.session_state.names[5] = st.text_input("Όνομα 6", st.session_state.names[5])

    @st.fragment(run_every=1.0)
    def draw_ambulances():
        for i in range(1, 7):
            a = st.session_state.amb[i]
            with st.container(border=True):
                if not a["active"]:
                    c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 0.8])
                    with c1:
                        a["crew"] = st.text_input("Πλήρωμα", value=a["crew"], key=f"c_{i}", placeholder="Ονόματα")
                    with c2:
                        a["origin"] = st.text_input("Από", key=f"o_{i}")
                    with c3:
                        a["dest"] = st.text_input("Προς", key=f"d_{i}")
                    with c4:
                        st.number_input("Λεπτά", min_value=1, max_value=180, value=15, key=f"m_{i}")
                    with c5:
                        st.write("")
                        st.write("")
                        st.button("▶", key=f"b_{i}", use_container_width=True, type="primary", on_click=start_amb, args=(i,))
                    st.markdown(f"### 🚑 {st.session_state.names[i-1]}")
                else:
                    st.markdown(f"### 🚑 {st.session_state.names[i-1]}")
                    col_info, col_prog, col_timer, col_btn = st.columns([2, 1.5, 1.2, 0.8])
                    with col_info:
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
                        st.button("⏹", key=f"s_{i}", use_container_width=True, on_click=stop_amb, args=(i,))
    draw_ambulances()

elif menu == "📋 Πρόγραμμα Διακομιδών":
    st.title("📋 Πρόγραμμα Διακομιδών")
    st.subheader("Καταχώρηση Νέας Διακομιδής")
    
    st.text_input("Όνομα Ασθενούς", key="f_patient")
    st.date_input("Ημερομηνία", key="f_date")
    st.text_input("Ώρα Έναρξης", key="f_time")
    st.text_input("Ώρα Τέλους", key="f_end")
    st.text_input("Από", key="f_from")
    st.text_input("Προς", key="f_to")
    st.selectbox("Επιλογή Ασθενοφόρου", st.session_state.names, key="f_amb")
    st.text_input("Σημειώσεις", key="f_notes")
    st.button("Καταχώρηση", type="primary", on_click=add_trip)
    
    if st.session_state.get("trip_success") =
