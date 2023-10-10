import pandas as pd
import isodate as iso
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector as sql
import pymongo
from googleapiclient.discovery import build
from PIL import Image
from get_channel_details import get_channel_details
from get_channel_videos import get_channel_videos
from get_playlist_name import get_playlist_name
from get_video_details import get_video_details
from get_comments_details import get_comments_details
from channel_names import channel_names


# SETTING PAGE CONFIGURATIONS
icon = Image.open("Youtube_logo.png")
st.set_page_config(page_title="Youtube Data Harvesting and Warehousing | Tillo Tenney A E",
                   page_icon=icon,
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={'About': """# This app is created by *Tillo Tenney A E_DT15*"""})

# CREATING OPTION MENU
with st.sidebar:
    selected = option_menu(None, ["Home", "Extract & Transform", "View"],
                           icons=["house-door-fill", "tools", "card-text"],
                           default_index=0,
                           orientation="vertical",
                           styles={"nav-link": {"font-size": "20px", "text-align": "centre", "margin": "0px",
                                                "--hover-color": "#7792E3"},
                                   "icon": {"font-size": "20px"},
                                   "container": {"max-width": "7000px"},
                                   "nav-link-selected": {"background-color": "#273346"}})

# Bridging a connection with MongoDB Atlas and Creating a new database(youtube_data)
client = pymongo.MongoClient("localhost", 27017)
db = client.youtube_raw_data

# CONNECTING WITH MYSQL DATABASE(youtube)
mydb = sql.connect(host="localhost",
                   user="root",
                   password="root",
                   database="youtube"
                   )
mycursor = mydb.cursor(buffered=True)

# BUILDING CONNECTION WITH YOUTUBE API
api_key = "AIzaSyCs0WxXm3TrDBlqdr_eX5ErQ-XJk6kyVwg"
youtube = build('youtube', 'v3', developerKey=api_key)

# HOME PAGE
if selected == "Home":
    # Title Image
    st.image(["title.png","youtube.png"],width=200)
    col1, col2 = st.columns(2, gap='medium')
    col1.markdown("## :blue[Domain] : _Social Media_")
    col1.subheader(":blue[Technologies used] : ")
    col1.write("Python,MongoDB, Youtube Data API V3, MySql, Streamlit")
    col1.subheader(":blue[Overview] : ")
    col1.write("Retrieving the Youtube channels data from the Google API, storing it in a MongoDB as data lake, migrating and transforming data into a SQL database,then querying the data and displaying it in the Streamlit app.")

# EXTRACT AND TRANSFORM PAGE
if selected == "Extract & Transform":
    tab1, tab2 = st.tabs(["$\huge 📝 EXTRACT $", "$\huge🚀 TRANSFORM $"])

    # EXTRACT TAB
    with tab1:
        st.markdown("#    ")
        st.write("### Enter YouTube Channel_ID below :")
        ch_id = st.text_input(
            "Hint : Goto channel's home page > Right click > View page source > Find channel_id(To extract multiple channels kindly seperate channel id's with comma(,))").split(',')

        if ch_id and st.button("Extract Data"):
            ch_details = get_channel_details(ch_id)
            #ch_details1= " ".join(ch_details)
            #st.write(f'#### Extracted data from :green["{ch_details1[0]["Channel_name"]}"] channel')
            st.table(ch_details)

        if st.button("Upload to MongoDB"):
            with st.spinner('Please Wait for it...'):
                ch_details = get_channel_details(ch_id)
                v_ids = get_channel_videos(ch_id)
                plist_name = get_playlist_name(ch_id)
                vid_details = get_video_details(v_ids)




                def comments():
                    com_d = []
                    for i in v_ids:
                        com_d += get_comments_details(i)
                    return com_d


                comm_details = comments()

                collections1 = db.channel_details
                collections1.insert_many(ch_details)

                collections2 = db.video_details
                collections2.insert_many(vid_details)

                collections3 = db.playlist_name
                collections3.insert_many(plist_name)

                collections4 = db.comments_details
                collections4.insert_many(comm_details)
                st.success("Upload to MogoDB successful !!")

    with tab2:
        st.markdown("#   ")
        st.markdown("### Select a channel to begin Transformation to SQL")

        ch_names = channel_names()
        user_inp = st.selectbox("Select channel", options=ch_names)


        def insert_into_channels():
            collections = db.channel_details
            query = """INSERT INTO channel (channel_id, channel_name, channel_views, channel_description, channel_status) VALUES(%s,%s,%s,%s,%s)"""

            for i in collections.find({"Channel_name": user_inp}, {'_id': 0,'Playlist_id':0,'Subscribers':0,'Total_videos':0,'Country':0}):
                print(tuple(i.values()))
                mycursor.execute(query, tuple(i.values()))
                mydb.commit()

        def insert_into_playlist():
            collections = db.playlist_name
            query = """INSERT INTO playlist VALUES(%s,%s,%s)"""

            for i in collections.find({"Channel_name": user_inp}, {'_id': 0,'Channel_name':0}):
                print(tuple(i.values()))
                mycursor.execute(query, tuple(i.values()))
                mydb.commit()


        def insert_into_videos():
            collections1 = db.video_details
            query1 = """INSERT INTO video(channel_name, video_id, video_name, thumbnail, video_description, published_date, duration, view_count, like_count, dislike_count, comment_count, favorite_count, caption_status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

            for i in collections1.find({"Channel_name": user_inp}, {'_id': 0, 'Channel_id':0, 'Tags':0, 'Definition':0}):
                print(tuple(i.values()))
                mycursor.execute(query1, tuple(i.values()))
                mydb.commit()


        def insert_into_comments():
            collections1 = db.video_details
            collections2 = db.comments_details
            query2 = """INSERT INTO comment(comment_id, video_id, comment_text, comment_author, comment_published_date) VALUES(%s,%s,%s,%s,%s)"""

            for vid in collections1.find({"Channel_name": user_inp}, {'_id': 0}):
                for i in collections2.find({'Video_id': vid['Video_id']}, {'_id': 0,'Like_count':0, 'Reply_count':0}):
                    mycursor.execute(query2, tuple(i.values()))
                    mydb.commit()


        if st.button("Submit"):
            try:
                insert_into_channels()
                insert_into_playlist()
                insert_into_videos()
                insert_into_comments()
                st.success("Transformation to MySQL Successful !!")
            except:
                st.error("Channel details already transformed !!")

# VIEW PAGE
try:
 if selected == "View":
    st.write("## :orange[Select any question to get Insights]")
    questions = st.selectbox('Questions',
                             ['1. What are the names of all the videos and their corresponding channels?',
                              '2. Which channels have the most number of videos, and how many videos do they have?',
                              '3. What are the top 10 most viewed videos and their respective channels?',
                              '4. How many comments were made on each video, and what are their corresponding video names?',
                              '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
                              '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
                              '7. What is the total number of views for each channel, and what are their corresponding channel names?',
                              '8. What are the names of all the channels that have published videos in the year 2022?',
                              '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
                              '10. Which videos have the highest number of comments, and what are their corresponding channel names?'])

    if questions == '1. What are the names of all the videos and their corresponding channels?':
        mycursor.execute("""SELECT video_name AS Video_Title, channel_name AS Channel_Name
                            FROM video
                            ORDER BY channel_name""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        st.write(df)

    elif questions == '2. Which channels have the most number of videos, and how many videos do they have?':
        mycursor.execute("""SELECT c.channel_name AS Channel_Name, Count(video_name) AS Total_Videos
                            FROM channel AS c
                            JOIN video AS v
                            ON
                            c.channel_name = v.channel_name
                            GROUP BY Channel_Name
                            ORDER BY total_videos DESC
                            LIMIT 1""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        st.write(df)
        st.write("### :green[Number of videos in each channel :]")
        # st.bar_chart(df,x= mycursor.column_names[0],y= mycursor.column_names[1])
        fig = px.bar(df,
                     x=mycursor.column_names[0],
                     y=mycursor.column_names[1],
                     orientation='v',
                     color=mycursor.column_names[0]
                     )
        st.plotly_chart(fig, use_container_width=True)

    elif questions == '3. What are the top 10 most viewed videos and their respective channels?':
        mycursor.execute("""SELECT channel_name AS Channel_Name, video_name AS Video_Title, view_count AS Views 
                            FROM video
                            ORDER BY views DESC
                            LIMIT 10""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        st.write(df)
        st.write("### :green[Top 10 most viewed videos :]")
        fig = px.bar(df,
                     x=mycursor.column_names[2],
                     y=mycursor.column_names[1],
                     orientation='h',
                     color=mycursor.column_names[0]
                     )
        st.plotly_chart(fig, use_container_width=True)

    elif questions == '4. How many comments were made on each video, and what are their corresponding video names?':
        mycursor.execute("""SELECT v.video_name AS Video_Title, b.Total_Comments
                            FROM video AS v
                            LEFT JOIN (SELECT video_id,COUNT(comment_id) AS Total_Comments FROM comment GROUP BY video_id) AS b
                            ON 
                            v.video_id = b.video_id
                            ORDER BY b.Total_Comments DESC""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        st.write(df)

    elif questions == '5. Which videos have the highest number of likes, and what are their corresponding channel names?':
        mycursor.execute("""SELECT channel_name AS Channel_Name, video_name AS Title, like_count AS Likes_Count 
                            FROM video
                            ORDER BY Likes_Count DESC
                            LIMIT 10""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        st.write(df)
        st.write("### :green[Top 10 most liked videos :]")
        fig = px.bar(df,
                     x=mycursor.column_names[2],
                     y=mycursor.column_names[1],
                     orientation='h',
                     color=mycursor.column_names[0]
                     )
        st.plotly_chart(fig, use_container_width=True)

    elif questions == '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
        mycursor.execute("""SELECT video_name AS Title, like_count AS Likes_Count, dislike_count AS Dislikes_Count
                            FROM video
                            ORDER BY like_count DESC""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        st.write(df)

    elif questions == '7. What is the total number of views for each channel, and what are their corresponding channel names?':
        mycursor.execute("""SELECT channel_name AS Channel_Name, SUM(view_count) AS Total_Views
                            FROM video
                            GROUP BY Channel_Name
                            ORDER BY Total_Views DESC""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        st.write(df)
        st.write("### :green[Channels vs Views :]")
        fig = px.bar(df,
                     x=mycursor.column_names[0],
                     y=mycursor.column_names[1],
                     orientation='v',
                     color=mycursor.column_names[0]
                     )
        st.plotly_chart(fig, use_container_width=True)

    elif questions == '8. What are the names of all the channels that have published videos in the year 2022?':
        mycursor.execute("""SELECT channel_name AS Channel_Name
                            FROM video
                            WHERE published_date LIKE '2022%'
                            GROUP BY channel_name
                            ORDER BY channel_name""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        st.write(df)

    elif questions == '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?':
        mycursor.execute("""SELECT channel_name AS Channel_Name,
                            AVG(duration)/60 AS "Average_Video_Duration (mins)"
                            FROM video
                            GROUP BY channel_name
                            ORDER BY AVG(duration)/60 DESC""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        st.write(df)
        st.write("### :green[Avg video duration for channels :]")
        fig = px.bar(df,
                     x=mycursor.column_names[0],
                     y=mycursor.column_names[1],
                     orientation='v',
                     color=mycursor.column_names[0]
                     )
        st.plotly_chart(fig, use_container_width=True)

    elif questions == '10. Which videos have the highest number of comments, and what are their corresponding channel names?':
        mycursor.execute("""SELECT channel_name AS Channel_Name, video_id AS Video_ID, comment_count AS Comments
                            FROM video
                            ORDER BY comments DESC
                            LIMIT 10""")
        df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
        st.write(df)
        st.write("### :green[Videos with most comments :]")
        fig = px.bar(df,
                     x=mycursor.column_names[1],
                     y=mycursor.column_names[2],
                     orientation='v',
                     color=mycursor.column_names[0]
                     )
        st.plotly_chart(fig, use_container_width=True)
except:
        st.write("### There's no MySQL DB exist to process result")



#print(get_channel_details(["UCtY8p96hHhCsKqMMKGDMp7w","UCnV8DtCO0uFndc8DBodTCSA","UCk081mmVz4hzff-3YVBAxow","UCiJKrqlkEha2kj3D9vSUCIg","UCl3pOdJaSEz8fnDwKV8Nbvg","UC7Qjz-AT300K3KRKBb4uiaA"]))
# print(len(get_channel_videos(["UC7Qjz-AT300K3KRKBb4uiaA","UCl3pOdJaSEz8fnDwKV8Nbvg"])))
# print(get_comments_details(get_channel_videos(["UC7Qjz-AT300K3KRKBb4uiaA","UCl3pOdJaSEz8fnDwKV8Nbvg"])))
#print(get_video_details(get_channel_videos(["UC7Qjz-AT300K3KRKBb4uiaA","UCl3pOdJaSEz8fnDwKV8Nbvg"])))
#print(len(get_video_details(get_channel_videos(["UC7Qjz-AT300K3KRKBb4uiaA","UCl3pOdJaSEz8fnDwKV8Nbvg"]))))
#print(get_channel_videos(["UC7Qjz-AT300K3KRKBb4uiaA","UCl3pOdJaSEz8fnDwKV8Nbvg"]))
#out = get_playlist_name(["UC7Qjz-AT300K3KRKBb4uiaA","UCl3pOdJaSEz8fnDwKV8Nbvg"])
#print(out)
#print(len(out))

# print(get_comments_details(get_channel_videos("UCvyZS6W6zMJCZBVzF-Ei6sw")))

#UCtY8p96hHhCsKqMMKGDMp7w,UCnV8DtCO0uFndc8DBodTCSA,UCk081mmVz4hzff-3YVBAxow,UCiJKrqlkEha2kj3D9vSUCIg,UCl3pOdJaSEz8fnDwKV8Nbvg,UC7Qjz-AT300K3KRKBb4uiaA
#UC8LFnF_C2w__jFAx_KdI35A,UCagSy965iDCzdAnZXPgNCJg