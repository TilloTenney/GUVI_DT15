# Importing necessary libraries
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import os
from PIL import Image
import warnings

# Ignoring warnings
warnings.filterwarnings('ignore')

# Loading app icon
app_icon_custom = Image.open(r"C:\Users\vinti\PycharmProjects\pythonProject\AirBnB\icon.jpeg")

# Setting up Streamlit page configuration
st.set_page_config(
    page_title="Airbnb Analysis | Tillo Tenney A E",
    page_icon=app_icon_custom,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': """# This app is created by *Tillo Tenney A E*"""}
)

st.markdown("<h1 style='text-align: center; color: red;'>Airbnb Analysis</h1>",
            unsafe_allow_html=True)

# Setting background for the app
def set_background_custom():
    st.markdown(f""" <style>.stApp {{
                            background: url("https://wallpaper-mania.com/wp-content/uploads/2018/09/High_resolution_wallpaper_background_ID_77700342881.jpg");
                            background-size: cover}}
                         </style>""", unsafe_allow_html=True)

set_background_custom()

# Create an option menu in the sidebar
with st.sidebar:
    selected_option_custom = option_menu(
        None, ["Home", "Upload & Extract"],
        icons=["house-door-fill", "bar-chart"],
        default_index=0,
        orientation="vertical",
        styles={
            "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px",
                         "--hover-color": "#ff1a1a",
                         "transition": "color 0.3s ease, background-color 0.3s ease"},
            "icon": {"font-size": "25px"},
            "container": {"max-width": "10000px", "padding": "10px", "border-radius": "5px"},
            "nav-link-selected": {"background-color": "#ff1a1a", "color": "white"}
        }
    )

# Define actions based on the selected option
if selected_option_custom == "Home":
    col1_custom, col2_custom = st.columns(2)
    with col1_custom:
        st.markdown("## :red[**Technologies Used :**] Python, MongoDB Atlas, EDA, Streamlit, Pandas, Tableau")
        st.markdown("## :red[**About :**]Airbnb, a San Francisco-based online marketplace, founded in 2008 by Chesky, Blecharczyk, and Gebbia, connects users with short- and long-term homestays and experiences, charging commissions per booking.")
    st.markdown("## :red[**Overview :**] Analyze Airbnb data using MongoDB Atlas, clean and prepare data, and develop geospatial visualizations and dynamic plots for insights into pricing, availability, and location-based trends.")
    with col2_custom:
        st.write("##")
        st.video("https://www.youtube.com/watch?v=dA2F0qScxrI&pp=ygUMYWlyYm5iIGludHJv")
        st.write("##")
        col3_custom, col4_custom, col5_custom, col6_custom, col7_custom= st.columns(5)
        with col7_custom:
            st.write("[ 👉 :orange[LinkdIn]](https://www.linkedin.com/in/tillo-tenney-a-e-aspiring-datascientist/)")
            st.write("[ 👉 :orange[Git]](https://github.com/TilloTenney/Projects_TilloTenney)")

if selected_option_custom == "Upload & Extract":
    # File upload functionality
    fl_custom = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
    if fl_custom is not None:
        filename_custom = fl_custom.name
        st.write(filename_custom)
        file_name_custom = str(filename_custom)
        path_custom = r"C:\Users\vinti\PycharmProjects\pythonProject\AirBnB"
        csv_filename_custom = os.path.join(path_custom, file_name_custom)
        df_custom = pd.read_csv(csv_filename_custom, encoding="ISO-8859-1")
    else:
        os.chdir(r"C:\Users\vinti\PycharmProjects\pythonProject\AirBnB")
        df_custom = pd.read_csv("AirBnB.csv", encoding="ISO-8859-1")

    # Sidebar options for filtering data
    st.sidebar.header("Choose your filter: ")
    neighbourhood_group_custom = st.sidebar.multiselect("Pick your neighbourhood_group", df_custom["neighbourhood_group"].unique())
    if not neighbourhood_group_custom:
        df2_custom = df_custom.copy()
    else:
        df2_custom = df_custom[df_custom["neighbourhood_group"].isin(neighbourhood_group_custom)]

    neighbourhood_custom = st.sidebar.multiselect("Pick the neighbourhood", df2_custom["neighbourhood"].unique())
    if not neighbourhood_custom:
        df3_custom = df2_custom.copy()
    else:
        df3_custom = df2_custom[df2_custom["neighbourhood"].isin(neighbourhood_custom)]

    # Filtering data based on selected options
    if not neighbourhood_group_custom and not neighbourhood_custom:
        filtered_df_custom = df_custom
    elif not neighbourhood_custom:
        filtered_df_custom = df_custom[df_custom["neighbourhood_group"].isin(neighbourhood_group_custom)]
    elif not neighbourhood_group_custom:
        filtered_df_custom = df_custom[df_custom["neighbourhood"].isin(neighbourhood_custom)]
    elif neighbourhood_custom:
        filtered_df_custom = df3_custom[df_custom["neighbourhood"].isin(neighbourhood_custom)]
    elif neighbourhood_group_custom:
        filtered_df_custom = df3_custom[df_custom["neighbourhood_group"].isin(neighbourhood_group_custom)]
    elif neighbourhood_group_custom and neighbourhood_custom:
        filtered_df_custom = df3_custom[df_custom["neighbourhood_group"].isin(neighbourhood_group_custom) & df3_custom["neighbourhood"].isin(neighbourhood_custom)]
    else:
        filtered_df_custom = df3_custom[df3_custom["neighbourhood_group"].isin(neighbourhood_group_custom) & df3_custom["neighbourhood"].isin(neighbourhood_custom)]

    # Create visualizations and summaries
    room_type_df_custom = filtered_df_custom.groupby(by=["room_type"], as_index=False)["price"].sum()
    col1_custom, col2_custom = st.columns(2)
    with col1_custom:
        st.subheader("room_type_ViewData")
        fig_custom = px.bar(room_type_df_custom, x="room_type", y="price", text=['${:,.2f}'.format(x) for x in room_type_df_custom["price"]],
                     template="seaborn")
        st.plotly_chart(fig_custom, use_container_width=True, height=200)

    with col2_custom:
        st.subheader("neighbourhood_group_ViewData")
        fig_custom = px.pie(filtered_df_custom, values="price", names="neighbourhood_group", hole=0.5)
        fig_custom.update_traces(text=filtered_df_custom["neighbourhood_group"], textposition="outside")
        st.plotly_chart(fig_custom, use_container_width=True)

    cl1_custom, cl2_custom = st.columns((2))
    with cl1_custom:
        with st.expander("room_type wise price"):
            st.write(room_type_df_custom.style.background_gradient(cmap="Blues"))
            csv_custom = room_type_df_custom.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=csv_custom, file_name="room_type.csv", mime="text/csv",
                               help='Click here to download the data as a CSV file')

    with cl2_custom:
        with st.expander("neighbourhood_group wise price"):
            neighbourhood_group_custom = filtered_df_custom.groupby(by="neighbourhood_group", as_index=False)["price"].sum()
            st.write(neighbourhood_group_custom.style.background_gradient(cmap="Oranges"))
            csv_custom = neighbourhood_group_custom.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=csv_custom, file_name="neighbourhood_group.csv", mime="text/csv",
                               help='Click here to download the data as a CSV file')

    data1_custom = px.scatter(filtered_df_custom, x="neighbourhood_group", y="neighbourhood", color="room_type")
    data1_custom['layout'].update(title="Room_type in the Neighbourhood and Neighbourhood_Group wise data using Scatter Plot.",
                           titlefont=dict(size=20), xaxis=dict(title="Neighbourhood_Group", titlefont=dict(size=20)),
                           yaxis=dict(title="Neighbourhood", titlefont=dict(size=20)))
    st.plotly_chart(data1_custom, use_container_width=True)

    with st.expander("Detailed Room Availability and Price View Data in the Neighbourhood"):
        st.write(filtered_df_custom.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))

    csv_custom = df_custom.to_csv(index=False).encode('utf-8')
    st.download_button('Download Data', data=csv_custom, file_name="Data.csv", mime="text/csv")

    import plotly.figure_factory as ff

    st.subheader(":point_right: Neighbourhood_group wise Room_type and Minimum stay nights")
    with st.expander("Summary_Table"):
        df_sample_custom = df_custom[0:5][["neighbourhood_group", "neighbourhood", "reviews_per_month", "room_type", "price", "minimum_nights", "host_name"]]
        fig_custom = ff.create_table(df_sample_custom, colorscale="Cividis")
        st.plotly_chart(fig_custom, use_container_width=True)

    st.subheader("Airbnb Analysis in Map view")
    df_custom = df_custom.rename(columns={"Latitude": "lat", "Longitude": "lon"})
    st.map(df_custom)
