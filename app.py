import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error
from datetime import date


st.set_page_config(
    page_title="Shelter Management",
    page_icon="🐾",
    layout="wide"
)

if "staff_ok" not in st.session_state:
    st.session_state["staff_ok"] = False

st.title("🐾 Animal Shelter Management System")

# adding animal photos. 
ANIMAL_PHOTOS = {
    "Bella": "images/bella.jpg",
    "Charlie": "images/charlie.jpg",
    "Daisy": "images/daisy.jpg",
    "Max": "images/max.jpg",
    "Luna": "images/luna.jpg",
    "Milo": "images/milo.jpg",
    "Oliver": "images/oliver.jpg",
    "Pepper": "images/pepper.jpg",
    "Simba": "images/simba.jpg",
    "Coco": "images/coco.jpg",
    "Rocky": "images/rocky.jpg",
    "Nala": "images/nala.jpg",
}

# Connect to MySQL database.

def get_connection():
    """Create and return a MySQL connection."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",                 
            password="Davidthedog2020!",   
            database="shelter_db"        
        )
        return conn
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None


def read_sql(query, params=None):
    """Wrapper around pandas.read_sql with simple error handling."""
    conn = get_connection()
    if conn is None:
        return None
    try:
        df = pd.read_sql(query, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Query error: {e}")
        conn.close()
        return None


def execute_sql(query, params=None, commit=False):
    """Run INSERT/UPDATE/DELETE."""
    conn = get_connection()
    if conn is None:
        return
    try:
        cur = conn.cursor()
        if params is None:
            cur.execute(query)
        else:
            cur.execute(query, params)
        if commit:
            conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        st.error(f"Execution error: {e}")
        conn.close()


# Creating Guest view 

def guest_view():
    st.subheader("Guest – Browse Available Animals")

    col1, col2, col3 = st.columns(3)

    with col1:
        species = st.selectbox("Species", ["All", "DOG", "CAT"])

    with col2:
        status = st.selectbox("Status", ["All", "Available", "Foster", "Adopted"], index=1)

    with col3:
        shelter_name_filter = st.text_input(
            "Shelter name contains (optional)", placeholder="e.g. Happy"
        )

    query = """
        SELECT
            a.name,
            a.species,
            a.breed,
            a.size,
            a.status,
            s.shelter_name,
            s.city
        FROM animals a
        JOIN shelters s ON a.shelter_id = s.shelter_id
        WHERE 1 = 1
    """
    params = []

    if species != "All":
        query += " AND a.species = %s"
        params.append(species)

    if status != "All":
        query += " AND a.status = %s"
        params.append(status)

    if shelter_name_filter:
        query += " AND s.shelter_name LIKE %s"
        params.append(f"%{shelter_name_filter}%")

    query += " ORDER BY s.shelter_name, a.name"

    df = read_sql(query, params=params)

    if df is None:
        st.info("Could not load animals.")
        return

    if df.empty:
        st.info("No animals found with these filters.")
        return

    st.write("")
    st.markdown("### Results")

    for _, row in df.iterrows():
        st.markdown("---")
        c1, c2 = st.columns([1, 2])

        with c1:
            photo_path = ANIMAL_PHOTOS.get(row["name"])
            if photo_path:
                st.image(photo_path, use_container_width=True)
            else:
                st.write("📷 No photo")

        with c2:
            name = row["name"]
            species = row["species"]
            breed = row["breed"] if row["breed"] else "Unknown"
            size = row["size"] if row["size"] else "Unknown"
            status_val = row["status"]
            shelter_name = row["shelter_name"]
            city = row["city"]

            st.markdown(f"#### {name} ({species})")
            st.markdown(f"- **Breed:** {breed}")
            st.markdown(f"- **Size:** {size}")
            st.markdown(f"- **Status:** {status_val}")
            st.markdown(f"- **Shelter:** {shelter_name} – {city}")


# Staff view.

def load_shelter_options():
    df = read_sql("SELECT shelter_id, shelter_name FROM shelters ORDER BY shelter_name")
    if df is None or df.empty:
        return {}
    return {row["shelter_name"]: int(row["shelter_id"]) for _, row in df.iterrows()}


def load_vaccine_options():
    df = read_sql("SELECT vaccine_id, vaccine_name, species FROM vaccines ORDER BY species, vaccine_name")
    if df is None or df.empty:
        return {}
    return {
        f"{row['vaccine_name']} ({row['species']})": int(row["vaccine_id"])
        for _, row in df.iterrows()
    }

# Staff view (CRUD + vaccines)

def staff_view():
    st.subheader("Staff – Manage Shelter Data")

    tabs = st.tabs([
        "View animals",
        "Add new animal",
        "Update status",
        "Delete animal",
        "Vaccines & stock",
        "Upcoming vaccinations"
    ])

    # ----- Tab 0: View animals -----
    with tabs[0]:
        df = read_sql("""
            SELECT a.animal_id, a.name, a.species, a.breed, a.size,
                   a.sex, a.status, s.shelter_name, a.intake_date
            FROM animals a
            JOIN shelters s ON a.shelter_id = s.shelter_id
            ORDER BY a.intake_date DESC
        """)
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No animals found.")

    # ----- Tab 1: Add new animal -----
    with tabs[1]:
        st.markdown("### ➕ Add a new animal")
        shelters = load_shelter_options()

        if not shelters:
            st.warning("No shelters found in database.")
        else:
            with st.form("add_animal_form"):
                name = st.text_input("Name")
                species = st.selectbox("Species", ["DOG", "CAT"])
                breed = st.text_input("Breed")
                size = st.selectbox("Size", ["Small", "Medium", "Large"])
                sex = st.selectbox("Sex", ["Female", "Male"])
                hypo = st.selectbox("Hypoallergenic", ["YES", "NO"])
                dob = st.date_input("Date of birth (optional)", value=None)
                intake = st.date_input("Intake date", value=date.today())
                status_new = st.selectbox("Status", ["Available", "Foster", "Adopted"])
                shelter_name = st.selectbox("Shelter", list(shelters.keys()))
                shelter_id = shelters[shelter_name]

                submitted = st.form_submit_button("Add animal")

                if submitted:
                    if not name.strip():
                        st.error("Name is required.")
                    else:
                        query = """
                            INSERT INTO animals
                            (name, species, size, hypoallergenic, breed, sex,
                             date_of_birth, intake_date, status, shelter_id)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """
                        params = (
                            name.strip(),
                            species,
                            size,
                            hypo,
                            breed.strip() if breed else None,
                            sex,
                            dob if dob else None,
                            intake,
                            status_new,
                            shelter_id
                        )
                        execute_sql(query, params=params, commit=True)
                        st.success(f"Animal '{name}' added successfully!")

    # ----- Tab 2: Update status -----
    with tabs[2]:
        st.markdown("### ✏️ Update animal status")

        df_animals = read_sql("""
            SELECT animal_id, name, species, status
            FROM animals
            ORDER BY name
        """)
        if df_animals is None or df_animals.empty:
            st.info("No animals to update.")
        else:
            df_animals["label"] = df_animals.apply(
                lambda r: f"{r['name']} ({r['species']}) - {r['status']}", axis=1
            )
            options = {
                row["label"]: int(row["animal_id"])
                for _, row in df_animals.iterrows()
            }

            choice = st.selectbox("Choose animal", list(options.keys()))
            new_status = st.selectbox("New status", ["Available", "Foster", "Adopted"])

            if st.button("Update status"):
                animal_id = options[choice]
                execute_sql(
                    "UPDATE animals SET status = %s WHERE animal_id = %s",
                    params=(new_status, animal_id),
                    commit=True
                )
                st.success("Status updated successfully!")

    # ----- Tab 3: Delete animal -----
    with tabs[3]:
        st.markdown("### 🗑️ Delete animal (hard delete)")

        df_animals = read_sql("""
            SELECT animal_id, name, species, status
            FROM animals
            ORDER BY name
        """)
        if df_animals is None or df_animals.empty:
            st.info("No animals to delete.")
        else:
            df_animals["label"] = df_animals.apply(
                lambda r: f"{r['name']} ({r['species']}) - {r['status']}", axis=1
            )
            options_del = {
                row["label"]: int(row["animal_id"])
                for _, row in df_animals.iterrows()
            }

            choice_del = st.selectbox("Choose animal to delete", list(options_del.keys()))
            confirm = st.checkbox("I understand this will permanently delete the record.")

            if st.button("Delete") and confirm:
                animal_id = options_del[choice_del]
                execute_sql(
                    "DELETE FROM animals WHERE animal_id = %s",
                    params=(animal_id,),
                    commit=True
                )
                st.success("Animal deleted successfully!")

    # ----- Tab 4: Vaccines & stock -----
    with tabs[4]:
        st.markdown("### 💉 Vaccines & stock")

        df_v = read_sql("""
            SELECT vaccine_id, vaccine_name, species, quantity, notes
            FROM vaccines
            ORDER BY species, vaccine_name
        """)
        if df_v is not None and not df_v.empty:
            st.dataframe(df_v, use_container_width=True)
        else:
            st.info("No vaccines found.")

        st.markdown("#### Adjust stock for an existing vaccine")
        vac_options = load_vaccine_options()

        if not vac_options:
            st.warning("No vaccines to update.")
        else:
            with st.form("update_stock_form"):
                label = st.selectbox("Choose vaccine", list(vac_options.keys()))
                vaccine_id = vac_options[label]
                delta = st.number_input(
                    "Change in quantity (positive or negative)",
                    min_value=-500,
                    max_value=500,
                    value=0,
                    step=1
                )
                submitted = st.form_submit_button("Apply change")

                if submitted:
                    if delta == 0:
                        st.info("Change is 0 – nothing to update.")
                    else:
                        execute_sql(
                            """
                            UPDATE vaccines
                            SET quantity = GREATEST(quantity + %s, 0)
                            WHERE vaccine_id = %s
                            """,
                            params=(int(delta), vaccine_id),
                            commit=True
                        )
                        st.success(f"Stock updated by {delta} for {label}.")

        st.markdown("#### Add a new vaccine")
        with st.expander("Add new vaccine"):
            with st.form("add_vaccine_form"):
                v_name = st.text_input("Vaccine name")
                v_species = st.selectbox("Species", ["DOG", "CAT"])
                v_qty = st.number_input("Initial quantity", min_value=0, max_value=10000, value=0)
                v_notes = st.text_area("Notes (optional)")
                submit_vac = st.form_submit_button("Add vaccine")

                if submit_vac:
                    if not v_name.strip():
                        st.error("Vaccine name is required.")
                    else:
                        execute_sql(
                            """
                            INSERT INTO vaccines (vaccine_name, species, quantity, notes)
                            VALUES (%s,%s,%s,%s)
                            """,
                            params=(v_name.strip(), v_species, int(v_qty), v_notes or None),
                            commit=True
                        )
                        st.success(f"Vaccine '{v_name}' added successfully!")

    # ----- Tab 5: Upcoming vaccinations -----
    with tabs[5]:
        st.markdown("### 📅 Vaccinations due in the next 30 days")

        query_due = """
            SELECT
                a.name AS animal_name,
                a.species,
                v.vaccine_name,
                vr.vaccination_date,
                vr.due_date,
                s.shelter_name
            FROM vaccination_record vr
            JOIN animals a   ON vr.animal_id  = a.animal_id
            JOIN vaccines v  ON vr.vaccine_id = v.vaccine_id
            JOIN shelters s  ON a.shelter_id  = s.shelter_id
            WHERE vr.due_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
            ORDER BY vr.due_date, a.name
        """
        df_due = read_sql(query_due)

        if df_due is not None and not df_due.empty:
            st.dataframe(df_due, use_container_width=True)
        else:
            st.info("No vaccinations due in the next 30 days.")

        st.markdown("### ⏰ Overdue vaccinations (past due_date)")
        query_overdue = """
            SELECT
                a.name AS animal_name,
                a.species,
                v.vaccine_name,
                vr.vaccination_date,
                vr.due_date,
                s.shelter_name
            FROM vaccination_record vr
            JOIN animals a   ON vr.animal_id  = a.animal_id
            JOIN vaccines v  ON vr.vaccine_id = v.vaccine_id
            JOIN shelters s  ON a.shelter_id  = s.shelter_id
            WHERE vr.due_date < CURDATE()
            ORDER BY vr.due_date, a.name
        """
        df_overdue = read_sql(query_overdue)

        if df_overdue is not None and not df_overdue.empty:
            st.dataframe(df_overdue, use_container_width=True)
        else:
            st.info("No overdue vaccinations (nice!).")



#  Sidebar "login" + mode

st.sidebar.header("Mode selection")

mode = st.sidebar.radio(
    "Choose mode",
    ["Guest", "Staff"]
)

# Simple password for staff access. 

STAFF_PASSWORD = "shelter123" 

if mode == "Staff":
    pwd = st.sidebar.text_input("Staff password", type="password")
    if st.sidebar.button("Log in"):
        if pwd == STAFF_PASSWORD:
            st.session_state["staff_ok"] = True
            st.sidebar.success("Logged in as staff.")
        else:
            st.session_state["staff_ok"] = False
            st.sidebar.error("Incorrect password.")

st.sidebar.write("---")
st.sidebar.write("Connected to: `shelter_db` (local MySQL)")

# Staff vs Guest view. 

if mode == "Staff" and st.session_state["staff_ok"]:
    staff_view()
else:
    guest_view()

