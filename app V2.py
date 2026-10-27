import os
import json
from datetime import datetime

import streamlit as st
import numpy as np
import pandas as pd


st.set_page_config(page_title="Mining Health, Safety and Equipment Monitoring", page_icon="🏗️", layout="wide")

EQUIPMENT_FILE = "equipment.csv"
WORKERS_FILE = "workers.csv"
RISK_FILE = "risk_register.csv"
INCIDENTS_FILE = "incidents.csv"
USERS_FILE = "users.json"


                  ########## A ###########
#User Login Details#
users = {
    "Administrator": {
        "password": "admin123",
        "role": "Administrator"
    },

    "Safety Officer": {
        "password": "safety123",
        "role": "Safety Officer"
    },

    "Mining Engineer": {
        "password": "mining123",
        "role": "Mining Engineer"
    },

    "Maintenance Engineer": {
        "password": "maintenance123",
        "role": "Maintenance Engineer"
    },

    "Manager": {
        "password": "manager123",
        "role": "Manager"
    }
}

#Users added/changed by the Administrator are saved in users.json (see section H)
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)

#Granting Access Based on Role#
permissions = {
    "Administrator": [
        "dashboard",
        "worker safety",
        "safety incidents",
        "equipment",
        "maintenance",
        "risk assessment",
        "reports",
        "manage users"
    ],

    "Safety Officer": [
        "dashboard",
        "worker safety",
        "safety incidents",
        "risk assessment",
        "reports"
    ],

    "Mining Engineer": [
        "dashboard",
        "worker safety",
        "safety incidents",
        "equipment",
        "maintenance",
        "risk assessment",
        "reports"
    ],

    "Maintenance Engineer": [
        "dashboard",
        "equipment",
        "maintenance",
        "reports"
    ],

    "Manager": [
        "dashboard",
        "worker safety",
        "safety incidents",
        "equipment",
        "maintenance",
        "risk assessment",
        "reports"
    ]
}

#Ask the user to log in (Streamlit version: session_state keeps the user logged in)
if "role" not in st.session_state:
    st.session_state.role = None
    st.session_state.username = None

if "show_login" not in st.session_state:
    st.session_state.show_login = False

#Cover page (shown first; the Log in button takes the user to the login form)
if st.session_state.role is None and not st.session_state.show_login:
    st.markdown("<h1 style='text-align: center;'>🏗️ Mining Health, Safety and Equipment Monitoring</h1>",
                unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem;'>"
                "A monitoring tool for worker safety, equipment condition, maintenance and risk."
                "</p>", unsafe_allow_html=True)
    st.write("")

    f1, f2, f3 = st.columns(3)
    with f1:
        st.subheader("Worker Safety")
        st.write("Track PPE compliance, training, fatigue, near misses and incidents.")
    with f2:
        st.subheader("Equipment Monitoring")
        st.write("Monitor temperature and vibration, and flag equipment that needs inspection.")
    with f3:
        st.subheader("Maintenance & Risk")
        st.write("Identify overdue equipment, low availability and high-risk hazards.")

    st.write("")
    _, centre, _ = st.columns([2, 1, 2])
    with centre:
        if st.button("Log in", type="primary", use_container_width=True):
            st.session_state.show_login = True
            st.rerun()

    st.write("")
    st.caption("MINN2020A Final Project.")
    st.stop()

if st.session_state.role is None:
    st.title("Mining Health, Safety and Equipment Monitoring")
    if st.button("← Back to cover page"):
        st.session_state.show_login = False
        st.rerun()
    st.subheader("Login")
    username = st.text_input("Enter username")
    password = st.text_input("Enter password", type="password")

    if st.button("Log in"):
        #Check the login details
        if username in users and users[username]["password"] == password:
            st.session_state.role = users[username]["role"]
            st.session_state.username = username
            st.rerun()
        elif username not in users:
            st.error("Access denied. Invalid username.")
        else:
            st.error("Invalid username or password")
    st.stop()

#After Logging in (Response to User Input)
role = st.session_state.role
st.sidebar.success(f"Login successful! Welcome {role}")
st.sidebar.write("Access granted to the following sections:")
page = st.sidebar.radio("Navigate", permissions[role])

if st.sidebar.button("Log out"):
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.show_login = False   # return to the cover page
    st.rerun()


                  ########### B ###########
#Worker Health and Safety Monitoring#
def worker_page():
    st.header("Worker Health and Safety Monitoring")

    with st.form("worker_form"):
        #Worker Information
        worker_id = st.text_input("Enter Worker ID")
        department = st.text_input("Enter Department")
        job_role = st.text_input("Enter Job Role")
        shift = st.selectbox("Enter Shift", ["Day", "Afternoon", "Night"])

        #Safety Information
        ppe = st.selectbox("Is PPE compliant?", ["Yes", "No"]).upper()
        training = st.selectbox("Has safety training been completed?", ["Yes", "No"]).upper()
        fatigue = st.slider("Enter fatigue level (1-5)", 1, 5, 1)
        observations = st.text_area("Safety observations")
        near_misses = st.number_input("Enter number of near misses", min_value=0, step=1)
        previous_incidents = st.number_input("Enter number of previous incidents", min_value=0, step=1)
        submitted = st.form_submit_button("Assess worker")

    if not submitted:
        return
    if not worker_id.strip():
        st.warning("Enter a Worker ID.")
        return

    #Displaying Worker information
    st.subheader("WORKER INFORMATION")
    st.write("Worker ID:", worker_id)
    st.write("Department:", department)
    st.write("Job Role:", job_role)
    st.write("Shift:", shift)
    st.write("PPE Compliant:", ppe)
    st.write("Safety Training Completed:", training)
    st.write("Fatigue Level:", fatigue)
    st.write("Near Misses:", near_misses)
    st.write("Previous Incidents:", previous_incidents)

    #Checking for Safety Warnings
    risk = "Low"

    if ppe == "NO":
        st.warning("WARNING: PPE requirements are not being met.")
        risk = "High"

    if training == "NO":
        st.warning("WARNING: Worker has not completed safety training.")
        risk = "High"

    if fatigue >= 4:
        st.warning("WARNING: High fatigue level detected.")
        risk = "High"

    if near_misses >= 1:
        st.warning("WARNING: Previous near miss recorded.")
        if risk == "Low":
            risk = "Medium"

    if previous_incidents >= 1:
        st.warning("WARNING: Previous safety incident recorded.")
        if risk == "Low":
            risk = "Medium"

    if risk == "High":
        st.error(f"Risk Level: {risk}")
    elif risk == "Medium":
        st.warning(f"Risk Level: {risk}")
    else:
        st.success(f"Risk Level: {risk}")

    #Save to workers.csv (headers match the existing file)
    new_row = pd.DataFrame([{
        "Worker_ID": worker_id,
        "Department": department,
        "Job_Role": job_role,
        "Shift": shift,
        "PPE_Compliant": ppe.title(),
        "Safety_Training_Completed": training.title(),
        "Fatigue_Level_1_to_5": fatigue,
        "Safety_Observations": observations,
        "Near_Misses": near_misses,
        "Previous_Incidents": previous_incidents,
        "Risk_Level": risk,
    }])
    new_row.to_csv(WORKERS_FILE, mode="a", index=False,
                   header=not os.path.exists(WORKERS_FILE))
    st.info("Worker record saved.")


                  ########### C ###########
#Equipment Condition Monitoring, Maintenance Monitoring and Risk Assessment#
# NOTE: All thresholds are educational prototype values only. They are NOT
# actual manufacturer or mine safety limits.

COL_ID = "Equipment ID"
COL_TYPE = "Equipment type"
COL_OP = "Operating hours"
COL_DOWN = "Downtime"
COL_TEMP = "Temperature (°C)"
COL_VIB = "Vibration (mm/s)"
COL_BRAKE = "Brake status"
COL_TYRE = "Tyre status"
COL_ENGINE = "Engine status"
COL_MAINT = "Maintenance status"

TEMP_WARNING = 80      # >= 80 is Warning
TEMP_CRITICAL = 100    # > 100 is Critical
VIB_WARNING = 5        # >= 5 is Warning
VIB_CRITICAL = 8       # > 8 is Critical

LOW_AVAILABILITY = 85.0        # % - below this = low availability
EXCESSIVE_DOWNTIME_PCT = 15.0  # % of total time - above this = excessive downtime
REPEATED_ALERT_COUNT = 2       # this many abnormal readings = repeated alerts

BAD_STATUS_WORDS = ["fault", "worn", "poor", "fail", "critical", "bad",
                    "damage", "replace", "leak", "overheat", "low"]

DISCLAIMER = ("These values are educational prototype thresholds only and must "
              "not be interpreted as actual manufacturer or mine safety limits.")


def load_equipment():
    """Read equipment.csv and make sure numeric columns are numeric."""
    if not os.path.exists(EQUIPMENT_FILE):
        st.error(f"{EQUIPMENT_FILE} not found. Place it in the same folder as app.py.")
        return None
    df = pd.read_csv(EQUIPMENT_FILE)
    df.columns = [c.strip() for c in df.columns]
    for col in [COL_OP, COL_DOWN, COL_TEMP, COL_VIB]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


#d) Equipment Database#
EQUIPMENT_TYPES = ["Haul truck", "Loader", "Excavator", "Drilling machine", "Bulldozer",
                   "Scraper winch", "Crusher", "Conveyor", "Other"]
MAINTENANCE_OPTIONS = ["Up to date", "Due", "Overdue", "Under maintenance"]


def equipment_database():
    """View, search and add records in the equipment repository (equipment.csv)."""
    st.subheader("Equipment database")
    df = load_equipment()
    if df is None:
        return

    #Search and filter
    s1, s2 = st.columns(2)
    search = s1.text_input("Search equipment (ID, type, status...)")
    types = s2.multiselect("Filter by equipment type", sorted(df[COL_TYPE].astype(str).unique()))
    filtered = df.copy()
    if search.strip():
        mask = filtered.astype(str).apply(
            lambda col: col.str.contains(search.strip(), case=False, regex=False)).any(axis=1)
        filtered = filtered[mask]
    if types:
        filtered = filtered[filtered[COL_TYPE].astype(str).isin(types)]
    st.write(f"**{len(filtered)}** of {len(df)} records shown")
    st.dataframe(filtered, use_container_width=True, hide_index=True)

    #Add a new equipment record / reading
    with st.expander("Add equipment record"):
        file_columns = [c.strip() for c in pd.read_csv(EQUIPMENT_FILE, nrows=0).columns]
        with st.form("equipment_form", clear_on_submit=True):
            a1, a2, a3 = st.columns(3)
            eq_id = a1.text_input("Equipment ID (e.g. TRK-012)")
            eq_type = a2.selectbox("Equipment type", EQUIPMENT_TYPES)
            manufacturer = a3.text_input("Manufacturer")
            b1, b2, b3, b4 = st.columns(4)
            op_hours = b1.number_input("Operating hours", min_value=0.0, step=1.0)
            downtime = b2.number_input("Downtime (hours)", min_value=0.0, step=1.0)
            temp = b3.number_input("Temperature (°C)", min_value=-20.0, max_value=200.0, value=60.0)
            vib = b4.number_input("Vibration (mm/s)", min_value=0.0, max_value=50.0, value=2.0)
            c1, c2, c3, c4 = st.columns(4)
            brake = c1.selectbox("Brake status", ["Good", "Worn", "Faulty"])
            tyre = c2.selectbox("Tyre status", ["Good", "Worn", "Damaged", "N/A"])
            engine = c3.selectbox("Engine status", ["Good", "Overheating", "Faulty", "N/A"])
            maint = c4.selectbox("Maintenance status", MAINTENANCE_OPTIONS)
            fuel = st.number_input("Fuel consumption (L/h)", min_value=0.0, step=1.0)
            submitted = st.form_submit_button("Add record")

        if submitted:
            if not eq_id.strip():
                st.warning("Enter an Equipment ID.")
                return
            values = {COL_ID: eq_id.strip().upper(), COL_TYPE: eq_type, "Manufacturer": manufacturer,
                      COL_OP: op_hours, COL_DOWN: downtime, COL_TEMP: temp, COL_VIB: vib,
                      COL_BRAKE: brake, COL_TYRE: tyre, COL_ENGINE: engine, COL_MAINT: maint,
                      "Fuel consumption": fuel,
                      "Availability": round(calculate_availability(op_hours, downtime), 1)}
            #Match the column order of the existing file; unknown columns are left blank
            row = []
            for col in file_columns:
                match = [v for k, v in values.items() if col.lower().startswith(k.lower())]
                row.append(match[0] if match else "")
            #Make sure the file ends with a new line before appending
            with open(EQUIPMENT_FILE, "rb") as f:
                content = f.read()
            if content and not content.endswith(b"\n"):
                with open(EQUIPMENT_FILE, "a", encoding="utf-8", newline="") as f:
                    f.write("\n")
            pd.DataFrame([row], columns=file_columns).to_csv(EQUIPMENT_FILE, mode="a", index=False, header=False)
            st.success(f"Record for {eq_id.strip().upper()} saved.")
            for level, text in condition_messages(pd.Series(values)):
                show_message(level, text)


#e) Equipment Condition Monitoring#
def classify_temperature(temp):
    if pd.isna(temp):
        return "Unknown"
    if temp > TEMP_CRITICAL:
        return "Critical"
    if temp >= TEMP_WARNING:
        return "Warning"
    return "Normal"


def classify_vibration(vib):
    if pd.isna(vib):
        return "Unknown"
    if vib > VIB_CRITICAL:
        return "Critical"
    if vib >= VIB_WARNING:
        return "Warning"
    return "Normal"


def status_is_bad(value):
    text = str(value).lower()
    return any(word in text for word in BAD_STATUS_WORDS)


def overall_condition(temp_status, vib_status):
    """Worst of the two parameter statuses."""
    if "Critical" in (temp_status, vib_status):
        return "Critical"
    if "Warning" in (temp_status, vib_status):
        return "Warning"
    return "Normal"


def condition_messages(row):
    """Build the NORMAL / WARNING / CRITICAL messages for one equipment row."""
    messages = []
    t = classify_temperature(row[COL_TEMP])
    v = classify_vibration(row[COL_VIB])

    if t == "Critical":
        messages.append(("CRITICAL", "Equipment temperature exceeds predefined threshold. Inspection required."))
    elif t == "Warning":
        messages.append(("WARNING", "Equipment temperature approaching predefined threshold."))

    if v == "Critical":
        messages.append(("CRITICAL", "Equipment vibration exceeds predefined threshold. Inspection required."))
    elif v == "Warning":
        messages.append(("WARNING", "Equipment vibration approaching predefined threshold."))

    for label, col in [("Brake", COL_BRAKE), ("Tyre", COL_TYRE), ("Engine", COL_ENGINE)]:
        if status_is_bad(row[col]):
            messages.append(("WARNING", f"{label} status reported as '{row[col]}'. Check recommended."))

    if not messages:
        messages.append(("NORMAL", "Equipment operating within defined monitoring limits."))
    return messages


def add_condition_columns(df):
    df = df.copy()
    df["Temperature status"] = df[COL_TEMP].apply(classify_temperature)
    df["Vibration status"] = df[COL_VIB].apply(classify_vibration)
    df["Overall condition"] = df.apply(
        lambda r: overall_condition(r["Temperature status"], r["Vibration status"]), axis=1)
    # Number of abnormal parameters in each row (used for "repeated alerts")
    df["Alert count"] = (
        (df["Temperature status"] != "Normal").astype(int)
        + (df["Vibration status"] != "Normal").astype(int)
        + df[COL_BRAKE].apply(status_is_bad).astype(int)
        + df[COL_TYRE].apply(status_is_bad).astype(int)
        + df[COL_ENGINE].apply(status_is_bad).astype(int)
    )
    return df


def show_message(level, text):
    if level == "CRITICAL":
        st.error(f"CRITICAL: {text}")
    elif level == "WARNING":
        st.warning(f"WARNING: {text}")
    else:
        st.success(f"NORMAL: {text}")


def colour_condition(value):
    colours = {"Critical": "background-color: #ff4b4b; color: white",
               "Warning": "background-color: #ffc83d; color: black",
               "Normal": "background-color: #2ecc71; color: black"}
    return colours.get(value, "")


def equipment_page():
    st.header("Equipment Condition Monitoring")
    st.caption(DISCLAIMER)

    df = load_equipment()
    if df is None:
        return
    df = add_condition_columns(df)

    with st.expander("Monitoring thresholds (prototype values)"):
        st.table(pd.DataFrame({
            "Parameter": ["Temperature", "Vibration"],
            "Normal": [f"< {TEMP_WARNING} °C", f"< {VIB_WARNING} mm/s"],
            "Warning": [f"{TEMP_WARNING}–{TEMP_CRITICAL} °C", f"{VIB_WARNING}–{VIB_CRITICAL} mm/s"],
            "Critical": [f"> {TEMP_CRITICAL} °C", f"> {VIB_CRITICAL} mm/s"],
        }))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total equipment", len(df))
    c2.metric("Normal", int((df["Overall condition"] == "Normal").sum()))
    c3.metric("Warning", int((df["Overall condition"] == "Warning").sum()))
    c4.metric("Critical", int((df["Overall condition"] == "Critical").sum()))

    st.subheader("Check a single piece of equipment")
    selected = st.selectbox("Select equipment", df[COL_ID].astype(str).unique())
    row = df[df[COL_ID].astype(str) == selected].iloc[-1]  # latest reading
    m1, m2 = st.columns(2)
    m1.metric("Temperature (°C)", row[COL_TEMP])
    m2.metric("Vibration (mm/s)", row[COL_VIB])
    for level, text in condition_messages(row):
        show_message(level, text)

    st.subheader("All equipment")
    show_cols = [COL_ID, COL_TYPE, COL_TEMP, "Temperature status",
                 COL_VIB, "Vibration status", "Overall condition"]
    styled = df[show_cols].style.map(
        colour_condition,
        subset=["Temperature status", "Vibration status", "Overall condition"])
    st.dataframe(styled, use_container_width=True)

    flagged = df[df["Overall condition"] != "Normal"]
    if not flagged.empty:
        st.subheader("Equipment requiring inspection")
        st.dataframe(flagged[show_cols], use_container_width=True)

    st.divider()
    equipment_database()


#f) Equipment Maintenance Monitoring#
def calculate_availability(operating, downtime):
    """Availability = Operating Time / (Downtime + Operating Time) x 100"""
    total = operating + downtime
    if pd.isna(total) or total == 0:
        return 0.0
    return operating / total * 100


def build_maintenance_table(df):
    df = add_condition_columns(df)

    summary = df.groupby(COL_ID, as_index=False).agg(
        **{
            COL_TYPE: (COL_TYPE, "last"),
            COL_OP: (COL_OP, "sum"),
            COL_DOWN: (COL_DOWN, "sum"),
            COL_MAINT: (COL_MAINT, "last"),
            "Alert count": ("Alert count", "sum"),
        }
    )
    summary["Availability (%)"] = summary.apply(
        lambda r: round(calculate_availability(r[COL_OP], r[COL_DOWN]), 1), axis=1)
    summary["Downtime (%)"] = (100 - summary["Availability (%)"]).round(1)

    status = summary[COL_MAINT].astype(str).str.lower()
    summary["Under maintenance"] = status.str.contains("under|in progress|ongoing")
    summary["Overdue"] = status.str.contains("overdue")
    summary["Due for maintenance"] = status.str.contains("due") & ~summary["Overdue"]
    summary["Excessive downtime"] = summary["Downtime (%)"] > EXCESSIVE_DOWNTIME_PCT
    summary["Repeated alerts"] = summary["Alert count"] >= REPEATED_ALERT_COUNT
    summary["Low availability"] = summary["Availability (%)"] < LOW_AVAILABILITY
    return summary


def maintenance_page():
    st.header("Equipment Maintenance Monitoring")
    st.caption(DISCLAIMER)

    df = load_equipment()
    if df is None:
        return
    table = build_maintenance_table(df)

    st.markdown(
        "**Availability = Operating Time ÷ (Downtime + Operating Time) × 100**  \n"
        f"Low availability: below {LOW_AVAILABILITY:.0f}%  |  "
        f"Excessive downtime: above {EXCESSIVE_DOWNTIME_PCT:.0f}% of total time  |  "
        f"Repeated alerts: {REPEATED_ALERT_COUNT}+ abnormal readings")

    categories = ["Due for maintenance", "Overdue", "Under maintenance",
                  "Excessive downtime", "Repeated alerts", "Low availability"]

    cols = st.columns(len(categories))
    for col, cat in zip(cols, categories):
        col.metric(cat, int(table[cat].sum()))

    if table["Overdue"].any():
        st.error("CRITICAL: Overdue equipment identified. Maintenance required immediately.")
    if table["Low availability"].any():
        st.warning("WARNING: Equipment with low availability identified.")

    tabs = st.tabs(categories)
    show_cols = [COL_ID, COL_TYPE, COL_OP, COL_DOWN, "Availability (%)", COL_MAINT, "Alert count"]
    for tab, cat in zip(tabs, categories):
        with tab:
            subset = table[table[cat]]
            if subset.empty:
                st.success(f"No equipment in category: {cat}")
            else:
                st.dataframe(subset[show_cols], use_container_width=True)

    st.subheader("Availability by equipment")
    st.bar_chart(table.set_index(COL_ID)["Availability (%)"])

    with st.expander("Full maintenance table"):
        st.dataframe(table, use_container_width=True)


#g) Risk Assessment#
def classify_risk(score):
    """1-4 Low, 5-9 Medium, 10-16 High, 17-25 Critical."""
    if score >= 17:
        return "Critical"
    if score >= 10:
        return "High"
    if score >= 5:
        return "Medium"
    return "Low"


def risk_matrix_table():
    """5x5 matrix of Likelihood x Consequence scores."""
    matrix = pd.DataFrame(
        [[l * c for c in range(1, 6)] for l in range(5, 0, -1)],
        index=[f"Likelihood {l}" for l in range(5, 0, -1)],
        columns=[f"Consequence {c}" for c in range(1, 6)])

    def colour(score):
        level = classify_risk(score)
        return {"Low": "background-color: #2ecc71; color: black",
                "Medium": "background-color: #ffc83d; color: black",
                "High": "background-color: #ff8c42; color: black",
                "Critical": "background-color: #ff4b4b; color: white"}[level]

    return matrix.style.map(colour)


def risk_page():
    st.header("Risk Assessment")
    st.caption("RiskScore = Likelihood × Consequence (each on a 1–5 scale)")

    description = st.text_input("Hazard / risk description")
    c1, c2 = st.columns(2)
    likelihood = c1.slider("Likelihood (1 = rare, 5 = almost certain)", 1, 5, 3)
    consequence = c2.slider("Consequence (1 = minor, 5 = catastrophic)", 1, 5, 3)

    score = likelihood * consequence
    level = classify_risk(score)

    m1, m2 = st.columns(2)
    m1.metric("Risk score", score)
    m2.metric("Classification", level)

    if level == "Critical":
        st.error("CRITICAL RISK: Immediate action required. Stop the activity and escalate to management.")
    elif level == "High":
        st.error("HIGH RISK: Urgent control measures are required before work continues.")
    elif level == "Medium":
        st.warning("Medium risk: Apply controls and monitor.")
    else:
        st.success("Low risk: Acceptable with routine controls.")

    if st.button("Save to risk register"):
        if not description.strip():
            st.warning("Enter a risk description before saving.")
        else:
            new_row = pd.DataFrame([{
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Description": description.strip(),
                "Likelihood": likelihood,
                "Consequence": consequence,
                "Risk score": score,
                "Classification": level,
            }])
            new_row.to_csv(RISK_FILE, mode="a", index=False,
                           header=not os.path.exists(RISK_FILE))
            st.success("Risk saved.")

    st.subheader("Risk matrix")
    st.dataframe(risk_matrix_table(), use_container_width=True)

    if os.path.exists(RISK_FILE):
        st.subheader("Risk register")
        register = pd.read_csv(RISK_FILE)
        st.dataframe(register, use_container_width=True)
        high = register[register["Classification"].isin(["High", "Critical"])]
        if not high.empty:
            st.error(f"{len(high)} high or critical risk(s) in the register.")


                  ########### D ###########
#Safety Incident Database#
INCIDENT_COLUMNS = ["Incident_ID", "Date", "Time", "Shift", "Location", "Department",
                    "Incident_Type", "Severity", "Injury_Status", "Lost_Time_Injury",
                    "Cause", "Corrective_Action", "Incident_Status"]
INCIDENT_TYPES = ["Near miss", "Fall of ground", "Vehicle collision", "Slip, trip or fall",
                  "Equipment damage", "Electrical", "Fire", "Struck by object",
                  "Environmental", "Other"]
SEVERITY_LEVELS = ["Low", "Medium", "High", "Critical"]
INJURY_OPTIONS = ["No injury", "First aid", "Medical treatment", "Lost time injury", "Fatality"]
STATUS_OPTIONS = ["Open", "Under investigation", "Closed"]


def load_incidents():
    """Read incidents.csv (returns an empty table if no incidents have been recorded yet)."""
    if not os.path.exists(INCIDENTS_FILE):
        return pd.DataFrame(columns=INCIDENT_COLUMNS)
    df = pd.read_csv(INCIDENTS_FILE)
    df.columns = [c.strip() for c in df.columns]
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df


def save_incidents(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%Y-%m-%d")
    df.to_csv(INCIDENTS_FILE, index=False)


def next_incident_id(df):
    """Creates the next ID, e.g. INC-001, INC-002 ..."""
    if df.empty:
        return "INC-001"
    numbers = pd.to_numeric(df["Incident_ID"].astype(str).str.extract(r"(\d+)")[0], errors="coerce")
    if numbers.isna().all():
        return f"INC-{len(df) + 1:03d}"
    return f"INC-{int(numbers.max()) + 1:03d}"


def colour_severity(value):
    colours = {"Low": "background-color: #2ecc71; color: black",
               "Medium": "background-color: #ffc83d; color: black",
               "High": "background-color: #ff8c42; color: black",
               "Critical": "background-color: #ff4b4b; color: white"}
    return colours.get(value, "")


def add_incident_form():
    df = load_incidents()
    with st.form("incident_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        date = c1.date_input("Date", value=datetime.now().date(), max_value=datetime.now().date())
        time = c2.time_input("Time", value=datetime.now().time().replace(second=0, microsecond=0))
        shift = c3.selectbox("Shift", ["Day", "Afternoon", "Night"])
        c4, c5, c6 = st.columns(3)
        location = c4.text_input("Location (e.g. Level 5 stope, Pit 2 ramp)")
        department = c5.text_input("Department")
        incident_type = c6.selectbox("Incident type", INCIDENT_TYPES)
        c7, c8, c9 = st.columns(3)
        severity = c7.selectbox("Severity", SEVERITY_LEVELS)
        injury = c8.selectbox("Injury status", INJURY_OPTIONS)
        lti = c9.selectbox("Lost-time injury?", ["No", "Yes"])
        cause = st.text_input("Cause")
        corrective = st.text_area("Corrective action")
        status = st.selectbox("Incident status", STATUS_OPTIONS)
        submitted = st.form_submit_button("Add incident")

    if not submitted:
        return

    #Input validation
    missing = [name for name, value in [("Location", location), ("Department", department),
                                        ("Cause", cause)] if not value.strip()]
    if missing:
        st.warning("Please fill in: " + ", ".join(missing))
        return
    if injury == "Lost time injury" and lti == "No":
        lti = "Yes"   # keep the two fields consistent

    incident_id = next_incident_id(df)
    new_row = pd.DataFrame([{
        "Incident_ID": incident_id,
        "Date": date.strftime("%Y-%m-%d"),
        "Time": time.strftime("%H:%M"),
        "Shift": shift,
        "Location": location.strip(),
        "Department": department.strip().title(),
        "Incident_Type": incident_type,
        "Severity": severity,
        "Injury_Status": injury,
        "Lost_Time_Injury": lti,
        "Cause": cause.strip(),
        "Corrective_Action": corrective.strip(),
        "Incident_Status": status,
    }])
    new_row.to_csv(INCIDENTS_FILE, mode="a", index=False,
                   header=not os.path.exists(INCIDENTS_FILE))
    st.success(f"Incident {incident_id} saved.")
    if severity == "Critical":
        st.error("CRITICAL: Critical safety incident recorded. Notify management immediately.")
    elif severity == "High":
        st.warning("WARNING: High severity incident recorded. Investigation required.")


def view_incidents():
    df = load_incidents()
    if df.empty:
        st.info("No incidents recorded yet.")
        return

    #Search
    search = st.text_input("Search incidents (ID, location, cause, department...)")

    #Filters
    f1, f2, f3, f4 = st.columns(4)
    dept = f1.multiselect("Department", sorted(df["Department"].dropna().astype(str).unique()))
    shift = f2.multiselect("Shift", sorted(df["Shift"].dropna().astype(str).unique()))
    severity = f3.multiselect("Severity", SEVERITY_LEVELS)
    status = f4.multiselect("Status", sorted(df["Incident_Status"].dropna().astype(str).unique()))
    inc_type = st.multiselect("Incident type", sorted(df["Incident_Type"].dropna().astype(str).unique()))

    filtered = df.copy()
    if search.strip():
        mask = filtered.astype(str).apply(
            lambda col: col.str.contains(search.strip(), case=False, regex=False)).any(axis=1)
        filtered = filtered[mask]
    for column, chosen in [("Department", dept), ("Shift", shift), ("Severity", severity),
                           ("Incident_Status", status), ("Incident_Type", inc_type)]:
        if chosen:
            filtered = filtered[filtered[column].astype(str).isin(chosen)]

    st.write(f"**{len(filtered)}** of {len(df)} incidents shown")
    display = filtered.copy()
    display["Date"] = display["Date"].dt.strftime("%Y-%m-%d")
    st.dataframe(display.style.map(colour_severity, subset=["Severity"]),
                 use_container_width=True, hide_index=True)

    #Update the status of an incident (e.g. close it after the investigation)
    with st.expander("Update incident status"):
        u1, u2 = st.columns(2)
        chosen_id = u1.selectbox("Incident ID", df["Incident_ID"].astype(str).tolist())
        new_status = u2.selectbox("New status", STATUS_OPTIONS)
        if st.button("Update status"):
            df.loc[df["Incident_ID"].astype(str) == chosen_id, "Incident_Status"] = new_status
            save_incidents(df)
            st.success(f"{chosen_id} updated to '{new_status}'.")
            st.rerun()


def incident_analysis():
    df = load_incidents()
    if df.empty:
        st.info("No incidents recorded yet.")
        return

    open_mask = df["Incident_Status"].astype(str).str.lower() != "closed"
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total incidents", len(df))
    c2.metric("Open incidents", int(open_mask.sum()))
    c3.metric("High / Critical", int(df["Severity"].isin(["High", "Critical"]).sum()))
    c4.metric("Lost-time injuries", int((df["Lost_Time_Injury"].astype(str).str.lower() == "yes").sum()))

    #Categorise and count incidents
    st.subheader("Categorise incidents")
    group_by = st.selectbox("Count incidents by",
                            ["Department", "Shift", "Incident_Type", "Severity", "Cause", "Incident_Status"])
    counts = df[group_by].value_counts()
    a1, a2 = st.columns([2, 1])
    a1.bar_chart(counts)
    a2.dataframe(counts.rename("Number of incidents"), use_container_width=True)

    #Trends
    st.subheader("Incident trend by month")
    dated = df.dropna(subset=["Date"])
    if not dated.empty:
        trend = dated.groupby(dated["Date"].dt.to_period("M")).size()
        trend.index = trend.index.astype(str)
        st.line_chart(trend.rename("Incidents"))

    st.subheader("Severity by shift")
    st.dataframe(pd.crosstab(df["Shift"], df["Severity"]), use_container_width=True)


def incidents_page():
    st.header("Safety Incident Database")
    tab1, tab2, tab3 = st.tabs(["Add incident", "View, search & filter", "Analysis & trends"])
    with tab1:
        add_incident_form()
    with tab2:
        view_incidents()
    with tab3:
        incident_analysis()


                  ########### E ###########
#h) Alerts and Notifications#
PPE_TARGET = 90.0   # % - below this = low PPE compliance (prototype value)

#Which page a user needs access to before they can see an alert from that source
ALERT_SOURCE_PERMISSION = {"Equipment": "equipment", "Maintenance": "maintenance",
                           "Workers": "worker safety", "Incidents": "safety incidents",
                           "Risk register": "risk assessment"}


def load_workers():
    """Read workers.csv and keep the latest record for each worker."""
    if not os.path.exists(WORKERS_FILE):
        return pd.DataFrame()
    df = pd.read_csv(WORKERS_FILE)
    df.columns = [c.strip() for c in df.columns]
    for col in ["Fatigue_Level_1_to_5", "Near_Misses", "Previous_Incidents"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df.groupby("Worker_ID", as_index=False).tail(1)


def load_risks():
    if not os.path.exists(RISK_FILE):
        return pd.DataFrame()
    return pd.read_csv(RISK_FILE)


def ppe_compliance(workers):
    """Percentage of workers that are PPE compliant."""
    if workers.empty:
        return None
    compliant = workers["PPE_Compliant"].astype(str).str.strip().str.lower() == "yes"
    return round(compliant.mean() * 100, 1)


def make_alert(level, source, label, item, parameter, value, status, action):
    return {"Level": level, "Source": source, "Label": label, "Item": item,
            "Parameter": parameter, "Value": value, "Status": status, "Recommended action": action}


def equipment_alerts():
    alerts = []
    if not os.path.exists(EQUIPMENT_FILE):
        return alerts
    df = add_condition_columns(load_equipment())
    latest = df.groupby(COL_ID).tail(1)    # latest reading of each machine

    inspect = "Inspect equipment and initiate appropriate maintenance/safety procedures."
    for _, row in latest.iterrows():
        eq = str(row[COL_ID])
        t = row["Temperature status"]
        v = row["Vibration status"]
        if t == "Critical":
            alerts.append(make_alert("CRITICAL", "Equipment", "Equipment ID", eq, "Temperature",
                                     f"{row[COL_TEMP]} °C", "Above Critical Threshold", inspect))
        elif t == "Warning":
            alerts.append(make_alert("WARNING", "Equipment", "Equipment ID", eq, "Temperature",
                                     f"{row[COL_TEMP]} °C", "Approaching Threshold",
                                     "Monitor temperature and schedule an inspection."))
        if v == "Critical":
            alerts.append(make_alert("CRITICAL", "Equipment", "Equipment ID", eq, "Vibration",
                                     f"{row[COL_VIB]} mm/s", "Above Critical Threshold", inspect))
        elif v == "Warning":
            alerts.append(make_alert("WARNING", "Equipment", "Equipment ID", eq, "Vibration",
                                     f"{row[COL_VIB]} mm/s", "Approaching Threshold",
                                     "Monitor vibration and schedule an inspection."))
        for label, col in [("Brake", COL_BRAKE), ("Tyre", COL_TYRE), ("Engine", COL_ENGINE)]:
            if status_is_bad(row[col]):
                alerts.append(make_alert("WARNING", "Equipment", "Equipment ID", eq, f"{label} status",
                                         str(row[col]), "Abnormal",
                                         f"Check the {label.lower()} before the next shift."))

    table = build_maintenance_table(load_equipment())
    for _, row in table.iterrows():
        eq = str(row[COL_ID])
        if row["Overdue"]:
            alerts.append(make_alert("CRITICAL", "Maintenance", "Equipment ID", eq, "Maintenance",
                                     str(row[COL_MAINT]), "Overdue Maintenance",
                                     "Withdraw from service and carry out maintenance immediately."))
        if row["Excessive downtime"]:
            alerts.append(make_alert("WARNING", "Maintenance", "Equipment ID", eq, "Downtime",
                                     f"{row['Downtime (%)']} % of total time", "Excessive Downtime",
                                     "Investigate the causes of breakdowns."))
        if row["Low availability"]:
            alerts.append(make_alert("WARNING", "Maintenance", "Equipment ID", eq, "Availability",
                                     f"{row['Availability (%)']} %", "Low Availability",
                                     "Review the maintenance plan for this machine."))
    return alerts


def worker_alerts():
    alerts = []
    workers = load_workers()
    if workers.empty:
        return alerts
    for _, row in workers.iterrows():
        wid = str(row["Worker_ID"])
        if str(row["PPE_Compliant"]).strip().lower() == "no":
            alerts.append(make_alert("WARNING", "Workers", "Worker ID", wid, "PPE compliance",
                                     "Not compliant", "PPE Requirement Not Met",
                                     "Issue correct PPE before the worker enters the workplace."))
        if row["Fatigue_Level_1_to_5"] >= 4:
            level = "CRITICAL" if row["Fatigue_Level_1_to_5"] >= 5 else "WARNING"
            alerts.append(make_alert(level, "Workers", "Worker ID", wid, "Fatigue level",
                                     f"{int(row['Fatigue_Level_1_to_5'])} / 5", "High Fatigue",
                                     "Remove from high-risk tasks and allow rest."))
        if str(row["Risk_Level"]).strip().lower() == "high":
            obs = str(row.get("Safety_Observations", ""))
            alerts.append(make_alert("WARNING", "Workers", "Worker ID", wid, "Safety observation",
                                     obs if obs and obs != "nan" else "-", "High-Risk Observation",
                                     "Supervisor to review the worker's conditions before the shift."))

    compliance = ppe_compliance(workers)
    if compliance is not None and compliance < PPE_TARGET:
        alerts.append(make_alert("WARNING", "Workers", "Area", "All workers", "PPE compliance",
                                 f"{compliance} %", f"Below {PPE_TARGET:.0f} % target",
                                 "Run a PPE awareness campaign and spot checks."))
    return alerts


def incident_alerts():
    alerts = []
    df = load_incidents()
    if df.empty:
        return alerts
    open_inc = df[df["Incident_Status"].astype(str).str.lower() != "closed"]
    for _, row in open_inc.iterrows():
        if row["Severity"] in ["Critical", "High"]:
            level = "CRITICAL" if row["Severity"] == "Critical" else "WARNING"
            alerts.append(make_alert(level, "Incidents", "Incident ID", str(row["Incident_ID"]),
                                     row["Incident_Type"], f"{row['Location']} ({row['Department']})",
                                     f"{row['Severity']} incident - {row['Incident_Status']}",
                                     "Investigate, apply corrective action and close out."))
    return alerts


def risk_alerts():
    alerts = []
    df = load_risks()
    if df.empty:
        return alerts
    for _, row in df[df["Classification"].isin(["High", "Critical"])].iterrows():
        level = "CRITICAL" if row["Classification"] == "Critical" else "WARNING"
        alerts.append(make_alert(level, "Risk register", "Hazard", str(row["Description"]),
                                 "Risk score", str(row["Risk score"]), f"{row['Classification']} Risk",
                                 "Apply control measures before work continues."))
    return alerts


def collect_alerts(role):
    """All alerts the logged-in role is allowed to see, CRITICAL first."""
    alerts = equipment_alerts() + worker_alerts() + incident_alerts() + risk_alerts()
    df = pd.DataFrame(alerts, columns=["Level", "Source", "Label", "Item", "Parameter",
                                       "Value", "Status", "Recommended action"])
    allowed = [s for s, p in ALERT_SOURCE_PERMISSION.items() if p in permissions[role]]
    df = df[df["Source"].isin(allowed)]
    df["Order"] = df["Level"].map({"CRITICAL": 0, "WARNING": 1})
    return df.sort_values("Order").drop(columns="Order").reset_index(drop=True)


def format_alert(alert):
    """Alert text in the same layout as Figure 1 of the brief."""
    line = "=" * 53
    return (f"{line}\nMINING MONITORING ALERT\n{line}\n"
            f"[{alert['Level']}]\n"
            f"{alert['Label']}: {alert['Item']}\n"
            f"Parameter: {alert['Parameter']}\n"
            f"Value: {alert['Value']}\n"
            f"Status: {alert['Status']}\n"
            f"Recommended Action:\n {alert['Recommended action']}\n"
            f"{line}")


def alerts_section(alerts):
    st.subheader("Alerts and notifications")
    if alerts.empty:
        st.success("NORMAL: No active alerts.")
        return

    critical = alerts[alerts["Level"] == "CRITICAL"]
    warnings = alerts[alerts["Level"] == "WARNING"]
    if not critical.empty:
        st.error(f"{len(critical)} CRITICAL alert(s) require immediate action.")
    if not warnings.empty:
        st.warning(f"{len(warnings)} WARNING alert(s) to follow up.")

    f1, f2 = st.columns(2)
    levels = f1.multiselect("Alert level", ["CRITICAL", "WARNING"], default=["CRITICAL", "WARNING"])
    sources = f2.multiselect("Source", sorted(alerts["Source"].unique()),
                             default=sorted(alerts["Source"].unique()))
    shown = alerts[alerts["Level"].isin(levels) & alerts["Source"].isin(sources)]
    st.dataframe(shown.drop(columns="Label").style.map(
        lambda v: colour_severity("Critical" if v == "CRITICAL" else "Medium"), subset=["Level"]),
        use_container_width=True, hide_index=True)

    with st.expander("Critical alert notices"):
        if critical.empty:
            st.write("No critical alerts.")
        for _, alert in critical.iterrows():
            st.code(format_alert(alert), language=None)


                  ########### F ###########
#i) Mining Monitoring Dashboard#
def calculate_kpis(alerts):
    """Key performance indicators used on the dashboard and in the reports."""
    workers = load_workers()
    incidents = load_incidents()
    k = {}

    #Health and safety
    k["Total workers"] = int(workers["Worker_ID"].nunique()) if not workers.empty else 0
    k["Total safety incidents"] = len(incidents)
    worker_nm = int(workers["Near_Misses"].sum()) if not workers.empty else 0
    incident_nm = int((incidents["Incident_Type"] == "Near miss").sum()) if not incidents.empty else 0
    k["Near misses"] = worker_nm + incident_nm
    k["High-risk observations"] = (int((workers["Risk_Level"].astype(str) == "High").sum())
                                   if not workers.empty else 0)
    k["PPE compliance (%)"] = ppe_compliance(workers)
    k["Open incidents"] = (int((incidents["Incident_Status"].astype(str).str.lower() != "closed").sum())
                           if not incidents.empty else 0)
    k["Lost-time injuries"] = (int((incidents["Lost_Time_Injury"].astype(str).str.lower() == "yes").sum())
                               if not incidents.empty else 0)

    #Equipment
    k["Total equipment"] = 0
    k["Equipment available"] = 0
    k["Under maintenance"] = 0
    k["Average availability (%)"] = None
    k["Operating normally (%)"] = None
    if os.path.exists(EQUIPMENT_FILE):
        eq = load_equipment()
        table = build_maintenance_table(eq)
        latest = add_condition_columns(eq).groupby(COL_ID).tail(1)
        k["Total equipment"] = len(table)
        k["Under maintenance"] = int(table["Under maintenance"].sum())
        k["Equipment available"] = k["Total equipment"] - k["Under maintenance"]
        k["Average availability (%)"] = round(table["Availability (%)"].mean(), 1)
        k["Operating normally (%)"] = round((latest["Overall condition"] == "Normal").mean() * 100, 1)

    eq_alerts = alerts[alerts["Source"].isin(["Equipment", "Maintenance"])]
    k["Equipment alerts"] = len(eq_alerts)
    k["Critical equipment alerts"] = int((eq_alerts["Level"] == "CRITICAL").sum())
    k["Active critical alerts"] = int((alerts["Level"] == "CRITICAL").sum())
    return k


def show_value(value, suffix=""):
    return "No data" if value is None else f"{value}{suffix}"


def dashboard_page(role):
    st.header("Mining Monitoring Dashboard")
    st.caption(f"Khwezi Mining  |  Last updated {datetime.now():%Y-%m-%d %H:%M}")

    alerts = collect_alerts(role)
    k = calculate_kpis(alerts)
    can_see_safety = "worker safety" in permissions[role]
    can_see_equipment = "equipment" in permissions[role]

    if can_see_safety:
        st.subheader("Health and safety")
        a = st.columns(5)
        a[0].metric("Total workers", k["Total workers"])
        a[1].metric("Total safety incidents", k["Total safety incidents"])
        a[2].metric("Near misses", k["Near misses"])
        a[3].metric("High-risk observations", k["High-risk observations"])
        a[4].metric("PPE compliance", show_value(k["PPE compliance (%)"], " %"))

    if can_see_equipment:
        st.subheader("Equipment")
        b = st.columns(6)
        b[0].metric("Total equipment", k["Total equipment"])
        b[1].metric("Equipment available", k["Equipment available"])
        b[2].metric("Under maintenance", k["Under maintenance"])
        b[3].metric("Equipment alerts", k["Equipment alerts"])
        b[4].metric("Avg availability", show_value(k["Average availability (%)"], " %"))
        b[5].metric("Critical equipment alerts", k["Critical equipment alerts"])

    #Charts
    g1, g2 = st.columns(2)
    if can_see_safety:
        incidents = load_incidents()
        with g1:
            st.markdown("**Incidents by severity**")
            if incidents.empty:
                st.info("No incidents recorded yet.")
            else:
                st.bar_chart(incidents["Severity"].value_counts().reindex(SEVERITY_LEVELS, fill_value=0))
    if can_see_equipment and os.path.exists(EQUIPMENT_FILE):
        latest = add_condition_columns(load_equipment()).groupby(COL_ID).tail(1)
        with g2:
            st.markdown("**Equipment condition (latest readings)**")
            st.bar_chart(latest["Overall condition"].value_counts()
                         .reindex(["Normal", "Warning", "Critical"], fill_value=0))

    alerts_section(alerts)


                  ########### G ###########
#Reports and j) Interactive Data Analysis#
SAFETY_QUESTIONS = [
    "How many safety incidents occurred during the selected period?",
    "Which department has the highest number of incidents?",
    "Which shift records the most incidents?",
    "What percentage of workers comply with PPE requirements?",
    "How many near misses have been recorded?",
    "Which incident types occur most frequently?",
    "How many incidents are classified as high or critical?",
    "Which departments have the highest safety risk?",
    "Is there an observable difference in incidents between day and night shifts?",
    "What are the most common causes of safety incidents?",
    "Which safety conditions require immediate attention?",
]
EQUIPMENT_QUESTIONS = [
    "Which equipment has the highest downtime?",
    "Which equipment has the lowest availability?",
    "Which equipment has the highest vibration?",
    "Which equipment has the highest operating temperature?",
    "Which equipment has generated the most alerts?",
    "Which equipment requires maintenance?",
    "Which equipment is overdue for maintenance?",
    "What is the average equipment availability?",
    "Which equipment type has the highest downtime?",
    "Which equipment requires immediate inspection?",
    "What percentage of monitored equipment is operating normally?",
]
INTEGRATED_QUESTIONS = [
    "How many critical alerts are currently active?",
    "Which equipment should receive maintenance priority?",
    "Which safety indicators require management intervention?",
    "Which areas of the operation require the greatest attention?",
    "What recommendations can be generated from the monitoring results?",
]


def show_top(counts, sentence):
    """Print the top item of a count/ranking and draw a bar chart of all items."""
    if counts.empty:
        st.info("No data available to answer this question.")
        return
    st.success(sentence.format(item=counts.index[0], value=counts.iloc[0]))
    st.bar_chart(counts)


def safety_answers(q, alerts):
    incidents = load_incidents()
    workers = load_workers()
    needs_incidents = q not in [SAFETY_QUESTIONS[3], SAFETY_QUESTIONS[4], SAFETY_QUESTIONS[10]]
    if needs_incidents and incidents.empty:
        st.info("No incidents recorded yet. Add incidents on the 'safety incidents' page.")
        return

    if q == SAFETY_QUESTIONS[0]:
        dates = incidents["Date"].dropna()
        if dates.empty:
            st.info("No incident dates recorded.")
            return
        period = st.date_input("Select period", value=(dates.min().date(), dates.max().date()))
        if len(period) != 2:
            st.info("Select a start and an end date.")
            return
        mask = (incidents["Date"].dt.date >= period[0]) & (incidents["Date"].dt.date <= period[1])
        selected = incidents[mask]
        st.success(f"{len(selected)} safety incident(s) occurred between {period[0]} and {period[1]}.")
        if not selected.empty:
            st.bar_chart(selected.groupby(selected["Date"].dt.strftime("%Y-%m")).size().rename("Incidents"))

    elif q == SAFETY_QUESTIONS[1]:
        show_top(incidents["Department"].value_counts(),
                 "{item} has the highest number of incidents ({value}).")

    elif q == SAFETY_QUESTIONS[2]:
        show_top(incidents["Shift"].value_counts(), "The {item} shift records the most incidents ({value}).")

    elif q == SAFETY_QUESTIONS[3]:
        compliance = ppe_compliance(workers)
        if compliance is None:
            st.info("No worker records yet.")
            return
        st.success(f"{compliance} % of workers comply with PPE requirements (target {PPE_TARGET:.0f} %).")
        st.bar_chart(workers["PPE_Compliant"].value_counts())
        non = workers[workers["PPE_Compliant"].astype(str).str.lower() == "no"]
        if not non.empty:
            st.write("Workers not compliant:")
            st.dataframe(non[["Worker_ID", "Department", "Job_Role", "Shift"]], hide_index=True)

    elif q == SAFETY_QUESTIONS[4]:
        worker_nm = int(workers["Near_Misses"].sum()) if not workers.empty else 0
        incident_nm = int((incidents["Incident_Type"] == "Near miss").sum()) if not incidents.empty else 0
        st.success(f"{worker_nm + incident_nm} near misses recorded "
                   f"({worker_nm} from worker records and {incident_nm} from the incident database).")

    elif q == SAFETY_QUESTIONS[5]:
        show_top(incidents["Incident_Type"].value_counts(),
                 "'{item}' is the most frequent incident type ({value}).")

    elif q == SAFETY_QUESTIONS[6]:
        high = incidents[incidents["Severity"].isin(["High", "Critical"])]
        st.success(f"{len(high)} incident(s) are classified as high or critical "
                   f"({(high['Severity'] == 'Critical').sum()} critical).")
        display = high.copy()
        display["Date"] = display["Date"].dt.strftime("%Y-%m-%d")
        st.dataframe(display, hide_index=True, use_container_width=True)

    elif q == SAFETY_QUESTIONS[7]:
        #Risk points: Low = 1, Medium = 2, High = 3, Critical = 4 per incident,
        #plus 3 points for each high-risk worker in the department
        points = incidents["Severity"].map({"Low": 1, "Medium": 2, "High": 3, "Critical": 4}).fillna(0)
        score = points.groupby(incidents["Department"]).sum()
        if not workers.empty:
            high_workers = workers[workers["Risk_Level"].astype(str) == "High"].groupby("Department").size() * 3
            score = score.add(high_workers, fill_value=0)
        st.caption("Safety risk score = severity points of incidents (Low 1 … Critical 4) "
                   "+ 3 points per high-risk worker.")
        show_top(score.sort_values(ascending=False),
                 "{item} has the highest safety risk (score {value:.0f}).")

    elif q == SAFETY_QUESTIONS[8]:
        counts = incidents["Shift"].value_counts()
        day = int(counts.get("Day", 0))
        night = int(counts.get("Night", 0))
        if day == night:
            st.success(f"No difference: {day} incidents on day shift and {night} on night shift.")
        else:
            more = "day" if day > night else "night"
            st.success(f"Yes: {day} incidents on day shift vs {night} on night shift. "
                       f"More incidents happen on the {more} shift.")
        st.dataframe(pd.crosstab(incidents["Shift"], incidents["Severity"]), use_container_width=True)

    elif q == SAFETY_QUESTIONS[9]:
        show_top(incidents["Cause"].value_counts(),
                 "The most common cause of incidents is '{item}' ({value}).")

    elif q == SAFETY_QUESTIONS[10]:
        urgent = alerts[alerts["Source"].isin(["Workers", "Incidents", "Risk register"])]
        if urgent.empty:
            st.success("No safety conditions require immediate attention.")
        else:
            st.error(f"{len(urgent)} safety condition(s) require attention "
                     f"({(urgent['Level'] == 'CRITICAL').sum()} critical).")
            st.dataframe(urgent.drop(columns="Label"), hide_index=True, use_container_width=True)


def equipment_answers(q, alerts):
    if not os.path.exists(EQUIPMENT_FILE):
        st.info(f"{EQUIPMENT_FILE} not found.")
        return
    eq = add_condition_columns(load_equipment())
    table = build_maintenance_table(load_equipment()).set_index(COL_ID)
    latest = eq.groupby(COL_ID).tail(1).set_index(COL_ID)

    if q == EQUIPMENT_QUESTIONS[0]:
        show_top(table[COL_DOWN].sort_values(ascending=False),
                 "{item} has the highest downtime ({value} hours).")

    elif q == EQUIPMENT_QUESTIONS[1]:
        show_top(table["Availability (%)"].sort_values(),
                 "{item} has the lowest availability ({value} %).")

    elif q == EQUIPMENT_QUESTIONS[2]:
        show_top(eq.groupby(COL_ID)[COL_VIB].max().sort_values(ascending=False),
                 "{item} has the highest vibration ({value} mm/s).")

    elif q == EQUIPMENT_QUESTIONS[3]:
        show_top(eq.groupby(COL_ID)[COL_TEMP].max().sort_values(ascending=False),
                 "{item} has the highest operating temperature ({value} °C).")

    elif q == EQUIPMENT_QUESTIONS[4]:
        show_top(table["Alert count"].sort_values(ascending=False),
                 "{item} has generated the most alerts ({value}).")

    elif q == EQUIPMENT_QUESTIONS[5]:
        needs = table[table["Due for maintenance"] | table["Overdue"] | table["Excessive downtime"]
                      | table["Repeated alerts"] | table["Low availability"]]
        st.success(f"{len(needs)} piece(s) of equipment require maintenance.")
        st.dataframe(needs[[COL_TYPE, COL_MAINT, "Availability (%)", "Alert count"]],
                     use_container_width=True)

    elif q == EQUIPMENT_QUESTIONS[6]:
        overdue = table[table["Overdue"]]
        if overdue.empty:
            st.success("No equipment is overdue for maintenance.")
        else:
            st.error(f"{len(overdue)} piece(s) of equipment are overdue: {', '.join(overdue.index.astype(str))}.")
            st.dataframe(overdue[[COL_TYPE, COL_MAINT, "Availability (%)"]], use_container_width=True)

    elif q == EQUIPMENT_QUESTIONS[7]:
        st.success(f"Average equipment availability is {table['Availability (%)'].mean():.1f} %.")
        st.write("Average availability by equipment type:")
        st.bar_chart(table.groupby(COL_TYPE)["Availability (%)"].mean().round(1))

    elif q == EQUIPMENT_QUESTIONS[8]:
        show_top(table.groupby(COL_TYPE)[COL_DOWN].sum().sort_values(ascending=False),
                 "{item} equipment has the highest total downtime ({value} hours).")

    elif q == EQUIPMENT_QUESTIONS[9]:
        critical = latest[latest["Overall condition"] == "Critical"]
        if critical.empty:
            st.success("No equipment requires immediate inspection.")
        else:
            st.error(f"Immediate inspection required: {', '.join(critical.index.astype(str))}.")
            st.dataframe(critical[[COL_TYPE, COL_TEMP, COL_VIB, "Overall condition"]],
                         use_container_width=True)

    elif q == EQUIPMENT_QUESTIONS[10]:
        normal = (latest["Overall condition"] == "Normal").mean() * 100
        st.success(f"{normal:.1f} % of monitored equipment is operating normally.")
        st.bar_chart(latest["Overall condition"].value_counts())


def priority_table():
    """Maintenance priority score for each piece of equipment."""
    table = build_maintenance_table(load_equipment()).set_index(COL_ID)
    latest = add_condition_columns(load_equipment()).groupby(COL_ID).tail(1).set_index(COL_ID)
    table["Critical condition"] = latest["Overall condition"] == "Critical"
    table["Priority score"] = (table["Overdue"] * 5 + table["Critical condition"] * 4
                               + table["Low availability"] * 3 + table["Excessive downtime"] * 2
                               + table["Due for maintenance"] * 2 + table["Alert count"])
    return table.sort_values("Priority score", ascending=False)


def recommendations(k, alerts):
    """Simple rule-based recommendations from the monitoring results."""
    recs = []
    if k["PPE compliance (%)"] is not None and k["PPE compliance (%)"] < PPE_TARGET:
        recs.append(f"PPE compliance is {k['PPE compliance (%)']} %: run PPE spot checks and toolbox talks.")
    if k["High-risk observations"] > 0:
        recs.append(f"{k['High-risk observations']} high-risk worker observation(s): supervisors to follow up.")
    if k["Open incidents"] > 0:
        recs.append(f"{k['Open incidents']} incident(s) still open: complete investigations and close out.")
    if k["Lost-time injuries"] > 0:
        recs.append(f"{k['Lost-time injuries']} lost-time injury(ies): review root causes with management.")
    if k["Average availability (%)"] is not None and k["Average availability (%)"] < LOW_AVAILABILITY:
        recs.append(f"Average availability is {k['Average availability (%)']} %: review the maintenance strategy.")
    overdue = alerts[(alerts["Source"] == "Maintenance") & (alerts["Status"] == "Overdue Maintenance")]
    if not overdue.empty:
        recs.append(f"Overdue maintenance on {', '.join(overdue['Item'])}: schedule immediately.")
    eq_critical = alerts[(alerts["Source"] == "Equipment") & (alerts["Level"] == "CRITICAL")]
    if not eq_critical.empty:
        recs.append(f"Inspect {', '.join(eq_critical['Item'].unique())} before the next shift "
                    "(critical temperature/vibration).")
    if not recs:
        recs.append("All indicators are within the defined limits. Continue routine monitoring.")
    return recs


def integrated_answers(q, role, alerts):
    k = calculate_kpis(alerts)

    if q == INTEGRATED_QUESTIONS[0]:
        critical = alerts[alerts["Level"] == "CRITICAL"]
        st.success(f"{len(critical)} critical alert(s) are currently active.")
        for _, alert in critical.iterrows():
            st.code(format_alert(alert), language=None)

    elif q == INTEGRATED_QUESTIONS[1]:
        if not os.path.exists(EQUIPMENT_FILE):
            st.info(f"{EQUIPMENT_FILE} not found.")
            return
        table = priority_table()
        st.caption("Priority score = Overdue×5 + Critical condition×4 + Low availability×3 "
                   "+ Excessive downtime×2 + Due×2 + number of alerts")
        st.success(f"{table.index[0]} should receive maintenance priority (score {table['Priority score'].iloc[0]}).")
        st.dataframe(table[[COL_TYPE, "Priority score", COL_MAINT, "Availability (%)", "Alert count"]],
                     use_container_width=True)

    elif q == INTEGRATED_QUESTIONS[2]:
        rows = [
            ("PPE compliance (%)", k["PPE compliance (%)"], f">= {PPE_TARGET:.0f}",
             k["PPE compliance (%)"] is not None and k["PPE compliance (%)"] < PPE_TARGET),
            ("High-risk observations", k["High-risk observations"], "0", k["High-risk observations"] > 0),
            ("Open incidents", k["Open incidents"], "0", k["Open incidents"] > 0),
            ("Lost-time injuries", k["Lost-time injuries"], "0", k["Lost-time injuries"] > 0),
            ("Active critical alerts", k["Active critical alerts"], "0", k["Active critical alerts"] > 0),
        ]
        indicators = pd.DataFrame(rows, columns=["Indicator", "Current value", "Target", "Intervention needed"])
        needed = indicators[indicators["Intervention needed"]]
        if needed.empty:
            st.success("No safety indicators require management intervention.")
        else:
            st.error("Management intervention required for: " + ", ".join(needed["Indicator"]) + ".")
        st.dataframe(indicators, hide_index=True, use_container_width=True)

    elif q == INTEGRATED_QUESTIONS[3]:
        if alerts.empty:
            st.success("No active alerts. No area requires special attention.")
            return
        counts = alerts.groupby("Source").size().sort_values(ascending=False)
        show_top(counts, "{item} requires the greatest attention ({value} active alerts).")
        st.write("Items with the most alerts:")
        st.dataframe(alerts.groupby(["Source", "Item"]).size().sort_values(ascending=False)
                     .rename("Alerts").head(10), use_container_width=True)

    elif q == INTEGRATED_QUESTIONS[4]:
        for i, rec in enumerate(recommendations(k, alerts), start=1):
            st.write(f"{i}. {rec}")


def build_report_text(role, k, alerts):
    """Plain-text summary report that can be downloaded."""
    line = "=" * 53
    lines = [line, "KHWEZI MINING - MONITORING SUMMARY REPORT", line,
             f"Generated: {datetime.now():%Y-%m-%d %H:%M}",
             f"Generated by: {role}", ""]
    if "worker safety" in permissions[role]:
        lines += ["HEALTH AND SAFETY",
                  f"  Total workers: {k['Total workers']}",
                  f"  Total safety incidents: {k['Total safety incidents']}",
                  f"  Open incidents: {k['Open incidents']}",
                  f"  Lost-time injuries: {k['Lost-time injuries']}",
                  f"  Near misses: {k['Near misses']}",
                  f"  High-risk observations: {k['High-risk observations']}",
                  f"  PPE compliance: {show_value(k['PPE compliance (%)'], ' %')}", ""]
    if "equipment" in permissions[role]:
        lines += ["EQUIPMENT",
                  f"  Total equipment: {k['Total equipment']}",
                  f"  Equipment available: {k['Equipment available']}",
                  f"  Under maintenance: {k['Under maintenance']}",
                  f"  Average availability: {show_value(k['Average availability (%)'], ' %')}",
                  f"  Operating normally: {show_value(k['Operating normally (%)'], ' %')}",
                  f"  Equipment alerts: {k['Equipment alerts']} "
                  f"({k['Critical equipment alerts']} critical)", ""]
    lines += [f"ACTIVE ALERTS: {len(alerts)} ({k['Active critical alerts']} critical)"]
    for _, alert in alerts[alerts["Level"] == "CRITICAL"].iterrows():
        lines += ["", format_alert(alert)]
    lines += ["", "RECOMMENDATIONS"]
    lines += [f"  {i}. {rec}" for i, rec in enumerate(recommendations(k, alerts), start=1)]
    lines += ["", DISCLAIMER]
    return "\n".join(lines)


def reports_page(role):
    st.header("Reports and Data Analysis")
    alerts = collect_alerts(role)
    tab1, tab2 = st.tabs(["Interactive data analysis", "Generate reports"])

    with tab1:
        #Only show the questions the role is allowed to answer
        categories = {}
        if "worker safety" in permissions[role]:
            categories["Health and Safety"] = SAFETY_QUESTIONS
        if "equipment" in permissions[role]:
            categories["Equipment"] = EQUIPMENT_QUESTIONS
        integrated = INTEGRATED_QUESTIONS.copy()
        if "worker safety" not in permissions[role]:
            integrated.remove(INTEGRATED_QUESTIONS[2])   # safety indicators need safety access
        categories["Integrated Safety and Equipment Analysis"] = integrated

        category = st.radio("Question category", list(categories.keys()), horizontal=True)
        question = st.selectbox("Select a question", categories[category])
        st.markdown(f"**{question}**")

        if category == "Health and Safety":
            safety_answers(question, alerts)
        elif category == "Equipment":
            equipment_answers(question, alerts)
        else:
            integrated_answers(question, role, alerts)

    with tab2:
        k = calculate_kpis(alerts)
        report = build_report_text(role, k, alerts)
        st.download_button("Download summary report (.txt)", report,
                           file_name=f"khwezi_report_{datetime.now():%Y%m%d_%H%M}.txt")
        st.text(report)

        st.subheader("Download data")
        downloads = [("Active alerts", alerts.drop(columns="Label"), "alerts.csv", "dashboard")]
        if "worker safety" in permissions[role]:
            downloads.append(("Worker records", load_workers(), "workers_report.csv", "worker safety"))
        if "safety incidents" in permissions[role]:
            downloads.append(("Safety incidents", load_incidents(), "incidents_report.csv", "safety incidents"))
        if "maintenance" in permissions[role] and os.path.exists(EQUIPMENT_FILE):
            downloads.append(("Maintenance table", build_maintenance_table(load_equipment()),
                              "maintenance_report.csv", "maintenance"))
        if "risk assessment" in permissions[role]:
            downloads.append(("Risk register", load_risks(), "risk_register_report.csv", "risk assessment"))

        cols = st.columns(len(downloads))
        for col, (name, data, filename, _) in zip(cols, downloads):
            col.download_button(name, data.to_csv(index=False), file_name=filename,
                                mime="text/csv", disabled=data.empty)


                  ########### H ###########
#Manage Users (Administrator only)#
def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def count_admins():
    return sum(1 for details in users.values() if details["role"] == "Administrator")


def manage_users_page():
    st.header("Manage Users")
    tab1, tab2, tab3 = st.tabs(["Add user", "Change role / password", "Remove user"])

    #Add a new user
    with tab1:
        with st.form("add_user_form", clear_on_submit=True):
            new_name = st.text_input("Username")
            new_role = st.selectbox("Role", list(permissions.keys()))
            new_pass = st.text_input("Password", type="password")
            confirm = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Add user")
        if submitted:
            new_name = new_name.strip()
            if not new_name:
                st.warning("Enter a username.")
            elif new_name in users:
                st.error(f"The username '{new_name}' already exists.")
            elif len(new_pass) < 6:
                st.warning("The password must have at least 6 characters.")
            elif new_pass != confirm:
                st.error("The passwords do not match.")
            else:
                users[new_name] = {"password": new_pass, "role": new_role}
                save_users()
                st.success(f"User '{new_name}' added as {new_role}.")

    #Change the role or password of a user
    with tab2:
        name = st.selectbox("Select user", list(users.keys()), key="edit_user")
        roles = list(permissions.keys())
        role_choice = st.selectbox("Role", roles, index=roles.index(users[name]["role"]),
                                   key=f"edit_role_{name}")
        pass_choice = st.text_input("New password (leave blank to keep the current one)",
                                    type="password", key="edit_pass")
        if st.button("Save changes"):
            if (users[name]["role"] == "Administrator" and role_choice != "Administrator"
                    and count_admins() == 1):
                st.error("There must be at least one Administrator.")
            elif pass_choice and len(pass_choice) < 6:
                st.warning("The password must have at least 6 characters.")
            else:
                users[name]["role"] = role_choice
                if pass_choice:
                    users[name]["password"] = pass_choice
                save_users()
                st.success(f"User '{name}' updated.")

    #Remove a user
    with tab3:
        others = [u for u in users if u != st.session_state.username]
        if not others:
            st.info("There are no other users to remove.")
        else:
            name = st.selectbox("Select user to remove", others, key="remove_user")
            sure = st.checkbox(f"Yes, remove '{name}'")
            if st.button("Remove user", type="primary"):
                if not sure:
                    st.warning("Tick the box to confirm.")
                elif users[name]["role"] == "Administrator" and count_admins() == 1:
                    st.error("There must be at least one Administrator.")
                else:
                    del users[name]
                    save_users()
                    st.success(f"User '{name}' removed.")
                    st.rerun()

    st.subheader("Current users")
    st.dataframe(pd.DataFrame([{"Username": u, "Role": d["role"]} for u, d in users.items()]),
                 hide_index=True, use_container_width=True)

    st.subheader("Role permissions")
    sections = permissions["Administrator"]
    matrix = pd.DataFrame({r: ["✓" if s in permissions[r] else "-" for s in sections] for r in permissions},
                          index=[s.title() for s in sections])
    st.dataframe(matrix, use_container_width=True)


                  ########### PAGE ROUTING ###########
if page == "dashboard":
    dashboard_page(role)
elif page == "worker safety":
    worker_page()
elif page == "safety incidents":
    incidents_page()
elif page == "equipment":
    equipment_page()
elif page == "maintenance":
    maintenance_page()
elif page == "risk assessment":
    risk_page()
elif page == "reports":
    reports_page(role)
elif page == "manage users":
    manage_users_page()

#h) Automatic alerts shown in the sidebar on every page
active = collect_alerts(role)
n_critical = int((active["Level"] == "CRITICAL").sum())
n_warning = int((active["Level"] == "WARNING").sum())
if n_critical:
    st.sidebar.error(f"🚨 {n_critical} critical alert(s) active. See the dashboard.")
if n_warning:
    st.sidebar.warning(f"⚠️ {n_warning} warning(s) active.")
if not n_critical and not n_warning:
    st.sidebar.success("No active alerts.")