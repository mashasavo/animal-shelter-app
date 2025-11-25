import streamlit as st
import pandas as pd
from pathlib import Path
import os

# --------------------------------------------------
# Basic page setup
# --------------------------------------------------
st.set_page_config(
    page_title="Animal Shelter Management System",
    layout="wide",
)

# Custom CSS for fonts
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Paths & helpers
# --------------------------------------------------
BASE_DIR = Path(__file__).parent/ "data"

# CSV data paths
ANIMALS_CSV = BASE_DIR / "animals.csv"
SHELTERS_CSV = BASE_DIR / "shelters.csv"
EMPLOYEES_CSV = BASE_DIR / "employees.csv"
VACCINES_CSV = BASE_DIR / "vaccines.csv"
VACC_RECORD_CSV = BASE_DIR / "vaccination_record.csv"

IMAGES_DIR = BASE_DIR / "images"

# Map animal name to image filename
ANIMAL_IMAGES = {
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


def get_image_path(animal_name: str):
    filename = ANIMAL_IMAGES.get(animal_name)
    if not filename:
        return None
    path = IMAGES_DIR / filename
    return path if path.exists() else None


# --------------------------------------------------
# Data loading (from CSV instead of MySQL)
# --------------------------------------------------
@st.cache_data
def load_data():
    animals = pd.read_csv(ANIMALS_CSV, sep=';')
    shelters = pd.read_csv(SHELTERS_CSV sep=';')
    employees = pd.read_csv(EMPLOYEES_CSV sep=';')
    vaccines = pd.read_csv(VACCINES_CSV sep=';')
    vaccination_record = pd.read_csv(VACC_RECORD_CSV sep=';')

    # Join shelter name into animals for convenience
    animals = animals.merge(shelters[["shelter_id", "shelter_name", "city"]],
                            on="shelter_id", how="left")

    return animals, shelters, employees, vaccines, vaccination_record


animals, shelters, employees, vaccines, vaccination_record = load_data()

# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("🐾 Animal Shelter Management System")

st.caption(
    "Demo version on Streamlit Cloud – data is loaded from CSV snapshots of the MySQL database."
)

# --------------------------------------------------
# Tabs 
# --------------------------------------------------
tab_guest, tab_staff_animals, tab_staff_vaccines = st.tabs(
    [
        "Guest – Browse Available Animals",
        "Staff – Animals (read-only)",
        "Staff – Vaccinations & Stock (read-only)",
    ]
)

# --------------------------------------------------
# TAB 1 – Guest view (filters + cards + images)
# --------------------------------------------------
with tab_guest:
    st.subheader("Guest – Browse Available Animals")

    # Filters
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        species_options = ["All"] + sorted(animals["species"].dropna().unique().tolist())
        selected_species = st.selectbox("Species", species_options, index=0)

    with col2:
        status_options = ["All"] + sorted(animals["status"].dropna().unique().tolist())
        selected_status = st.selectbox("Status", status_options, index=0)

    with col3:
        shelter_filter = st.text_input("Shelter name contains (optional)", "")

    # Apply filters
    filtered = animals.copy()

    if selected_species != "All":
        filtered = filtered[filtered["species"] == selected_species]

    if selected_status != "All":
        filtered = filtered[filtered["status"] == selected_status]

    if shelter_filter.strip():
        filtered = filtered[
            filtered["shelter_name"]
            .fillna("")
            .str.contains(shelter_filter.strip(), case=False)
        ]

    filtered = filtered.sort_values(["shelter_name", "name"])

    if filtered.empty:
        st.warning("No animals found with these filters.")
    else:
        st.success(f"Found {len(filtered)} animals matching your filters.")

        # Card-style layout
        for _, row in filtered.iterrows():
            card_cols = st.columns([1, 2])
            with card_cols[0]:
                img_path = get_image_path(row["name"])
                if img_path:
                    st.image(str(img_path), use_container_width=True)
                else:
                    # Tiny placeholder
                    st.write("📷 No photo yet")

            with card_cols[1]:
                st.markdown(f"### {row['name']}")
                st.markdown(
                    f"**Species:** {row['species']}  \n"
                    f"**Breed:** {row['breed']}  \n"
                    f"**Size:** {row['size']}  \n"
                    f"**Status:** {row['status']}  \n"
                    f"**Shelter:** {row['shelter_name']} ({row['city']})"
                )
            st.divider()

# --------------------------------------------------
# TAB 2 – Staff animals overview (read-only)
# --------------------------------------------------
with tab_staff_animals:
    st.subheader("Staff – Animals overview (read-only in cloud demo)")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total animals", len(animals))
    with col2:
        st.metric("Dogs", len(animals[animals["species"] == "DOG"]))
    with col3:
        st.metric("Cats", len(animals[animals["species"] == "CAT"]))

    st.markdown("#### Animals by shelter")
    animals_by_shelter = (
        animals.groupby("shelter_name")["animal_id"]
        .count()
        .reset_index(name="animal_count")
        .sort_values("animal_count", ascending=False)
    )
    st.dataframe(animals_by_shelter, use_container_width=True)

    st.markdown("#### Full animals table (snapshot)")
    st.dataframe(
        animals[
            [
                "animal_id",
                "name",
                "species",
                "breed",
                "size",
                "status",
                "shelter_name",
            ]
        ].sort_values("animal_id"),
        use_container_width=True,
    )

    st.info(
        "In the real system, create / update / delete operations are executed "
        "via the MySQL scripts and triggers. This Streamlit view shows a "
        "read-only snapshot taken from the same database."
    )

# --------------------------------------------------
# TAB 3 – Staff vaccinations & stock (read-only)
# --------------------------------------------------
with tab_staff_vaccines:
    st.subheader("Staff – Vaccinations & stock (read-only in cloud demo)")

    # Vaccines stock summary
    st.markdown("#### Current vaccine stock")
    st.dataframe(
        vaccines[["vaccine_id", "vaccine_name", "species", "quantity"]]
        .sort_values(["species", "vaccine_name"]),
        use_container_width=True,
    )

    # Simple overdue vaccinations report
    st.markdown("#### Overdue vaccinations (based on CSV snapshot)")

    # Try to parse due_date if present
    vr = vaccination_record.copy()
    if "due_date" in vr.columns:
        try:
            vr["due_date"] = pd.to_datetime(vr["due_date"])
        except Exception:
            pass

    overdue = vr.merge(animals[["animal_id", "name", "species", "status", "shelter_name"]],
                       on="animal_id", how="left")
    if "due_date" in overdue.columns and pd.api.types.is_datetime64_any_dtype(
        overdue["due_date"]
    ):
        today = pd.Timestamp.today().normalize()
        overdue = overdue[
            (overdue["due_date"] < today)
            & overdue["status"].isin(["Available", "Foster"])
        ]
        overdue = overdue.sort_values("due_date")
        if overdue.empty:
            st.success("No overdue vaccinations in this snapshot.")
        else:
            st.dataframe(
                overdue[
                    ["vaccination_id", "name", "species", "due_date", "shelter_name"]
                ],
                use_container_width=True,
            )
    else:
        st.info("Due dates are not available as proper dates in the CSV snapshot.")

    st.markdown("#### Total vaccinations by species")
    vacc_by_species = (
        vaccination_record.merge(
            animals[["animal_id", "species"]], on="animal_id", how="left"
        )
        .groupby("species")["vaccination_id"]
        .count()
        .reset_index(name="total_vaccinations")
    )
    st.dataframe(vacc_by_species, use_container_width=True)

    st.info(
        "In the original MySQL version, a trigger automatically decrements "
        "vaccine stock whenever a new vaccination record is inserted. "
        "Here on Streamlit Cloud we show the **resulting stock levels** "
        "from the exported CSV data."
    )

