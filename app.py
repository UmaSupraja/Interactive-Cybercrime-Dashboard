import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(page_title="Cyber Crime Dashboard", layout="wide")

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; padding: 20px; border-radius: 10px; }
    h1, h2, h3 { color: #0e1117; text-align: center; }
    .stButton > button { color: white; background: #6c63ff; }
    </style>
""", unsafe_allow_html=True)

st.title("🔐 Cyber Crime in India (2002–2020)")

# --- Load and Clean Data ---
df = pd.read_csv("Dataset.csv")
df.fillna(0, inplace=True)
df.columns = df.columns.astype(str)
df['State/UT'] = df['State/UT'].str.strip()

# --- Tabs Layout ---
tab2, tab3, tab4, tab5 = st.tabs([ "📊 Visual Analysis", "📈 Interactive Trends", "📌 Insights", "🧾 Data Overview"])


with tab2:
    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import plotly.express as px

    # Assume df is already loaded and cleaned...

    st.header("📊 Visualizations")

    # 1. Dynamic Year Input with Validation for Top 10 States bar chart
    year_input = st.text_input("Enter year (2002 - 2020) for Top 10 States chart:", "2020")

    def validate_year(year_str):
        if not year_str.isdigit():
            return False
        year_int = int(year_str)
        return 2002 <= year_int <= 2020

    if validate_year(year_input):
        year = int(year_input)

        # Title with clickable bulb icon triggering an expander below
        st.markdown(f"### 🔟 Top 10 States by Cyber Crimes in {year}  <span style='cursor:pointer;'>💡</span>", unsafe_allow_html=True)
        with st.expander("What is this chart? How to read it?"):
            st.write("""
            This bar chart displays the top 10 states with the highest number of cybercrime cases for the selected year.
            The height of each bar corresponds to the number of cases.
            Use this chart to quickly identify states most affected by cybercrime in that year.
            """)

        top10_year = df.sort_values(by=str(year), ascending=False).head(10)
        fig_bar = px.bar(top10_year, x='State/UT', y=str(year), color=str(year), title=f"Top 10 States in {year}")
        st.plotly_chart(fig_bar, use_container_width=True)

    else:
        st.error("⚠️ Please enter a valid year between 2002 and 2020.")

    # 2. Yearly Correlation Heatmap with year range slider
    st.markdown("### 🔥 Yearly Correlation Heatmap  <span style='cursor:pointer;'>💡</span>", unsafe_allow_html=True)
    with st.expander("What is this heatmap? How to interpret?"):
        st.write("""
        The heatmap shows correlations between cybercrime cases across the selected years.
        Values close to 1 mean years had very similar trends, while values close to -1 mean opposite trends.
        Use this to understand if crime patterns are stable or changing year-to-year.
        """)

    start_year, end_year = st.slider(
        "Select year range for correlation heatmap:",
        min_value=2002, max_value=2020, value=(2010, 2020)
    )
    years_for_corr = [str(y) for y in range(start_year, end_year + 1)]
    corr_data = df[years_for_corr].corr()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr_data, cmap='coolwarm', annot=True, ax=ax)
    st.pyplot(fig)

    # 3. Yearly Distribution (Boxplot) with multi-select
    st.markdown("### 📦 Yearly Distribution (Boxplot)  <span style='cursor:pointer;'>💡</span>", unsafe_allow_html=True)
    with st.expander("What does this boxplot show? How to read it?"):
        st.write("""
        The boxplot shows distribution of cybercrime cases across selected years.
        The box shows the interquartile range (middle 50%), the line inside is the median,
        and dots/outliers represent extreme values.
        This helps identify trends, spreads, and anomalies in the data.
        """)

    selected_years = st.multiselect(
        "Select years for boxplot (hold Ctrl/Cmd to select multiple):",
        options=[str(y) for y in range(2002, 2021)],
        default=[str(y) for y in range(2018, 2021)]
    )
    if selected_years:
        fig2, ax2 = plt.subplots(figsize=(12, 5))
        sns.boxplot(data=df[selected_years], ax=ax2)
        plt.xticks(rotation=90)
        st.pyplot(fig2)
    else:
        st.info("Select at least one year to show the boxplot.")

import streamlit as st
import pandas as pd
import plotly.express as px

# Assume df is already loaded and cleaned

with tab3:
    st.header("📈 Interactive Year-wise Trends")

    states = df['State/UT'].unique().tolist()
    default_state = 'MAHARASHTRA' if 'MAHARASHTRA' in states else states[0]
    selected_state = st.selectbox("Choose a State", states, index=states.index(default_state))

    # Filter data for the selected state, years 2002 to 2020 (assuming columns are strings)
    years_cols = [str(y) for y in range(2002, 2021)]
    state_data = df[df['State/UT'] == selected_state][years_cols].T.reset_index()
    state_data.columns = ['Year', 'Cases']
    state_data['Cases'] = state_data['Cases'].astype(int)

    # Plot line chart
    st.subheader(f"📊 Trend: {selected_state} (2002–2020)")
    fig_line = px.line(state_data, x='Year', y='Cases', markers=True, title=f"Yearly Trend for {selected_state}")
    st.plotly_chart(fig_line, use_container_width=True)

    # Calculate stats
    avg_cases = state_data['Cases'].mean()
    min_cases = state_data['Cases'].min()
    max_cases = state_data['Cases'].max()
    year_lowest = state_data[state_data['Cases'] == min_cases]['Year'].values[0]
    year_highest = state_data[state_data['Cases'] == max_cases]['Year'].values[0]

    # Display info cards using columns
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Average Cases", f"{avg_cases:.1f}")
    col2.metric("Minimum Cases", f"{min_cases}")
    col3.metric("Maximum Cases", f"{max_cases}")
    col4.metric("Year with Lowest Crimes", year_lowest)
    col5.metric("Year with Highest Crimes", year_highest)

    # Display Image of the State
    # You need a folder "state_images" with images named exactly like states e.g. "MAHARASHTRA.jpg"
    import os
    from PIL import Image

    img_path = f"state_images/{selected_state}.jpg"  # or .png depending on your images
    if os.path.exists(img_path):
        st.image(Image.open(img_path), caption=f"{selected_state}", use_column_width=True)
    else:
        st.info("State image not available.")
import streamlit as st
import plotly.express as px

with tab4:
    st.header("📌 Summary Insights")

    # Multi-select for years
    years = st.multiselect(
        "Select Year(s) to Compare", 
        options=[str(y) for y in range(2002, 2021)], 
        default=['2020']
    )

    if not years:
        st.warning("Please select at least one year.")
    else:
        for year_str in years:
            year = int(year_str)

            # Calculate stats for this year
            max_cases = df[year_str].max()
            min_cases = df[year_str].min()
            mean_cases = df[year_str].mean()
            mode_cases = df[year_str].mode()[0]
            var_cases = df[year_str].var()

            st.markdown(f"### Year: {year}")
            st.markdown(f"""
            - 🔼 **Max Cases ({year}):** {max_cases}
            - 🔽 **Min Cases ({year}):** {min_cases}
            - 📊 **Mean Cases ({year}):** {mean_cases:.2f}
            - 🔁 **Mode ({year}):** {mode_cases}
            - 🧮 **Variance ({year}):** {var_cases:.2f}
            """)

            st.subheader(f"States with > 5000 Cases in {year}")
            st.dataframe(df[df[year_str] > 5000].reset_index(drop=True), use_container_width=True)

            st.subheader(f"States with 0 Cases in {year}")
            st.dataframe(df[df[year_str] == 0].reset_index(drop=True), use_container_width=True)

            st.subheader(f"🥧 Top 5 States Share ({year})")
            top5 = df[['State/UT', year_str]].sort_values(by=year_str, ascending=False).head(5)
            fig_pie = px.pie(top5, names='State/UT', values=year_str, title=f"Top 5 States by {year} Crimes")
            st.plotly_chart(fig_pie, use_container_width=True)


tab5 = st.tabs(["🧾 Data Overview"])[0]

with tab5:
    st.header("📋 DataFrame Exploration")

    options = [
        "Shape",
        "Columns",
        "Data Types",
        "Describe",
        "Missing Values",
        "Unique Values",
        "Head (Top 5)",
        "Tail (Bottom 5)",
        "Random Sample (5 Rows)",
        "Unique States",
        "Value Counts (State/UT)",
        "Column Names as List",
        "Memory Usage"
    ]

    choice = st.selectbox("Select DataFrame Info to View:", options)

    if choice == "Shape":
        st.write("**Rows, Columns:**", df.shape)

    elif choice == "Columns":
        st.write(df.columns.tolist())

    elif choice == "Data Types":
        st.dataframe(df.dtypes.reset_index().rename(columns={"index": "Column", 0: "Data Type"}))

    elif choice == "Describe":
        st.dataframe(df.describe())

    elif choice == "Missing Values":
        st.dataframe(df.isnull().sum().reset_index().rename(columns={"index": "Column", 0: "Missing Count"}))

    elif choice == "Unique Values":
        st.dataframe(df.nunique().reset_index().rename(columns={"index": "Column", 0: "Unique Count"}))

    elif choice == "Head (Top 5)":
        st.dataframe(df.head())

    elif choice == "Tail (Bottom 5)":
        st.dataframe(df.tail())

    elif choice == "Random Sample (5 Rows)":
        st.dataframe(df.sample(5))

    elif choice == "Unique States":
        st.write(df['State/UT'].unique())

    elif choice == "Value Counts (State/UT)":
        st.dataframe(df['State/UT'].value_counts().reset_index().rename(columns={"index": "State/UT", "State/UT": "Count"}))

    elif choice == "Column Names as List":
        st.write(df.columns.tolist())

    elif choice == "Memory Usage":
        st.dataframe(df.memory_usage(deep=True).reset_index().rename(columns={"index": "Column", 0: "Memory Bytes"}))
