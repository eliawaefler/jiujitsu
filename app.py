"""
st. ui for inputing new jj positions
"""
import os
import time
import streamlit as st
import uuid
from random import randint
import json
from datetime import datetime
import neon


def generate_uuid():
    return str(uuid.uuid4())

# Positionen Formular
def position_form():
    st.subheader("Position Eingabe")
    # test
    pos_data = {
        "guid": generate_uuid(),
        "realm": st.selectbox("Realm", options=["Standing", "Guard", "Controll", "Submission"], key="p_realm"),
        "class": st.text_input("Class", key="p_class"),
        "family": st.text_input("Family", key="p_fam"),
        "name": st.text_input("Name", key="p_name"),
        "id": st.text_input("ID", key="p_id"),
        "code": st.text_input("Code", key="p_code"),
        "btg_top": st.text_input("BTG Top", key="p_btgt"),
        "btg_pass": st.text_input("BTG Pass", key="p_btgp"),
        "btg_dom": st.text_input("BTG Dom", key="p_btgdom"),
        "variant": st.text_input("Variant", key="p_var"),
        "specfics": st.text_input("Specfics", key="p_spec"),
        "level": st.text_input("Level", key="p_lev"),
        "alt_names": st.text_input("Alternative Namen", key="p_altn"),
        #"created_by": st.text_input("Erstellt von", key="p_creator"),
        "created_at": datetime.now().isoformat()
    }
    return pos_data

# Moves Formular
def move_form():
    st.subheader("Move Eingabe")
    move_data_in = {
        "m_guid": generate_uuid(),
        "m_from_pos": st.text_input("Von Position"),
        "m_from_tb": st.text_input("Von TB"),
        "m_to_pos": st.text_input("Zu Position"),
        "m_to_tb": st.text_input("Zu TB"),
        "m_category": st.text_input("Kategorie"),
        "m_name": st.text_input("Name"),
        "m_code": st.text_input("Code"),
        "m_infos": st.text_area("Infos"),
        "m_step1": st.text_area("Schritt 1"),
        "m_step2": st.text_area("Schritt 2"),
        "m_step3": st.text_area("Schritt 3"),
        "m_counter1": st.text_area("Konter 1"),
        "m_counter2": st.text_area("Konter 2"),
        "m_counter3": st.text_area("Konter 3"),
        "m_family": st.text_input("Family"),
        "m_level": st.text_input("Level"),
        #"m_created_by": st.text_input("Erstellt von"),
        "m_created_at": datetime.now().isoformat()
    }
    return move_data_in

def reset_sst(incl_page=False):
    if incl_page:
        sst["page"] = "home"
    return 0

def innit_sst():
    if "page" not in sst:
        sst["page"] = "home"
    reset_sst()




def main():

    if sst.page == "home":
        st.title("BJJ Positionen & Moves Verwaltung")

        if st.button("drills"):
            sst.page = "drills"
            st.rerun()
        # Tabs für Positionen und Moves
        tab1, tab2 = st.tabs(["Positionen", "Moves"])

        with tab1:
            position_data = position_form()
            if st.button("Position speichern"):
                st.json(position_data)
                with open("positions.json", "a") as file:
                    file.write(json.dumps(position_data) + "\n")
                st.success("Position gespeichert!")

        with tab2:
            move_data = move_form()
            if st.button("Move speichern"):
                st.json(move_data)
                with open("moves.json", "a") as file:
                    file.write(json.dumps(move_data) + "\n")
                st.success("Move gespeichert!")
    elif sst.page == "drills":
        st.subheader("drills")
        all_drills = neon.read_db(os.environ["NEON_KEY_jj"], "drills")
        d_class = st.selectbox("from ", index=0, options=set(["all"] + [d[1] for d in all_drills]))
        if st.button("random drill"):
            if d_class == "all":
                drill = all_drills[randint(0, len(all_drills)-1)]
            else:
                class_drills = [d for d in all_drills if d[1] == d_class]
                drill = class_drills[randint(0, len(class_drills)-1)]
            st.write(f"from: {drill[2]}")
            st.write(f"do: {drill[4]}")
            time.sleep(5)


if __name__ == '__main__':
    sst = st.session_state
    innit_sst()
    main()

