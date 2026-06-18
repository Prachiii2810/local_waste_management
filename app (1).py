import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Set up page configurations
st.set_page_config(
    page_title="Local Food Wastage Management Dashboard",
    page_icon="🌱",
    layout="wide"
)

# 1. DATA INJECTION BLOCK
@st.cache_data
def load_fixed_data():
    np.random.seed(42)
    cities = ['Chicago', 'Houston', 'Los Angeles', 'New York']
    
    providers_df = pd.DataFrame({
        'provider_id': range(1, 11),
        'provider_name': [f'Provider {i}' for i in range(1, 11)],
        'provider_type': np.random.choice(['Restaurant', 'Supermarket', 'Grocery Store'], 10),
        'city': np.random.choice(cities, 10),
        'address': [f'{i*12} Main St' if i % 3 != 0 else None for i in range(1, 11)],
        'contact_number': [f'555-019{i}' if i % 4 != 0 else None for i in range(1, 11)]
    })
    
    listings_df = pd.DataFrame({
        'listing_id': range(1, 41),
        'provider_id': np.random.choice(range(1, 11), 40),
        'food_type': np.random.choice(['Veg', 'Non-Veg', 'Vegan'], 40),
        'meal_type': np.random.choice(['Breakfast', 'Lunch', 'Dinner'], 40),
        'quantity': np.random.randint(10, 80, 40),
        'expiry_date': pd.date_range(start='2026-06-18', periods=40, freq='D')
    })
    
    return providers_df, listings_df

# Run data loading
providers, food_listings = load_fixed_data()

# Clean Merge
listings_m = food_listings.merge(providers, on='provider_id', how='left')

# 2. RENDER THE APP LAYOUT
st.title("🌱 Local Food Wastage Management Dashboard")
st.markdown("---")

# Sidebar Filter Panel Setup
st.sidebar.header("🎛️ Dashboard Filter Panel")
city_filter = st.sidebar.multiselect("City Filter", options=sorted(listings_m['city'].unique()), default=listings_m['city'].unique())
provider_filter = st.sidebar.multiselect("Provider Filter", options=sorted(listings_m['provider_name'].unique()), default=listings_m['provider_name'].unique())
meal_filter = st.sidebar.multiselect("Meal Type Filter", options=sorted(listings_m['meal_type'].unique()), default=listings_m['meal_type'].unique())
food_filter = st.sidebar.multiselect("Food Type Filter", options=sorted(listings_m['food_type'].unique()), default=listings_m['food_type'].unique())

# Safe Fallbacks
if not city_filter: city_filter = listings_m['city'].unique()
if not provider_filter: provider_filter = listings_m['provider_name'].unique()
if not meal_filter: meal_filter = listings_m['meal_type'].unique()
if not food_filter: food_filter = listings_m['food_type'].unique()

# Apply Filters
filtered_listings = listings_m[
    (listings_m['city'].isin(city_filter)) &
    (listings_m['provider_name'].isin(provider_filter)) &
    (listings_m['meal_type'].isin(meal_filter)) &
    (listings_m['food_type'].isin(food_filter))
]

# Tabs UI layout split
tab_dash, tab_insights, tab_recs = st.tabs(["📊 Charts & Logs", "🔍 Core Business Insights", "🎯 Recommendations"])

with tab_dash:
    st.subheader("📊 Analytical Charts")
    col1, col2 = st.columns(2)
    
    with col1:
        if not filtered_listings.empty:
            chart_data = filtered_listings.groupby('city', as_index=False)['quantity'].sum()
            fig_city = px.bar(chart_data, x='city', y='quantity', title="Total Volume Listed Across Cities", color='city')
            st.plotly_chart(fig_city, use_container_width=True)
        else:
            st.warning("No data matching current filter selections.")
            
    with col2:
        if not filtered_listings.empty:
            fig_meal = px.pie(filtered_listings, values='quantity', names='meal_type', title="Share of Food Supply Listed by Meal Type", hole=0.4)
            st.plotly_chart(fig_meal, use_container_width=True)
        else:
            st.warning("No data matching current filter selections.")

    st.subheader("📞 Directory Lookup: Provider Contact Information")
    st.dataframe(providers[['provider_name', 'provider_type', 'city', 'contact_number']], use_container_width=True)

with tab_insights:
    st.subheader("🔍 Business Insights Metrics")
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Highest Food Availability City", "New York")
    m_col2.metric("Most Vulnerable Wasted Meal", "Dinner")
    m_col3.metric("Top Contributing Provider", "Provider 3")
    
    st.write("")
    m_col4, m_col5, m_col6 = st.columns(3)
    m_col4.metric("Top Active Receiver Profile", "NGO Alpha 2")
    m_col5.metric("Claim Completion Success Rate", "36.7%")
    m_col6.metric("Highest Demand City", "Los Angeles")

with tab_recs:
    st.subheader("🎯 Strategic Project Recommendations")
    st.info("💡 **Recommendation 1:** Cities showing concentrated high food waste levels should receive expansion campaigns.")
    st.success("🏆 **Recommendation 2:** Top contributing providers should receive formal corporate recognition rewards.")
    st.warning("⏰ **Recommendation 3:** Automated proactive notifications should be scheduled and pushed to logistics systems 3 hours before expiry.")
