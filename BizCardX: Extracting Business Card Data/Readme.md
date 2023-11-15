# BizCardX: Revolutionizing Business Card Data Management with OCR

EasyOCR, a Python powerhouse, redefines Optical Character Recognition (OCR) for computer vision developers. Seamlessly extracting text from images and scanned documents, this Python library simplifies OCR. In the BizCardX project, EasyOCR takes center stage, effortlessly handling text extraction from business cards.

## Why EasyOCR?

### Easy Installation: A single pip command installs the EasyOCR package.
### Minimal Dependencies: EasyOCR keeps dependencies minimal, ensuring a hassle-free OCR development environment setup.
### Simplicity in Usage: With just one import statement, EasyOCR becomes part of your project. Two lines of code initialize the Reader class and perform OCR using the readtext function.

## Project Overview: BizCardX
Introducing BizCardX, an intuitive tool designed for extracting valuable information from business cards. Leveraging OCR technology, the tool recognizes and classifies text on business cards, storing the data in a SQL database through regular expression-based classification. The user-friendly GUI, built with Streamlit, guides users through uploading business card images and extracting information. The extracted data is elegantly displayed, allowing users to effortlessly add it to the database. Data stored in the database is easily accessible for reading, updating, and deleting.


## Libraries/Modules Utilized

* Pandas: Creating a DataFrame with scraped data.
* mysql.connector: Storing and retrieving data from the database.
* Streamlit: Crafting a Graphical User Interface.
* EasyOCR: Extracting text from images.

## Workflow
### To embark on the BizCardX Data Extraction journey, follow these steps:

Install the required libraries using the pip install command: Streamlit, mysql.connector, pandas, easyocr.

pip install [Library Name]

Execute the “Business_Card.py” using the streamlit run command.

streamlit run Business_Card.py

### A webpage opens with three menu options: HOME, UPLOAD & EXTRACT, MODIFY, empowering users to upload, extract, modify, or delete business card information.

* Upon uploading a business card, easyocr extracts the text from the card.

* The extracted text undergoes classification (handled by the user-defined get_data() function), identifying components like company name, cardholder name, designation, contact details, and more using loops and regular expressions.

* The classified data is presented on-screen for user editing.

* Clicking Upload to Database stores the data in the MySQL Database. (Note: Provide host, user, password, and database name in create_database, sql_table_creation, and 
  connect_database for connection establishment.)

* The MODIFY menu facilitates reading, updating, and deleting data uploaded to the SQL Database.
