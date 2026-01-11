import streamlit as st
from models.order_manager import OrderManager
from models.user_manager import UserManager
from visualizations import (
    plot_sales_by_state,
    plot_status_distribution,
    plot_sales_by_category,
    plot_sales_trend
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Inventory Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# GLOBAL CSS (BLUR + ANIMATIONS + MATERIAL FEEL)
# --------------------------------------------------
st.markdown(
    """
    <style>
    /* Smooth transitions */
    * {
        transition: all 0.25s ease-in-out;
    }

    /* Glassmorphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 14px;
        padding: 1.2rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }

    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.12);
    }

    /* App bar */
    .app-bar {
        background: linear-gradient(90deg, #1976D2, #EC407A);
        color: white;
        padding: 1.2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
    }

    /* Sidebar polish */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FAFAFA, #FFFFFF);
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        padding: 0.6rem 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# MANAGERS
# --------------------------------------------------
user_manager = UserManager()
order_manager = OrderManager()

user_manager.create_user("admin", "admin123", "Manager")
user_manager.create_user("junior", "junior123", "Junior Manager")

@st.cache_data
def load_orders():
    om = OrderManager()
    om.load_data("data/amazon_sale_report.csv")
    return om

order_manager = load_orders()

# --------------------------------------------------
# SESSION
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --------------------------------------------------
# LOGIN PAGE
# --------------------------------------------------
if not st.session_state.logged_in:
    st.markdown(
        """
        <div class="glass-card" style="max-width:420px; margin:auto; margin-top:6rem;">
            <h2 style="text-align:center;">📦 Inventory Analytics</h2>
            <p style="text-align:center; color:#555;">Secure Login</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if user_manager.authenticate(username, password):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# --------------------------------------------------
# APP BAR WITH LOGO
# --------------------------------------------------
st.markdown(
    """
    <div class="app-bar">
        <h2 style="margin:0;">📦 Inventory Management Dashboard</h2>
        <p style="margin-top:4px; opacity:0.9;">
            Amazon Sales Analytics • Material UI Inspired
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.markdown("## 📁 Navigation")
menu = st.sidebar.radio(
    "",
    [
        "Overview",
        "Cancelled Orders",
        "Top Products",
        "Sales by City",
        "Category Performance",
        "Visual Analytics"
    ]
)

st.sidebar.markdown("---")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------
if menu == "Overview":
    st.subheader("📊 Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="glass-card">
                <h4>📦 Total Orders</h4>
                <h2>{len(order_manager.orders)}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        cancelled = order_manager.search_by_status("cancelled")
        st.markdown(
            f"""
            <div class="glass-card">
                <h4>❌ Cancelled Orders</h4>
                <h2>{len(cancelled)}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="glass-card">
                <h4>🗂 Categories</h4>
                <h2>{len(order_manager.category_performance())}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

# --------------------------------------------------
# CANCELLED ORDERS
# --------------------------------------------------
elif menu == "Cancelled Orders":
    st.subheader("❌ Cancelled Orders")

    cancelled_orders = order_manager.search_by_status("cancelled")

    st.markdown(
        f"""
        <div class="glass-card">
            <b>Total Cancelled Orders:</b> {len(cancelled_orders)}
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("View sample orders"):
        for o in cancelled_orders[:20]:
            st.text(str(o))

# --------------------------------------------------
# TOP PRODUCTS
# --------------------------------------------------
elif menu == "Top Products":
    st.subheader("🏆 Top Products")

    for sku, amount in order_manager.top_n_by_amount(5):
        st.markdown(
            f"""
            <div class="glass-card">
                <b>SKU:</b> {sku}<br>
                <b>Sales:</b> ₹{amount}
            </div>
            """,
            unsafe_allow_html=True
        )

# --------------------------------------------------
# SALES BY CITY
# --------------------------------------------------
elif menu == "Sales by City":
    st.subheader("🏙 Sales by City")

    cities = sorted(
        set(o.ship_city for o in order_manager.orders if o.ship_city)
    )

    city = st.selectbox("Select City", cities)
    total = order_manager.sales_by_city(city)

    st.markdown(
        f"""
        <div class="glass-card">
            <h4>Total Sales in {city}</h4>
            <h2>₹{total}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# CATEGORY PERFORMANCE
# --------------------------------------------------
elif menu == "Category Performance":
    st.subheader("🗂 Category Performance")

    for cat, val in order_manager.category_performance().items():
        st.markdown(
            f"""
            <div class="glass-card">
                <b>{cat}</b><br>
                Sales: ₹{val['amount']}<br>
                Quantity: {val['qty']}
            </div>
            """,
            unsafe_allow_html=True
        )

# --------------------------------------------------
# VISUAL ANALYTICS
# --------------------------------------------------
elif menu == "Visual Analytics":
    st.subheader("📈 Visual Analytics")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Sales by State", "Order Status", "Category Sales", "Sales Trend"]
    )

    with tab1:
        plot_sales_by_state(order_manager.orders)
        st.pyplot()

    with tab2:
        plot_status_distribution(order_manager.orders)
        st.pyplot()

    with tab3:
        plot_sales_by_category(order_manager.category_performance())
        st.pyplot()

    with tab4:
        plot_sales_trend(order_manager.orders)
        st.pyplot()
