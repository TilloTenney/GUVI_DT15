**Title:** YouTube Data Harvesting and Warehousing using SQL, MongoDB, and Streamlit

**Skills Acquired:** Python scripting, Data Collection, MongoDB, Streamlit, API integration, Data Management using MongoDB (Atlas) and SQL

**Domain:** Social Media

**Problem Statement:**

  * The burgeoning ecosystem of YouTube content presents a formidable challenge to efficiently access, analyze, and manage data from multiple YouTube channels. This project offers a comprehensive solution, focusing on the development of a Streamlit application to streamline data collection, warehousing, and analysis. The technical problem statement encompasses the following objectives:

**Data Retrieval Module:** Implement an interface that enables users to input a YouTube channel ID, facilitating the retrieval of crucial data elements from the YouTube API. These elements include channel name, subscriber count, video count, playlist IDs, video IDs, likes, dislikes, and comments for each video.

**Data Storage in MongoDB:** Create a data lake within a MongoDB database to store the collected YouTube data. MongoDB is chosen for its aptitude in accommodating unstructured and semi-structured data.

**Multi-Channel Data Collection:** Develop a feature allowing users to concurrently collect data from up to 10 YouTube channels, seamlessly storing it within the MongoDB data lake.

**Data Warehousing in SQL:** Enable users to select specific channels and transfer their data from the MongoDB data lake to a structured SQL database. Common SQL databases such as MySQL or PostgreSQL will be considered for this purpose.

**Data Retrieval and Analysis:** Empower users with the capability to search, retrieve, and analyze data from the SQL database utilizing SQL queries. This includes the ability to perform table joins to derive comprehensive channel insights.

**Technical Approach:**

  * The approach taken to address the aforementioned technical problem statement can be broken down into the following detailed steps:

**Streamlit App Development:**

  * Utilize Streamlit to construct an intuitive and user-friendly interface.
  * Implement input fields for YouTube channel IDs, enabling users to initiate data retrieval processes.

**YouTube API Integration:**

  * Employ the Google API client library for Python to establish connectivity with the YouTube API.
  * Create functions to request and extract channel and video-related data.

**MongoDB Data Lake Implementation:**

  * Design data models for MongoDB to accommodate the various data elements.
  * Develop functionalities to store the collected data in the MongoDB data lake.


**SQL Data Warehouse Setup:**

  * Assess and select a suitable SQL database system (e.g., MySQL, PostgreSQL) for data warehousing.
  * Create SQL tables to represent the structured data for multiple YouTube channels.

**SQL Querying and Analysis:**

  * Utilize Python SQL libraries such as SQLAlchemy to facilitate interaction with the SQL database.
  * Construct SQL queries to enable efficient data retrieval, including table joins for comprehensive channel analysis.

**Streamlit Data Visualization Integration:**

  * Incorporate the retrieved and analyzed data into the Streamlit application.
  * Leverage Streamlit's data visualization capabilities to generate informative charts, graphs, and tables for user-friendly data exploration and understanding.
