# app.py - NYC Crime Data Visualization
import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar

# Page configuration
st.set_page_config(
    page_title="NYC Crime Data Analysis", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🗽 NYC Crime Data Analysis Dashboard</h1>', unsafe_allow_html=True)

# Sidebar for controls
st.sidebar.header("📊 Filter Controls")

@st.cache_data
def load_data():
    """Load and preprocess the crime data"""
    try:
        # Try to load the arrests.csv file first
        df = pd.read_csv("arrests.csv")
        
        # Data preprocessing
        df['arrest_date'] = pd.to_datetime(df['arrest_date'])
        df = df.dropna(subset=['latitude', 'longitude'])
        df = df[(df['latitude'] != 0) & (df['longitude'] != 0)]
        
        # Extract time features
        df['year'] = df['arrest_date'].dt.year
        df['month'] = df['arrest_date'].dt.month
        df['month_name'] = df['arrest_date'].dt.month_name()
        df['day_of_week'] = df['arrest_date'].dt.day_name()
        df['hour'] = df['arrest_date'].dt.hour
        
        return df
    except FileNotFoundError:
        return None

# Load data
df = load_data()

if df is None:
    # Fallback to file uploader if arrests.csv not found
    st.warning("arrests.csv not found. Please upload a CSV file.")
    file = st.file_uploader("CSV hochladen", type=["csv"])
    if not file:
        st.info("Bitte eine CSV-Datei auswählen.")
        st.stop()
    
    df = pd.read_csv(file)
    if 'arrest_date' in df.columns:
        df['arrest_date'] = pd.to_datetime(df['arrest_date'])
        df = df.dropna(subset=['latitude', 'longitude'])
        df = df[(df['latitude'] != 0) & (df['longitude'] != 0)]
        
        df['year'] = df['arrest_date'].dt.year
        df['month'] = df['arrest_date'].dt.month
        df['month_name'] = df['arrest_date'].dt.month_name()
        df['day_of_week'] = df['arrest_date'].dt.day_name()
        df['hour'] = df['arrest_date'].dt.hour

# Main content
if df is not None and not df.empty:
    # Sidebar filters
    st.sidebar.subheader("🎯 Crime Type Filter")
    
    # Define target crime types from your analysis
    target_crime_types = [
        "ROBBERY", 
        "ASSAULT 3 & RELATED OFFENSES", 
        "OFFENSES AGAINST PUBLIC SAFETY",
        "KIDNAPPING & RELATED OFFENSES", 
        "THEFT-FRAUD"
    ]
    
    # Get unique crime types from data
    all_crime_types = df['ofns_desc'].unique().tolist()
    all_crime_types.sort()
    
    # Filter to show target crimes first, then others
    available_target_crimes = [crime for crime in target_crime_types if crime in all_crime_types]
    other_crimes = [crime for crime in all_crime_types if crime not in target_crime_types]
    
    # Combine with target crimes first
    crime_types_ordered = available_target_crimes + other_crimes
    
    # Multi-select for crime types with target crimes pre-selected
    selected_crimes = st.sidebar.multiselect(
        "Select Crime Types:",
        options=crime_types_ordered,
        default=available_target_crimes,  # Default to your target crimes
        help="Select one or more crime types to display. Target crimes from your analysis are pre-selected."
    )
    
    # Show info about target crimes
    if available_target_crimes:
        st.sidebar.info(f"🎯 Your analysis focuses on {len(available_target_crimes)} target crime types (pre-selected above)")
    
    # Month slider
    st.sidebar.subheader("📅 Time Filter")
    
    # Get available months
    available_months = sorted(df['month'].unique())
    month_names = {i: calendar.month_name[i] for i in available_months}
    
    # Month slider
    selected_month = st.sidebar.select_slider(
        "Select Month:",
        options=available_months,
        value=available_months[0] if available_months else 1,
        format_func=lambda x: month_names.get(x, f"Month {x}"),
        help="Slide to select a specific month"
    )
    
    # Year filter (if multiple years available)
    available_years = sorted(df['year'].unique())
    if len(available_years) > 1:
        selected_year = st.sidebar.selectbox(
            "Select Year:",
            options=available_years,
            index=len(available_years)-1  # Default to latest year
        )
    else:
        selected_year = available_years[0]
    
    # Borough filter
    st.sidebar.subheader("🏙️ Borough Filter")
    available_boroughs = df['arrest_boro'].unique().tolist()
    available_boroughs = [b for b in available_boroughs if pd.notna(b)]
    
    selected_boroughs = st.sidebar.multiselect(
        "Select Boroughs:",
        options=available_boroughs,
        default=available_boroughs,
        help="Select boroughs to display"
    )
    
    # Filter data based on selections
    filtered_df = df[
        (df['ofns_desc'].isin(selected_crimes)) &
        (df['month'] == selected_month) &
        (df['year'] == selected_year) &
        (df['arrest_boro'].isin(selected_boroughs))
    ].copy()
    
    # Main dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Arrests",
            value=f"{len(filtered_df):,}",
            delta=f"{len(filtered_df) - len(df)/12:.0f}"
        )
    
    with col2:
        st.metric(
            label="Crime Types",
            value=len(selected_crimes),
            delta=f"{len(selected_crimes) - len(available_target_crimes)}"
        )
    
    with col3:
        st.metric(
            label="Selected Month",
            value=month_names.get(selected_month, f"Month {selected_month}"),
            delta=None
        )
    
    with col4:
        most_common_crime = filtered_df['ofns_desc'].mode()
        st.metric(
            label="Top Crime Type",
            value=most_common_crime.iloc[0] if not most_common_crime.empty else "N/A",
            delta=None
        )
    
    # Main map
    st.subheader(f"🗺️ Crime Map - {month_names.get(selected_month)} {selected_year}")
    
    if not filtered_df.empty:
        # Create color mapping for different crime types
        unique_crimes = filtered_df['ofns_desc'].unique()
        colors = px.colors.qualitative.Set3[:len(unique_crimes)]
        color_map = dict(zip(unique_crimes, colors))
        
        # Convert colors to RGB for pydeck
        def color_to_rgb(color):
            """Convert various color formats to RGB list"""
            if isinstance(color, str):
                if color.startswith('#'):
                    # Hex color
                    hex_color = color.lstrip('#')
                    if len(hex_color) == 6:
                        return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
                elif color.startswith('rgb'):
                    # RGB string format like 'rgb(255, 0, 0)'
                    import re
                    rgb_values = re.findall(r'\d+', color)
                    if len(rgb_values) >= 3:
                        return [int(rgb_values[i]) for i in range(3)]
                else:
                    # Named colors or other formats - use a color mapping
                    color_dict = {
                        'red': [255, 0, 0], 'blue': [0, 0, 255], 'green': [0, 255, 0],
                        'purple': [128, 0, 128], 'orange': [255, 165, 0], 'brown': [165, 42, 42],
                        'pink': [255, 192, 203], 'gray': [128, 128, 128], 'olive': [128, 128, 0],
                        'cyan': [0, 255, 255], 'yellow': [255, 255, 0], 'magenta': [255, 0, 255]
                    }
                    return color_dict.get(color.lower(), [255, 0, 0])  # Default to red
            
            # Default fallback
            return [255, 0, 0]  # Red
        
        # Create better color mapping using standard colors
        import matplotlib.colors as mcolors
        
        # Use matplotlib's standard colors which are more reliable
        standard_colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown', 
                          'pink', 'gray', 'olive', 'cyan', 'yellow', 'magenta']
        
        # Create color mapping
        color_map = {}
        for i, crime in enumerate(unique_crimes):
            color_idx = i % len(standard_colors)
            color_map[crime] = standard_colors[color_idx]
        
        # Add color column
        filtered_df['color'] = filtered_df['ofns_desc'].map(
            lambda x: color_to_rgb(color_map.get(x, 'red'))
        )
        
        # NYC coordinates for better view
        nyc_lat = 40.7128
        nyc_lon = -74.0060
        
        # Use NYC center if no data points or fallback to data center
        if len(filtered_df) > 0:
            center_lat = filtered_df['latitude'].mean()
            center_lon = filtered_df['longitude'].mean()
        else:
            center_lat = nyc_lat
            center_lon = nyc_lon
        
        # Create the pydeck map with proper NYC view
        view_state = pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=11,
            pitch=0,  # Set to 0 for better map visibility
            bearing=0
        )
        
        layer = pdk.Layer(
            'ScatterplotLayer',
            data=filtered_df,
            get_position='[longitude, latitude]',
            get_color='color',
            get_radius=150,
            radius_scale=8,
            radius_min_pixels=4,
            radius_max_pixels=80,
            pickable=True,
            auto_highlight=True,
        )
        
        tooltip = {
            "html": "<b>Crime:</b> {ofns_desc}<br/>"
                   "<b>Date:</b> {arrest_date}<br/>"
                   "<b>Borough:</b> {arrest_boro}<br/>"
                   "<b>Precinct:</b> {arrest_precinct}",
            "style": {"backgroundColor": "steelblue", "color": "white"}
        }
        
        # Option to switch map types first
        map_type = st.sidebar.radio(
            "🗺️ Map Type:",
            ["Standard Streamlit Map", "Satellite View", "Street Map"],
            help="Choose your preferred map style"
        )
        
        if map_type == "Standard Streamlit Map":
            # Use the reliable Streamlit map
            if not filtered_df.empty:
                map_data = filtered_df[['latitude', 'longitude']].copy()
                st.map(map_data, zoom=11, use_container_width=True)
            else:
                st.info("Keine Daten für die Kartenanzeige verfügbar.")
                
        elif map_type == "Satellite View":
            # Satellite map style
            r = pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip=tooltip,
                map_style='mapbox://styles/mapbox/satellite-streets-v12'
            )
            try:
                st.pydeck_chart(r, use_container_width=True)
            except:
                st.warning("Satellitenkarte nicht verfügbar, zeige Standard-Karte...")
                if not filtered_df.empty:
                    map_data = filtered_df[['latitude', 'longitude']].copy()
                    st.map(map_data, zoom=11, use_container_width=True)
                    
        else:  # Street Map
            # Try different street map styles with fallback
            street_styles = [
                'mapbox://styles/mapbox/streets-v12',
                'mapbox://styles/mapbox/streets-v11',
                'mapbox://styles/mapbox/light-v11',
                'road'
            ]
            
            map_displayed = False
            for style in street_styles:
                try:
                    r = pdk.Deck(
                        layers=[layer],
                        initial_view_state=view_state,
                        tooltip=tooltip,
                        map_style=style
                    )
                    st.pydeck_chart(r, use_container_width=True)
                    map_displayed = True
                    break
                except:
                    continue
            
            if not map_displayed:
                st.warning("3D-Karte nicht verfügbar, zeige Standard-Karte...")
                if not filtered_df.empty:
                    map_data = filtered_df[['latitude', 'longitude']].copy()
                    st.map(map_data, zoom=11, use_container_width=True)
        
        # Legend
        st.subheader("🎨 Crime Type Legend")
        legend_cols = st.columns(min(len(unique_crimes), 4))
        for i, crime in enumerate(unique_crimes):
            with legend_cols[i % 4]:
                color_name = color_map[crime]
                st.markdown(
                    f'<div style="display: flex; align-items: center; margin: 5px 0;">'
                    f'<div style="width: 20px; height: 20px; background-color: {color_name}; '
                    f'border-radius: 50%; margin-right: 10px;"></div>'
                    f'<span style="font-size: 12px;">{crime}</span></div>',
                    unsafe_allow_html=True
                )
        
        # Additional analytics
        st.subheader("📈 Crime Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Crime distribution pie chart
            crime_counts = filtered_df['ofns_desc'].value_counts()
            fig_pie = px.pie(
                values=crime_counts.values,
                names=crime_counts.index,
                title=f"Crime Distribution - {month_names.get(selected_month)} {selected_year}"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Hourly distribution
            hourly_counts = filtered_df['hour'].value_counts().sort_index()
            fig_bar = px.bar(
                x=hourly_counts.index,
                y=hourly_counts.values,
                title="Arrests by Hour of Day",
                labels={'x': 'Hour', 'y': 'Number of Arrests'}
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Borough analysis
        if len(selected_boroughs) > 1:
            st.subheader("🏙️ Borough Comparison")
            borough_counts = filtered_df['arrest_boro'].value_counts()
            fig_borough = px.bar(
                x=borough_counts.values,
                y=borough_counts.index,
                orientation='h',
                title="Arrests by Borough",
                labels={'x': 'Number of Arrests', 'y': 'Borough'}
            )
            st.plotly_chart(fig_borough, use_container_width=True)
        
        # Time series for comparison
        if st.checkbox("Show Monthly Trend Comparison"):
            st.subheader("📊 Monthly Trend Analysis")
            monthly_data = df[
                (df['ofns_desc'].isin(selected_crimes)) &
                (df['year'] == selected_year) &
                (df['arrest_boro'].isin(selected_boroughs))
            ].groupby(['month', 'month_name']).size().reset_index(name='arrests')
            
            fig_trend = px.line(
                monthly_data,
                x='month_name',
                y='arrests',
                title=f"Monthly Arrest Trends - {selected_year}",
                markers=True
            )
            
            # Highlight selected month
            fig_trend.add_vline(
                x=selected_month-1,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Selected: {month_names.get(selected_month)}"
            )
            
            st.plotly_chart(fig_trend, use_container_width=True)
        
    else:
        st.warning("No data available for the selected filters. Please adjust your selection.")
        
    # Data summary
    with st.expander("📋 Data Summary"):
        st.write(f"**Total records in dataset:** {len(df):,}")
        st.write(f"**Filtered records:** {len(filtered_df):,}")
        st.write(f"**Date range:** {df['arrest_date'].min().strftime('%Y-%m-%d')} to {df['arrest_date'].max().strftime('%Y-%m-%d')}")
        st.write(f"**Available crime types:** {len(all_crime_types)}")
        st.write(f"**Target crime types from analysis:** {len(available_target_crimes)}")
        st.write(f"**Available boroughs:** {len(available_boroughs)}")
        
        if st.checkbox("Show sample data"):
            st.dataframe(filtered_df.head(100))

else:
    st.error("No data available. Please check your CSV file.")
    st.info("Expected columns: arrest_date, latitude, longitude, ofns_desc, arrest_boro")
