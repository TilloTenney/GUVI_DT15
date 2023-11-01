**Phonepe Pulse Data Visualisation:**

Data visualization is the process of graphically representing data using charts, graphs, and visual elements to facilitate comprehension and analysis. These visualizations are designed to present data in an aesthetically pleasing and easily understandable format, allowing users to quickly discern trends, patterns, and insights from their transaction history.

**Technical Overview:**

Problem Statement:
The Phonepe Pulse Github repository houses a substantial volume of data encompassing various metrics and statistics. The objective is to extract, process, and present this data in a user-friendly, visual format.

**Approach:**

*Data Extraction:* Employ scripting to clone the Phonepe Pulse Github repository, retrieving the data and storing it in a suitable format like CSV or JSON.

*Data Transformation:* Utilize Python, along with libraries such as Pandas, to manipulate and preprocess the data. This may include data cleaning, handling missing values, and transforming the data for analysis and visualization.

*Database Insertion:* Use the "mysql-connector-python" library in Python to establish a connection with a MySQL database and insert the transformed data using SQL commands.

*Dashboard Creation:* Leverage Python libraries like Streamlit and Plotly to create an interactive and visually appealing dashboard. Plotly's built-in geo map functions can be employed to visualize data on a map, while Streamlit can be used to construct a user-friendly interface with dropdown options for selecting various data subsets.

*Data Retrieval:* Utilize the "mysql-connector-python" library to connect to the MySQL database and fetch the data into a Pandas dataframe, updating the dashboard dynamically.

*Deployment:* Ensure the solution's security, efficiency, and user-friendliness. Conduct thorough testing and deploy the dashboard publicly, making it accessible to users.

**Technologies Utilized:**

Github Cloning
Python
Pandas
MySQL
mysql-connector-python
Streamlit
Plotly

**Dashboard:**
The dashboard is divided into Three main sections,

*HOME Page:*
Details about Phonepe Pulse Data Visualisation.

*Analysis:*
The analysis section provides insights at different levels:
All India
States
Top Categories
Under each of these, it offers analysis based on both transaction and user data within each category, and it presents data based on the year and quarter.

*Insights:*
The insights section simplifies the findings from the analysis, presenting them in a user-friendly manner. Additionally, an annual report is provided, summarizing key takeaways.
