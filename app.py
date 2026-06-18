import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. App Configuration
st.set_page_config(
    page_title="AI India Tour Planner & Recommender",
    page_icon="✈️",
    layout="wide"
)

# 2. Optimized, Cached Data Pipeline
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("indian tourism.csv")
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
        
    string_cols = ['Zone', 'State', 'City', 'Type', 'Significance', 'Best Time to visit', 'DSLR Allowed', 'Airport with 50km Radius']
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].fillna('Not Specified').astype(str).str.strip()
            
    df['Entrance Fee in INR'] = pd.to_numeric(df['Entrance Fee in INR'], errors='coerce').fillna(0).astype(int)
    df['time needed to visit in hrs'] = pd.to_numeric(df['time needed to visit in hrs'], errors='coerce').fillna(1.0)
    df['Google review rating'] = pd.to_numeric(df['Google review rating'], errors='coerce').fillna(4.0)
    
    # Generate spatial text soup for similarity metrics
    df['combined_features'] = df['Type'] + " " + df['Significance'] + " " + df['Zone'] + " " + df['State'] + " " + df['Best Time to visit']
    return df

df = load_and_clean_data()

# 3. Machine Learning Similarity Calculations
@st.cache_resource
def compute_similarity(dataframe):
    cv = CountVectorizer(stop_words='english')
    count_matrix = cv.fit_transform(dataframe['combined_features'])
    return cosine_similarity(count_matrix)

similarity_matrix = compute_similarity(df)

# --- Streamlit Presentation Layer ---
st.title("🗺️ Smart India Tourism Explorer & AI Recommender")
st.markdown("---")

# Sidebar - User Inputs
st.sidebar.header("🎯 Filter Destinations")
all_states = sorted(df['State'].unique())
selected_states = st.sidebar.multiselect("Filter by State(s)", options=all_states, default=[])

all_types = sorted(df['Type'].unique())
selected_types = st.sidebar.multiselect("Filter by Attraction Type", options=all_types, default=[])

budget = st.sidebar.slider("Maximum Entrance Fee (INR)", min_value=0, max_value=int(df['Entrance Fee in INR'].max()), value=int(df['Entrance Fee in INR'].max()))
duration = st.sidebar.slider("Max Time to Spend (Hours)", min_value=0.5, max_value=float(df['time needed to visit in hrs'].max()), value=float(df['time needed to visit in hrs'].max()), step=0.5)

# Applying filter constraints
filtered_df = df.copy()
if selected_states:
    filtered_df = filtered_df[filtered_df['State'].isin(selected_states)]
if selected_types:
    filtered_df = filtered_df[filtered_df['Type'].isin(selected_types)]
filtered_df = filtered_df[(filtered_df['Entrance Fee in INR'] <= budget) & (filtered_df['time needed to visit in hrs'] <= duration)]

# Main View Split via Tabs
tab1, tab2 = st.tabs(["🎯 AI Recommendation Engine", "🗺️ Dynamic Trip Planner & Data Insights"])

with tab1:
    st.header("✨ Personalized AI Recommendations")
    st.write("Pick an attraction you've enjoyed or want to visit, and our Machine Learning model will find mathematically similar destinations based on category, region, and traits.")
    
    selected_place = st.selectbox("Search or choose a base tourist destination:", sorted(df['Name'].unique()))
    
    if selected_place:
        idx = df[df['Name'] == selected_place].index[0]
        base_spot = df.iloc[idx]
        
        # Display selected item profile metrics
        st.info(f"**Selected Destination Profile:** {base_spot['Name']} | **Type:** {base_spot['Type']} | **State:** {base_spot['State']} | **Rating:** ⭐ {base_spot['Google review rating']}")
        
        # Mathematical calculation ranking
        similarity_scores = list(enumerate(similarity_matrix[idx]))
        sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:6]
        
        st.markdown("### 🌟 Top 5 Similar Recommendations For You")
        cols = st.columns(5)
        for i, (rec_idx, score) in enumerate(sorted_scores):
            rec_row = df.iloc[rec_idx]
            with cols[i]:
                st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; min-height: 260px;">
                    <h4 style="margin-top:0; color:#1f2d3d;">{i+1}. {rec_row['Name']}</h4>
                    <p style="font-size:13px; color:#6c757d; margin-bottom:5px;">📍 {rec_row['City']}, {rec_row['State']}</p>
                    <hr style="margin: 8px 0;">
                    <b>🏷️ Type:</b> {rec_row['Type']}<br>
                    <b>⭐ Rating:</b> {rec_row['Google review rating']}<br>
                    <b>💰 Fee:</b> ₹{rec_row['Entrance Fee in INR']}<br>
                    <b>⏱️ Time:</b> {rec_row['time needed to visit in hrs']} hrs
                </div>
                """, unsafe_allow_html=True)
                st.caption(f"Match Confidence: {int(score*100)}%")
                st.progress(float(score))

with tab2:
    st.header("📊 Travel Discovery Sandbox")
    if not filtered_df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Destinations Found", len(filtered_df))
        c2.metric("Average Rating", f"⭐ {round(filtered_df['Google review rating'].mean(), 2)}")
        c3.metric("Avg Entrance Fee", f"₹ {round(filtered_df['Entrance Fee in INR'].mean(), 1)}")
        
        st.dataframe(filtered_df[['Name', 'Type', 'City', 'State', 'Google review rating', 'Entrance Fee in INR', 'time needed to visit in hrs']], use_container_width=True, hide_index=True)
    else:
        st.warning("No destinations match your current combinations of sidebar filters. Clear parameters to check alternatives!")
