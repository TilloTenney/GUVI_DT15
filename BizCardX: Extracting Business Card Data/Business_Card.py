import os
import re
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import easyocr
import mysql.connector as sql
from streamlit_option_menu import option_menu

# Set page configurations
app_icon = Image.open(r"C:\Users\vinti\PycharmProjects\pythonProject\Extracting_Business_Card_Data_with_OCR\icon.jpeg")
st.set_page_config(
    page_title="BizCardX: OCR Business Card Data Extraction | Tillo Tenney A E",
    page_icon=app_icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': """# This app is created by *Tillo Tenney A E*"""}
)
st.markdown("<h1 style='text-align: center; color: white;'>BizCardX: OCR Business Card Data Extraction</h1>",
            unsafe_allow_html=True)

# Set up background image
def set_background():
    st.markdown(f""" <style>.stApp {{
                            background: url("https://visme.co/blog/wp-content/uploads/2017/07/50-Beautiful-and-Minimalist-Presentation-Backgrounds-015.jpg");
                            background-size: cover}}
                         </style>""", unsafe_allow_html=True)

set_background()

# Create option menu
with st.sidebar:
    selected_option = option_menu(
        None, ["Home", "Upload & Extract", "Modify"],
        icons=["house-door-fill", "bar-chart", "card-text"],
        default_index=0,
        orientation="vertical",
        styles={
            "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px",
                         "--hover-color": "#AB63FA",
                         "transition": "color 0.3s ease, background-color 0.3s ease"},
            "icon": {"font-size": "25px"},
            "container": {"max-width": "10000px", "padding": "10px", "border-radius": "5px"},
            "nav-link-selected": {"background-color": "#AB63FA", "color": "white"}
        }
    )

# Initialize the EasyOCR reader
ocr_reader = easyocr.Reader(['en'])

# Connect to MySQL database
db_connection = sql.connect(
    host="localhost",
    user="root",
    password="root",
    database="bizcardx_db"
)
db_cursor = db_connection.cursor(buffered=True)

# Create table if not exists
db_cursor.execute('''CREATE TABLE IF NOT EXISTS card_data
                   (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    company_name TEXT,
                    card_holder TEXT,
                    designation TEXT,
                    mobile_number VARCHAR(50),
                    email TEXT,
                    website TEXT,
                    area TEXT,
                    city TEXT,
                    state TEXT,
                    pin_code VARCHAR(10),
                    image LONGBLOB
                    )''')

# Home menu
if selected_option == "Home":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("## :blue[**Technologies Used :**] Python, EasyOCR, Streamlit, MySQL, Pandas")
    st.markdown(
            "## :blue[**Overview :**] Upload a business card image to this sophisticated web app, leveraging easyOCR for seamless extraction of vital details. Explore, edit, and delete the extracted data, while also saving it, along with the submitted image, to a versatile database capable of storing multiple entries.")
    with col2:
        st.video("https://www.youtube.com/watch?v=qCR2Weh64h4")

# Upload and Extract menu
if selected_option == "Upload & Extract":
    st.markdown("### Upload a Business Card")
    uploaded_card = st.file_uploader("Upload here", label_visibility="collapsed", type=["png", "jpeg", "jpg"])

    if uploaded_card is not None:

        def save_uploaded_card(uploaded_card):
            with open(os.path.join("uploaded_cards", uploaded_card.name), "wb") as file:
                file.write(uploaded_card.getbuffer())

        save_uploaded_card(uploaded_card)

        def preview_image(image, ocr_results):
            for (bbox, text, prob) in ocr_results:
                (tl, tr, br, bl) = bbox
                tl = (int(tl[0]), int(tl[1]))
                tr = (int(tr[0]), int(tr[1]))
                br = (int(br[0]), int(br[1]))
                bl = (int(bl[0]), int(bl[1]))
                cv2.rectangle(image, tl, br, (0, 255, 0), 2)
                cv2.putText(image, text, (tl[0], tl[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            plt.rcParams['figure.figsize'] = (15, 15)
            plt.axis('off')
            plt.imshow(image)

        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("#     ")
            st.markdown("#     ")
            st.markdown("### You have uploaded the card")
            st.image(uploaded_card)

        with col2:
            st.markdown("#     ")
            st.markdown("#     ")
            with st.spinner("Please wait processing image..."):
                st.set_option('deprecation.showPyplotGlobalUse', False)
                saved_image_path = os.path.join(os.getcwd(), "uploaded_cards", uploaded_card.name)
                image_data = cv2.imread(saved_image_path)
                ocr_results = ocr_reader.readtext(saved_image_path)
                st.markdown("### Image Processed and Data Extracted")
                st.pyplot(preview_image(image_data, ocr_results))

        saved_image_path = os.path.join(os.getcwd(), "uploaded_cards", uploaded_card.name)
        ocr_result_text = ocr_reader.readtext(saved_image_path, detail=0, paragraph=False)

        def convert_image_to_binary(file_path):
            with open(file_path, 'rb') as file:
                binary_data = file.read()
            return binary_data

        extracted_data = {"company_name": [],
                          "card_holder": [],
                          "designation": [],
                          "mobile_number": [],
                          "email": [],
                          "website": [],
                          "area": [],
                          "city": [],
                          "state": [],
                          "pin_code": [],
                          "image": convert_image_to_binary(saved_image_path)
                          }

        def process_ocr_results(results):
            for index, text in enumerate(results):
                if "www " in text.lower() or "www." in text.lower():
                    extracted_data["website"].append(text)
                elif "WWW" in text:
                    extracted_data["website"] = results[4] + "." + results[5]

                elif "@" in text:
                    extracted_data["email"].append(text)

                elif "-" in text:
                    extracted_data["mobile_number"].append(text)
                    if len(extracted_data["mobile_number"]) == 2:
                        extracted_data["mobile_number"] = " & ".join(extracted_data["mobile_number"])

                elif index == len(results) - 1:
                    extracted_data["company_name"].append(text)

                elif index == 0:
                    extracted_data["card_holder"].append(text)

                elif index == 1:
                    extracted_data["designation"].append(text)

                if re.findall('^[0-9].+, [a-zA-Z]+', text):
                    extracted_data["area"].append(text.split(',')[0])
                elif re.findall('[0-9] [a-zA-Z]+', text):
                    extracted_data["area"].append(text)

                match1 = re.findall('.+St , ([a-zA-Z]+).+', text)
                match2 = re.findall('.+St,, ([a-zA-Z]+).+', text)
                match3 = re.findall('^[E].*', text)
                if match1:
                    extracted_data["city"].append(match1[0])
                elif match2:
                    extracted_data["city"].append(match2[0])
                elif match3:
                    extracted_data["city"].append(match3[0])

                state_match = re.findall('[a-zA-Z]{9} +[0-9]', text)
                if state_match:
                    extracted_data["state"].append(text[:9])
                elif re.findall('^[0-9].+, ([a-zA-Z]+);', text):
                    extracted_data["state"].append(text.split()[-1])
                if len(extracted_data["state"]) == 2:
                    extracted_data["state"].pop(0)

                if len(text) >= 6 and text.isdigit():
                    extracted_data["pin_code"].append(text)
                elif re.findall('[a-zA-Z]{9} +[0-9]', text):
                    extracted_data["pin_code"].append(text[10:])

        process_ocr_results(ocr_result_text)

        def create_dataframe(data):
            dataframe = pd.DataFrame(data)
            return dataframe

        dataframe = create_dataframe(extracted_data)
        st.success("### Data Extracted!")
        st.write(dataframe)

        if st.button("Upload",type="primary"):
            for i, row in dataframe.iterrows():
                sql_query = """INSERT INTO card_data(company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code, image)
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                db_cursor.execute(sql_query, tuple(row))
                db_connection.commit()
            st.success("#### Uploaded to database successfully!")

# Modify menu
if selected_option == "Modify":
    col1, col2, col3 = st.columns([3, 3, 2])
    col2.markdown("## Alter or Delete the data here")
    column1, column2 = st.columns(2, gap="large")
    try:
        with column1:
            db_cursor.execute("SELECT card_holder FROM card_data")
            result_set = db_cursor.fetchall()
            business_cards_dict = {row[0]: row[0] for row in result_set}
            selected_card_holder = st.selectbox("Select a card holder name to update", list(business_cards_dict.keys()))
            st.markdown("#### Update or modify any data below")
            db_cursor.execute(
                "SELECT company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code FROM card_data WHERE card_holder=%s",
                (selected_card_holder,))
            result_row = db_cursor.fetchone()

            updated_company_name = st.text_input("Company_Name", result_row[0])
            updated_card_holder = st.text_input("Card_Holder", result_row[1])
            updated_designation = st.text_input("Designation", result_row[2])
            updated_mobile_number = st.text_input("Mobile_Number", result_row[3])
            updated_email = st.text_input("Email", result_row[4])
            updated_website = st.text_input("Website", result_row[5])
            updated_area = st.text_input("Area", result_row[6])
            updated_city = st.text_input("City", result_row[7])
            updated_state = st.text_input("State", result_row[8])
            updated_pin_code = st.text_input("Pin_Code", result_row[9])

            if st.button("Update",type="primary"):
                db_cursor.execute("""UPDATE card_data SET company_name=%s, card_holder=%s, designation=%s, mobile_number=%s, email=%s, website=%s, area=%s, city=%s, state=%s, pin_code=%s
                                    WHERE card_holder=%s""", (
                    updated_company_name, updated_card_holder, updated_designation, updated_mobile_number, updated_email,
                    updated_website, updated_area, updated_city, updated_state, updated_pin_code, selected_card_holder))
                db_connection.commit()
                st.success("Information updated in the database successfully.")

        with column2:
            db_cursor.execute("SELECT card_holder FROM card_data")
            result_set = db_cursor.fetchall()
            business_cards_dict = {row[0]: row[0] for row in result_set}
            selected_card_holder = st.selectbox("Select a card holder name to delete", list(business_cards_dict.keys()))
            st.write(f"### You have selected :green[**{selected_card_holder}'s**] card to delete")
            st.write("#### Proceed to delete this card?")

            if st.button("Confirm",type="primary"):
                db_cursor.execute(f"DELETE FROM card_data WHERE card_holder='{selected_card_holder}'")
                db_connection.commit()
                st.success("Business card information deleted from the database.")
    except:
        st.warning("There is no data available in the database")

    if st.button("View updated data",type="primary"):
        db_cursor.execute(
            "SELECT company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code FROM card_data")
        updated_dataframe = pd.DataFrame(db_cursor.fetchall(),
                                         columns=["Company_Name", "Card_Holder", "Designation", "Mobile_Number", "Email",
                                                  "Website", "Area", "City", "State", "Pin_Code"])
        st.write(updated_dataframe)
