import streamlit as st
from datetime import date
import base64

st.set_page_config(
    page_title="Leftover Love",
    page_icon="🍱",
    layout="wide"
)

def set_bg(image_file):
    try:
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()

        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        h1, h2, h3 {{
            color: #4b3b2a !important;
            font-family: Georgia, serif;
            font-weight: 700 !important;
        }}

        label, p, span {{
            color: #4b3b2a !important;
            font-family: Georgia, serif;
            font-weight: 600 !important;
        }}

        .stTextInput input,
        .stNumberInput input,
        .stDateInput input,
        .stTimeInput input {{
            background-color: rgba(255,255,255,0.96) !important;
            color: #4b3b2a !important;
            border-radius: 10px !important;
            border: 1px solid #d6b08c !important;
            font-weight: 600 !important;
        }}

        .stSelectbox div[data-baseweb="select"] > div {{
            background-color: rgba(255,255,255,0.96) !important;
            color: #4b3b2a !important;
            border-radius: 10px !important;
            border: 1px solid #d6b08c !important;
            font-weight: 600 !important;
        }}

        div[role="option"] {{
            background-color: #fffaf5 !important;
            color: #4b3b2a !important;
            font-weight: 600 !important;
        }}

        div[role="option"]:hover {{
            background-color: #d8a36d !important;
            color: white !important;
        }}

        .stButton > button {{
            background: linear-gradient(180deg, #b56b35, #7a3e18);
            color: white !important;
            border: none;
            border-radius: 12px;
            padding: 12px 25px;
            font-weight: bold;
            box-shadow: 0 6px 0 #3d1c08,
                        0 10px 18px rgba(0,0,0,0.25);
            transition: 0.2s;
        }}

        .stButton > button:hover {{
            background: linear-gradient(180deg, #c97b43, #8a4a1f);
            transform: scale(1.02);
        }}

        .card {{
            background: rgba(255,255,255,0.92);
            padding: 18px;
            border-radius: 16px;
            margin-bottom: 15px;
            border: 1px solid #e6c9ab;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }}

        .urgent-card {{
            background: rgba(255,245,245,0.95);
            padding: 18px;
            border-radius: 16px;
            margin-bottom: 15px;
            border: 2px solid #d9534f;
        }}

        .safe-card {{
            background: rgba(240,255,245,0.95);
            padding: 18px;
            border-radius: 16px;
            margin-bottom: 15px;
            border: 2px solid #28a745;
        }}

        .unsafe-card {{
            background: rgba(255,240,240,0.95);
            padding: 18px;
            border-radius: 16px;
            margin-bottom: 15px;
            border: 2px solid #dc3545;
        }}

        .card p, .urgent-card p, .safe-card p, .unsafe-card p,
        .card b, .urgent-card b, .safe-card b, .unsafe-card b {{
            color: #4b3b2a !important;
            font-weight: 700 !important;
            margin: 4px 0;
        }}
        </style>
        """, unsafe_allow_html=True)

    except FileNotFoundError:
        st.warning("Background image not found. Check path: notebook/background.png")


set_bg("notebook/background.png")

if "receivers" not in st.session_state:
    st.session_state.receivers = []

if "donations" not in st.session_state:
    st.session_state.donations = []

if "pickups" not in st.session_state:
    st.session_state.pickups = []

st.markdown("<h1 style='text-align:center;'>🍱 Leftover Love</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>Regional Food Redistribution and Coordination System</h3>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "Receiver Verification",
    "Donate Food",
    "Pickup Scheduling",
    "Food Safety & Expiry Check"
])

# ---------- TAB 1 ----------
with tab1:
    st.subheader("Receiver Verification")

    name = st.text_input("Name")
    rtype = st.selectbox("Type", ["NGO", "Individual"])
    contact = st.text_input("Contact")
    location = st.selectbox("Location", ["Mumbai", "Navi Mumbai", "Thane", "Pune"])
    people = st.number_input("People Needing Food", min_value=1)

    if st.button("Verify Receiver"):
        if name and contact:
            st.session_state.receivers.append({
                "name": name,
                "type": rtype,
                "contact": contact,
                "location": location,
                "people": people
            })
            st.success("Receiver verified successfully. Now this receiver will appear in Pickup Scheduling.")
        else:
            st.error("Please fill all required details")

    st.divider()
    st.subheader("Verified Receivers")

    if not st.session_state.receivers:
        st.info("No receivers verified yet")
    else:
        for r in st.session_state.receivers:
            st.markdown(f"""
            <div class='card'>
                <p><b>Name:</b> {r['name']}</p>
                <p><b>Type:</b> {r['type']}</p>
                <p><b>Location:</b> {r['location']}</p>
                <p><b>People:</b> {r['people']}</p>
                <p><b>Contact:</b> {r['contact']}</p>
            </div>
            """, unsafe_allow_html=True)

# ---------- TAB 2 ----------
with tab2:
    st.subheader("Donate Food")

    donor = st.text_input("Donor Name")
    food = st.text_input("Food Name")

    food_image = st.file_uploader(
        "Upload Food Photo",
        type=["jpg", "jpeg", "png"],
        key="food_photo_upload"
    )

    image_bytes = None
    if food_image:
        image_bytes = food_image.getvalue()
        st.image(image_bytes, width=250)

    food_type = st.selectbox(
        "Food Type",
        ["Cooked Meal", "Fruits", "Vegetables", "Bakery", "Other"]
    )

    quantity = st.number_input("Quantity / Plates", min_value=1)

    food_location = st.selectbox(
        "Pickup Location",
        ["Mumbai", "Navi Mumbai", "Thane", "Pune"]
    )

    expiry = st.date_input("Expiry Date", min_value=date.today())

    days_left = (expiry - date.today()).days

    if days_left == 0:
        freshness = "Expiring Today"
        st.error("⚠️ Immediate pickup required")
    elif days_left <= 3:
        freshness = "Expiring Soon"
        st.warning("⚠️ Food is expiring soon")
    else:
        freshness = "Fresh"
        st.success("✅ Food is fresh")

    if st.button("Submit Donation"):
        if donor and food:
            donation_id = len(st.session_state.donations) + 1

            st.session_state.donations.append({
                "id": donation_id,
                "donor": donor,
                "food": food,
                "image": image_bytes,
                "type": food_type,
                "quantity": quantity,
                "location": food_location,
                "expiry": expiry,
                "freshness": freshness,
                "status": "Available",
                "safety": "Pending"
            })

            st.success("Donation added successfully. Complete Food Safety Check before Pickup Scheduling.")
        else:
            st.error("Please fill all required details")

    st.divider()
    st.subheader("Food Donations")

    if not st.session_state.donations:
        st.info("No donations added yet")
    else:
        for d in st.session_state.donations:
            safety = d.get("safety", "Pending")

            if safety == "Safe":
                card_class = "safe-card"
            elif safety == "Unsafe":
                card_class = "unsafe-card"
            elif d["freshness"] == "Expiring Today":
                card_class = "urgent-card"
            else:
                card_class = "card"

            if d.get("image"):
                st.image(d["image"], width=220)

            st.markdown(f"""
            <div class='{card_class}'>
                <p><b>Donation ID:</b> {d.get('id', '-')}</p>
                <p><b>Donor:</b> {d['donor']}</p>
                <p><b>Food:</b> {d['food']}</p>
                <p><b>Type:</b> {d['type']}</p>
                <p><b>Quantity:</b> {d['quantity']} plates</p>
                <p><b>Location:</b> {d['location']}</p>
                <p><b>Expiry:</b> {d['expiry']}</p>
                <p><b>Freshness:</b> {d['freshness']}</p>
                <p><b>Status:</b> {d['status']}</p>
                <p><b>Safety:</b> {safety}</p>
            </div>
            """, unsafe_allow_html=True)

# ---------- TAB 3 ----------
with tab3:
    st.subheader("Pickup Scheduling")

    receiver_names = [
        f"{i+1}. {r['name']} ({r['location']})"
        for i, r in enumerate(st.session_state.receivers)
    ]

    food_names = [
        f"{d.get('id', '-')}. {d['food']} ({d['location']}) - {d.get('safety', 'Pending')}"
        for d in st.session_state.donations
        if d["status"] == "Available"
    ]

    if not receiver_names:
        st.info("Add verified receiver first.")
    elif not food_names:
        st.info("Add food donation first.")
    else:
        receiver = st.selectbox("Select Verified Receiver", receiver_names)
        selected_food = st.selectbox("Select Available Food", food_names)
        pickup_time = st.time_input("Pickup Time")
        status = st.selectbox("Status", ["Scheduled", "Picked Up", "Delivered"])

        if st.button("Schedule Pickup"):
            selected_food_id = int(selected_food.split(".")[0])
            selected_receiver_index = int(receiver.split(".")[0]) - 1
            selected_receiver = st.session_state.receivers[selected_receiver_index]

            selected_donation = None
            for d in st.session_state.donations:
                if d.get("id") == selected_food_id:
                    selected_donation = d
                    break

            if selected_donation:
                if selected_receiver["location"] != selected_donation["location"]:
                    st.error("Receiver and food location must be same.")
                elif selected_donation.get("safety", "Pending") != "Safe":
                    st.warning("Food is not SAFE yet. Go to Food Safety tab and mark it SAFE first.")
                else:
                    st.session_state.pickups.append({
                        "receiver": receiver,
                        "food": selected_food,
                        "time": pickup_time,
                        "status": status
                    })

                    selected_donation["status"] = "Reserved"
                    st.success("Pickup scheduled successfully.")

    st.divider()
    st.subheader("Pickup Summary")

    if not st.session_state.pickups:
        st.info("No pickups scheduled yet")
    else:
        for p in st.session_state.pickups:
            st.markdown(f"""
            <div class='card'>
                <p><b>Food:</b> {p['food']}</p>
                <p><b>Receiver:</b> {p['receiver']}</p>
                <p><b>Pickup Time:</b> {p['time']}</p>
                <p><b>Status:</b> {p['status']}</p>
            </div>
            """, unsafe_allow_html=True)

# ---------- TAB 4 ----------
with tab4:
    st.subheader("🛡️ Food Safety & Expiry Check")
    st.info("Only food marked SAFE can be scheduled for pickup.")

    if not st.session_state.donations:
        st.info("No donations available. Add donation first.")
    else:
        donation_options = [
            f"{d.get('id', i+1)}. {d['food']} ({d['location']}) - {d.get('safety', 'Pending')}"
            for i, d in enumerate(st.session_state.donations)
        ]

        selected = st.selectbox("Select Food Donation", donation_options)
        selected_id = int(selected.split(".")[0])

        donation = None
        selected_index = None

        for i, d in enumerate(st.session_state.donations):
            if d.get("id", i + 1) == selected_id:
                donation = d
                selected_index = i
                break

        if donation:
            current_safety = donation.get("safety", "Pending")

            if donation.get("image"):
                st.image(donation["image"], width=250)

            st.markdown(f"""
            <div class='card'>
                <p><b>Donation ID:</b> {donation.get('id', '-')}</p>
                <p><b>Food:</b> {donation['food']}</p>
                <p><b>Type:</b> {donation['type']}</p>
                <p><b>Quantity:</b> {donation['quantity']} plates</p>
                <p><b>Location:</b> {donation['location']}</p>
                <p><b>Expiry:</b> {donation['expiry']}</p>
                <p><b>Current Safety:</b> {current_safety}</p>
            </div>
            """, unsafe_allow_html=True)

            st.divider()
            st.markdown("### Safety Checklist")

            prepared = st.radio("Prepared within last 4 hours?", ["Yes", "No"], horizontal=True)
            packed = st.radio("Properly packed & hygienic?", ["Yes", "No"], horizontal=True)
            smell = st.selectbox("Smell / Quality Check", ["Good", "Average", "Bad"])
            contamination = st.radio("Visible contamination?", ["No", "Yes"], horizontal=True)
            category = st.selectbox("Food Category", ["Vegetarian", "Non-Vegetarian"])

            days = (donation["expiry"] - date.today()).days

            if days == 0:
                st.warning("⚠️ Food expires today. Immediate pickup needed.")
            elif days < 0:
                st.error("❌ Food expired.")
            else:
                st.success(f"✅ {days} day(s) left before expiry.")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("✅ Mark SAFE"):
                    if prepared == "Yes" and packed == "Yes" and smell != "Bad" and contamination == "No" and days >= 0:
                        st.session_state.donations[selected_index]["safety"] = "Safe"
                        st.success("Food marked SAFE. It can now be scheduled for pickup.")
                    else:
                        st.error("Food cannot be marked safe. Checklist failed.")

            with col2:
                if st.button("❌ Mark UNSAFE"):
                    st.session_state.donations[selected_index]["safety"] = "Unsafe"
                    st.warning("Food marked UNSAFE.")

            st.divider()
            st.subheader("Safety Summary")

            safe_count = sum(1 for d in st.session_state.donations if d.get("safety", "Pending") == "Safe")
            unsafe_count = sum(1 for d in st.session_state.donations if d.get("safety", "Pending") == "Unsafe")
            pending_count = sum(1 for d in st.session_state.donations if d.get("safety", "Pending") == "Pending")

            c1, c2, c3 = st.columns(3)
            c1.success(f"✅ Safe: {safe_count}")
            c2.error(f"❌ Unsafe: {unsafe_count}")
            c3.warning(f"⏳ Pending: {pending_count}")

st.caption("Reducing food waste • Supporting local communities")