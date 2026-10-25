import streamlit as st
import time
from datetime import datetime, timedelta
import uuid
import json
import os

st.set_page_config(page_title="Κέντρο Ελέγχου Εταιρείας", layout="wide")
st.sidebar.title("Μενού Εφαρμογής")
menu = st.sidebar.radio("Επιλέξτε Ενότητα:", ["🏠 Αρχική", "🚑 Live Παρακολούθηση", "📋 Πρόγραμμα Διακομιδών"])

NAMES = ["Τ12", "Τ16", "Τ16Β", "Τ16Δ"]
FILE_NAME = "trips.json"

def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(trips):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(trips, f, ensure_ascii=False, indent=4)

if "amb" not in st.session_state:
    st.session_state.amb = {}
    for i in range(1, 5):
        st.session_state.amb[i] = {"name": NAMES[i-1], "crew": "", "origin": "", "dest": "", "target": None, "total_mins": 0, "active": False}

def save_trip():
    p = st.session_state.t_patient
    f_loc = st.session_state.t_from
    t_loc = st.session_state.t_to
    if p and f_loc and t_loc:
        trips = load_data()
        new_trip = {"id": str(uuid.uuid4()), "date": str(st.session_state.t_date), "time": st.session_state.t_time, "end": st.session_state.t_end, "patient": p, "from": f_loc, "to": t_loc, "amb": st.session_state.t_amb, "notes": st.session_state.t_notes}
        trips.append(new_trip)
        save_data(trips)
        st.session_state.t_success = True
    else:
        st.session_state.t_success = False

if menu == "🏠 Αρχική":
    st.markdown("<h1 style='text-align: center; color: #FF4B4B; font-size: 50px;'>🚑 Καλώς ήρθατε στην Εταιρεία μας</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #555;'>Η Νούμερο 1 Επιλογή στην Άμεση Ανταπόκριση και τις Διακομιδές</h3>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("""
    ### 🏆 Η Αριστεία είναι ο Πρότυπό μας
    Στην **Εταιρεία μας**, δεν κάνουμε απλώς τη δουλειά μας· θέτουμε τα πρότυπα της αγοράς. Είμαστε περήφανοι που θεωρούμαστε οι **απόλυτοι ηγέτες** στον τομέα των υπηρεσιών υγείας και διακομιδών.
    Διαθέτουμε τον **πιο σύγχρονο και άρτια εξοπλισμένο στόλο ασθενοφόρων** στην περιοχή. Κάθε όχημά μας είναι ένα κινούμενο κέντρο εντατικής φροντίδας.
    Πίσω από το τιμόνι βρίσκονται τα **πιο έμπειρα και καταρτισμένα πληρώματα**. Λειτουργούμε **24 ώρες το 24ωρο, 7 ημέρες την εβδομάδα**.
    """)
    st.write("---")
    st.success("👈 Χρησιμοποιήστε το μενού στα αριστερά για να μεταβείτε στις άλλες ενότητες.")

elif menu == "🚑 Live Παρακολούθηση":
    st.title("🚑 Κέντρο Παρακολούθησης Ασθενοφόρων")
    @st.fragment(run_every=1.0)
    def draw_ambulances():
        for i in range(1, 5):
            a = st.session_state.amb[i]
            with st.container(border=True):
                if not a["active"]:
                    c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 0.8])
                    with c1:
                        a["crew"] = st.text_input("Πλήρωμα", value=a["crew"], key=f"crew_{i}", placeholder="Ονόματα")
                    with c2:
                        a["origin"] = st.text_input("Από", key=f"o{i}")
                    with c3:
                        a["dest"] = st.text_input("Προς", key=f"d{i}")
                    with c4:
                        mins = st.number_input("Λεπτά", min_value=1, max_value=180, value=15, key=f"m{i}")
                    with c5:
                        st.write("")
                        st.write("")
                        if st.button("▶", key=f"btn{i}", use_container_width=True, type="primary"):
                            if a["origin"] and a["dest"]:
                                a["total_mins"] = mins
                                a["target"] = datetime.now() + timedelta(minutes=mins)
                                a["active"] = True
                                st.rerun()
                            else:
                                st.warning("Συμπλήρωσε διαδρομή.")
                    st.markdown(f"### 🚑 {a['name']}")
                else:
                    st.markdown(f"### 🚑 {a['name']}")
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
                        if st.button("⏹", key=f"stop{i}", use_container_width=True):
                            a["active"] = False
                            a["target"] = None
                            st.rerun()
    draw_ambulances()

elif menu == "📋 Πρόγραμμα Διακομιδών":
    st.title("📋 Πρόγραμμα Διακομιδών")
    st.subheader("Καταχώρηση Νέας Διακομιδής")
    
    st.text_input("Όνομα Ασθενούς", key="t_patient")
    st.date_input("Ημερομηνία", key="t_date")
    st.text_input("Ώρα Έναρξης", key="t_time")
    st.text_input("Ώρα Τέλους", key="t_end")
    st.text_input("Από", key="t_from")
    st.text_input("Προς", key="t_to")
    st.selectbox("Επιλογή Ασθενοφόρου", NAMES, key="t_amb")
    st.text_input("Σημειώσεις", key="t_notes")
    
    st.button("Καταχώρηση", type="primary", on_click=save_trip)
    
    if st.session_state.get("t_success") == True:
        st.success("Η διακομιδή καταχωρήθηκε με επιτυχία!")
        st.session_state.t_success = None
    elif st.session_state.get("t_success") == False:
        st.error("Συμπλήρωσε Ασθενή, Από και Προς.")
        st.session_state.t_success = None

    st.divider()
    current_trips = load_data()
    
    if not current_trips:
        st.info("Δεν υπάρχουν προγραμματισμένες διακομιδές.")
    else:
        st.subheader("Πρόγραμμα ανά Ασθενοφόρο")
        cols = st.columns(4)
        
        for idx, amb_name in enumerate(NAMES):
            with cols[idx]:
                st.markdown(f"### 🚑 {amb_name}")
                amb_trips = [t for t in current_trips if t['amb'] == amb_name]
                amb_trips = sorted(amb_trips, key=lambda x: (str(x['date']), str(x['time'])))
