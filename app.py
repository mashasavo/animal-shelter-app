import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path

# --------------------------------------------------
# Page setup
# --------------------------------------------------
st.set_page_config(
    page_title="Animal Shelter Management System",
    page_icon="🐾",
    layout="wide"
)

if "staff_ok" not in st.session_state:
    st.session_state["staff_ok"] = False
if "staff_name" not in st.session_state:
    st.session_state["staff_name"] = None

st.title("🐾 Animal Shelter Management System")

# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DIR = Path(__file__).parent / "data"

ANIMALS_CSV = BASE_DIR / "animals.csv"
SHELTERS_CSV = BASE_DIR / "shelters.csv"
VACCINES_CSV = BASE_DIR / "vaccines.csv"
VACC_RECORD_CSV = BASE_DIR / "vaccination_record.csv"
EMPLOYEES_CSV = BASE_DIR / "employees.csv"

IMAGES_DIR = Path(__file__).parent / "images"

ANIMAL_PHOTOS = {
    "Bella": "bella.jpg",
    "Charlie": "charlie.jpg",
    "Coco": "coco.jpg",
    "Daisy": "daisy.jpg",
    "Luna": "luna.jpg",
    "Max": "max.jpg",
    "Milo": "milo.jpg",
    "Nala": "nala.jpg",
    "Oliver": "oliver.jpg",
    "Pepper": "pepper.jpg",
    "Rocky": "rocky.jpg",
    "Simba": "simba.jpg",
}

def get_image_path(name):
    fname = ANIMAL_PHOTOS.get(name)
    if not fname:
        return None
    path = IMAGES_DIR / fname
    return str(path) if path.exists() else None

# --------------------------------------------------
# Data loading
# --------------------------------------------------
@st.cache_data
def load_data():
    animals = pd.read_csv(ANIMALS_CSV, sep=";")
    shelters = pd.read_csv(SHELTERS_CSV, sep=";")
    vaccines = pd.read_csv(VACCINES_CSV, sep=";")
    vaccination_record = pd.read_csv(VACC_RECORD_CSV, sep=";")
    employees = pd.read_csv(EMPLOYEES_CSV, sep=";")

    animals = animals.merge(shelters[["shelter_id", "shelter_name", "city"]],
                            on="shelter_id", how="left")
    return animals, shelters, vaccines, vaccination_record, employees

animals, shelters, vaccines, vaccination_record, employees = load_data()

# --------------------------------------------------
# Guest view
# --------------------------------------------------
def guest_view():
    st.subheader("Guest – Browse Available Animals")

    col1, col2, col3 = st.columns(3)
    with col1:
        species = st.selectbox("Species", ["All"] + sorted(animals["species"].unique()))
    with col2:
        status = st.selectbox("Status", ["All"] + sorted(animals["status"].unique()))
    with col3:
        shelter_filter = st.text_input("Shelter name contains (optional)")

    df = animals.copy()
    if species != "All":
        df = df[df["species"] == species]
    if status != "All":
        df = df[df["status"] == status]
    if shelter_filter.strip():
        df = df[df["shelter_name"].str.contains(shelter_filter, case=False)]

    if df.empty:
        st.warning("No animals found.")
        return

    for _, row in df.iterrows():
        st.divider()
        c1, c2 = st.columns([1, 2])
        with c1:
            img = get_image_path(row["name"])
            if img:
                st.image(img, use_container_width=True)
            else:
                st.write("📷 No photo")
        with c2:
            st.markdown(f"#### {row['name']} ({row['species']})")
            st.markdown(f"- **Breed:** {row['breed']}")
            st.markdown(f"- **Size:** {row['size']}")
            st.markdown(f"- **Status:** {row['status']}")
            st.markdown(f"- **Shelter:** {row['shelter_name']} – {row['city']}")

# --------------------------------------------------
# Staff view (mock CRUD)
# --------------------------------------------------
def staff_view():
    st.subheader(f"Staff – Manage Shelter Data (Logged in as {st.session_state['staff_name']})")

    tabs = st.tabs([
        "View animals", "Add new animal", "Update status",
        "Delete animal", "Vaccines & stock", "Upcoming vaccinations"
    ])

    # View animals
    with tabs[0]:
        st.dataframe(animals, use_container_width=True)

    # Add new animal
    with tabs[1]:
        with st.form("add_animal_form"):
            name = st.text_input("Name")
            species = st.selectbox("Species", ["DOG", "CAT"])
            breed = st.text_input("Breed")
            size = st.selectbox("Size", ["Small", "Medium", "Large"])
            status_new = st.selectbox("Status", ["Available", "Foster", "Adopted"])
            shelter_name = st.selectbox("Shelter", shelters["shelter_name"].tolist())
            submitted = st.form_submit_button("Add animal")
            if submitted:
                st.success(f"Mock: Animal '{name}' would be added.")

    # Update status
    with tabs[2]:
        choice = st.selectbox("Choose animal", animals["name"].tolist())
        new_status = st.selectbox("New status", ["Available", "Foster", "Adopted"])
        if st.button("Update status"):
            st.success(f"Mock: Status of {choice} would be updated to {new_status}.")

    # Delete animal
    with tabs[3]:
        choice = st.selectbox("Choose animal to delete", animals["name"].tolist())
        if st.button("Delete"):
            st.success(f"Mock: Animal {choice} would be deleted.")

    # Vaccines & stock
    with tabs[4]:
        st.dataframe(vaccines, use_container_width=True)
        choice = st.selectbox("Choose vaccine", vaccines["vaccine_name"].tolist())
        delta = st.number_input("Change in quantity", -100, 100, 0)
        if st.button("Apply change"):
            st.success(f"Mock: Vaccine {choice} stock would change by {delta}.")

    # Upcoming vaccinations
    with tabs[5]:
        st.dataframe(vaccination_record, use_container_width=True)

# --------------------------------------------------
# Sidebar login (Employer ID + password)
# --------------------------------------------------
st.sidebar.header("Mode selection")
mode = st.sidebar.radio("Choose mode", ["Guest", "Staff"])

if mode == "Staff":
    emp_id = st.sidebar.text_input("Employer ID")
    pwd = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Log in"):
        match = employees[
            (employees["employer_id"].astype(str) == emp_id) &
            (employees["password"].astype(str) == pwd)
        ]
        if not match.empty:
            st.session_state["staff_ok"] = True
            st.session_state["staff_name"] = match.iloc[0]["name"]
            st.sidebar.success(f"Welcome {st.session_state['staff_name']}!")
        else:
            st.session_state["staff_ok"] = False
            st.session_state["staff_name"] = None
            st.sidebar.error("Invalid Employer ID or password.")

# --------------------------------------------------
# Show views
# --------------------------------------------------
if mode == "Staff" and st.session_state["staff_ok"]:
    staff_view()
else:
    guest_view()

