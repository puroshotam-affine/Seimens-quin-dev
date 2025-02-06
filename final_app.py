import streamlit as st
import pandas as pd
from PIL import Image
import re
import os
import time

# Constants
BASE_PATH = os.getcwd()
FAQ_FILE = os.path.join(BASE_PATH, "faq_streamlit_genai", "faq.csv")
LOGO_PATH = "Siemens_Energy_logo.png"

# Functions
def add_logo(logo_path, width, height):
    """Load and resize a logo image."""
    try:
        logo = Image.open(logo_path)
        return logo.resize((width, height))
    except Exception as e:
        st.error(f"Error loading logo: {e}")
        return None

def add_plot(plot_path):
    """Load and return the plot image."""
    try:
        return Image.open(plot_path)
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Error loading plot: {e}")
        return None

def load_dataframe(file_path):
    """Load a dataframe from a CSV file."""
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"Dataframe file not found at {file_path}.")
        return None
    except Exception as e:
        st.error(f"Error loading dataframe: {e}")
        return None

# Streamlit UI Setup
st.markdown(
    "<h1 style='color:Blue; text-align:center;'>Quick Insights on Sales Data</h1>",
    unsafe_allow_html=True,
)

# Add Sidebar Logo
my_logo = add_logo(logo_path=LOGO_PATH, width=200, height=80)
if my_logo:
    st.sidebar.image(my_logo)

# Sidebar Radio Button
radio_choice = st.sidebar.radio(
    "Choose a flow",
    ["Insights Assistant"]
)

# Load FAQ Data
faq_df = load_dataframe(FAQ_FILE)

if faq_df is not None:
    # User Input for Query
    query = st.text_input("Enter your query:")

    # Handle Query
    if query:
        try:
            with st.spinner("Generating Insights...."):
                # Escape special characters for regex search
                escaped_query = re.escape(query)
                
                # Search for matching row in the DataFrame
                matched_rows = faq_df[faq_df["Questions"].str.contains(escaped_query, case=False, na=False)]
                
                if not matched_rows.empty:
                    row = matched_rows.iloc[0]
                    
                    # Extract values from the matched row
                    sql_query = row.get('SQL Query', '')
                    dataframe_path = os.path.join(BASE_PATH, str(row.get('Data', '')).replace('"', '').replace('\\', '//'))
                    insights = row.get('Insights', 'No insights available.')
                    plot_path = os.path.join(BASE_PATH, str(row.get('Plot', '')).replace('"', '').replace('\\', '//'))

                    # Display SQL Query
                    time.sleep(3)
                    st.subheader("SQL Query")
                    st.code(sql_query if sql_query else "No SQL query available.")

                    # Display DataFrame
                    time.sleep(2)
                    st.subheader("Dataframe")
                    df = load_dataframe(dataframe_path)
                    if df is not None:
                        st.dataframe(df)
                    else:
                        st.warning("No dataframe available.")

                    # Display Insights
                    time.sleep(2)
                    st.subheader("Insights")
                    st.markdown(insights)

                    # Display Visualization (if applicable)
                    time.sleep(2)
                    st.subheader("Visualization")
                    plot_image = add_plot(plot_path)
                    if plot_image:
                        st.image(plot_path, caption="Visualization", use_column_width=True)
                    else:
                        st.warning("No visualization available.")
                else:
                    st.error("No matching query found. Please try a different query.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.info("Please enter a query to get insights.")
else:
    st.error("Failed to load the FAQ dataset. Please check the file path.")
