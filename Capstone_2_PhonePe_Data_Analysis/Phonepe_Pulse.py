import os
import git
import json
import pandas as pd
import warnings
import requests
import subprocess
from subprocess import Popen, PIPE, STDOUT
import sqlalchemy
from sqlalchemy import create_engine
import mysql.connector as sql
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import numpy as np


warnings.filterwarnings('ignore')

os.chdir(r"C:/Users/vinti/PycharmProjects/pythonProject/Phonepe_Pulse_Capstone2/Dataset_raw/")

url = "https://github.com/PhonePe/pulse.git"  # Target clone repo address

proc = Popen(
    ["git", "clone", "--progress", url],
    stdout=PIPE, stderr=STDOUT, shell=True, text=True
)

for line in proc.stdout:
    if line:
        print(line.strip())  # Now you get all terminal clone output text



path_1 = "C:/Users/vinti/PycharmProjects/pythonProject/Phonepe_Pulse_Capstone2/Dataset_raw/pulse/data/aggregated/transaction/country/india/state/"
Agg_trans_state_list = os.listdir(path_1)
Agg_trans = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [],
             'Transaction_amount': []}


for i in Agg_trans_state_list:
    state_wise = path_1 + i + "/"
    Agg_state_list = os.listdir(state_wise)

    for j in Agg_state_list:
        year_wise = state_wise + j + "/"
        Agg_year_list = os.listdir(year_wise)

        for k in Agg_year_list:
            json_file_wise = year_wise + k
            Data = open(json_file_wise, 'r')
            file_list_1 = json.load(Data)

            for l in file_list_1['data']['transactionData']:
                Name = l['name']
                count = l['paymentInstruments'][0]['count']
                amount = l['paymentInstruments'][0]['amount']
                Agg_trans['State'].append(i)
                Agg_trans['Year'].append(j)
                Agg_trans['Quarter'].append(int(k.strip('.json')))
                Agg_trans['Transaction_type'].append(Name)
                Agg_trans['Transaction_count'].append(count)
                Agg_trans['Transaction_amount'].append(amount)

df_aggregated_transaction = pd.DataFrame(Agg_trans)


path_2 = "C:/Users/vinti/PycharmProjects/pythonProject/Phonepe_Pulse_Capstone2/Dataset_raw/pulse/data/aggregated/user/country/india/state/"
Agg_user_state_list = os.listdir(path_2)
Agg_user = {'State': [], 'Year': [], 'Quarter': [], 'Mobile_Brands': [], 'User_Count': [],
             'User_Percentage': []}

for i in Agg_user_state_list:
    state_wise = path_2 + i + "/"
    Agg_state_list = os.listdir(state_wise)


    for j in Agg_state_list:
        year_wise = state_wise + j + "/"
        Agg_year_list = os.listdir(year_wise)


        for k in Agg_year_list:
            json_file_wise = year_wise + k
            Data = open(json_file_wise, 'r')
            file_list_2 = json.load(Data)


            try:
                for l in file_list_2["data"]["usersByDevice"]:
                    if file_list_2["data"]["usersByDevice"]:
                        brand_name = l["brand"]
                        count_ = l["count"]
                        ALL_percentage = l["percentage"]
                        Agg_user["State"].append(i)
                        Agg_user["Year"].append(j)
                        Agg_user["Quarter"].append(int(k.strip('.json')))
                        Agg_user["Mobile_Brands"].append(brand_name)
                        Agg_user["User_Count"].append(count_)
                        Agg_user["User_Percentage"].append(ALL_percentage * 100)
            except:
                pass

df_aggregated_user = pd.DataFrame(Agg_user)


path_3 = "C:/Users/vinti/PycharmProjects/pythonProject/Phonepe_Pulse_Capstone2/Dataset_raw/pulse/data/map/transaction/hover/country/india/state/"
Map_trans_state_list = os.listdir(path_3)

Map_trans = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Transaction_Count': [], 'Transaction_Amount': []}

for i in Map_trans_state_list:
    state_wise = path_3 + i + "/"
    Map_state_list = os.listdir(state_wise)

    for j in Map_state_list:
        year_wise = state_wise + j + "/"
        Map_year_list = os.listdir(year_wise)

        for k in Map_year_list:
            json_file_wise = year_wise + k
            Data = open(json_file_wise, 'r')
            file_list_3 = json.load(Data)

            for l in file_list_3["data"]["hoverDataList"]:
                District = l["name"]
                count = l["metric"][0]["count"]
                amount = l["metric"][0]["amount"]
                Map_trans['State'].append(i)
                Map_trans['Year'].append(j)
                Map_trans['Quarter'].append(int(k.strip('.json')))
                Map_trans["District"].append(District)
                Map_trans["Transaction_Count"].append(count)
                Map_trans["Transaction_Amount"].append(amount)

df_map_transaction = pd.DataFrame(Map_trans)


path_4 = "C:/Users/vinti/PycharmProjects/pythonProject/Phonepe_Pulse_Capstone2/Dataset_raw/pulse/data/map/user/hover/country/india/state/"
Map_user_state_list = os.listdir(path_4)

Map_user = {"State": [], "Year": [], "Quarter": [], "District": [], "Registered_User": []}

for i in Map_user_state_list:
    state_wise = path_4 + i + "/"
    Map_state_wise_year_list = os.listdir(state_wise)

    for j in Map_state_wise_year_list:
        year_wise = state_wise + j + "/"
        Map_year_wise_file_list = os.listdir(year_wise)


        for k in Map_year_wise_file_list:
            json_file_wise = year_wise + k
            Data = open(json_file_wise, 'r')
            file_list_4 = json.load(Data)

            for l in file_list_4["data"]["hoverData"].items():
                district = l[0]
                registereduser = l[1]["registeredUsers"]
                Map_user['State'].append(i)
                Map_user['Year'].append(j)
                Map_user['Quarter'].append(int(k.strip('.json')))
                Map_user["District"].append(district)
                Map_user["Registered_User"].append(registereduser)

df_map_user = pd.DataFrame(Map_user)


path_5 = "C:/Users/vinti/PycharmProjects/pythonProject/Phonepe_Pulse_Capstone2/Dataset_raw/pulse/data/top/transaction/country/india/state/"
Top_trans_state_list = os.listdir(path_5)

Top_trans = {'State': [], 'Year': [], 'Quarter': [], 'District_Pincode': [], 'Transaction_count': [],
             'Transaction_amount': []}

for i in Top_trans_state_list:
    state_wise = path_5 + i + "/"
    Top_state_wise_year_list = os.listdir(state_wise)

    for j in Top_state_wise_year_list:
        year_wise = state_wise + j + "/"
        Top_year_wise_file_list = os.listdir(year_wise)

        for k in Top_year_wise_file_list:
            json_file_wise = year_wise + k
            Data = open(json_file_wise, 'r')
            file_list_5 = json.load(Data)

            for l in file_list_5['data']['pincodes']:
                Name = l['entityName']
                count = l['metric']['count']
                amount = l['metric']['amount']
                Top_trans['State'].append(i)
                Top_trans['Year'].append(j)
                Top_trans['Quarter'].append(int(k.strip('.json')))
                Top_trans['District_Pincode'].append(Name)
                Top_trans['Transaction_count'].append(count)
                Top_trans['Transaction_amount'].append(amount)

df_top_transaction = pd.DataFrame(Top_trans)


path_6 = "C:/Users/vinti/PycharmProjects/pythonProject/Phonepe_Pulse_Capstone2/Dataset_raw/pulse/data/top/user/country/india/state/"
Top_user_state_list = os.listdir(path_6)

Top_user = {'State': [], 'Year': [], 'Quarter': [], 'District_Pincode': [], 'Registered_User': []}

for i in Top_user_state_list:
    state_wise = path_6 + i + "/"
    Top_state_wise_year_list = os.listdir(state_wise)

    for j in Top_state_wise_year_list:
        year_wise = state_wise + j + "/"
        Top_year_wise_file_list = os.listdir(year_wise)

        for k in Top_year_wise_file_list:
            json_file_wise = year_wise + k
            Data = open(json_file_wise, 'r')
            file_list_6 = json.load(Data)

            for l in file_list_6['data']['pincodes']:
                Name = l['name']
                registeredUser = l['registeredUsers']
                Top_user['State'].append(i)
                Top_user['Year'].append(j)
                Top_user['Quarter'].append(int(k.strip('.json')))
                Top_user['District_Pincode'].append(Name)
                Top_user['Registered_User'].append(registeredUser)

df_top_user = pd.DataFrame(Top_user)


# Connect to the MySQL server
mydb = sql.connect(
  host = "localhost",
  user = "root",
  password = "root"
)

# Create a new database and use
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS phonepe_pulse")

# Close the cursor and database connection
mycursor.close()
mydb.close()

# Connect to the new created database
engine = create_engine('mysql+mysqlconnector://root:root@localhost/phonepe_pulse', echo=False)

# 1
df_aggregated_transaction.to_sql('aggregated_transaction', engine, if_exists = 'replace', index=False,
                                 dtype={'State': sqlalchemy.types.VARCHAR(length=50),
                                       'Year': sqlalchemy.types.Integer,
                                       'Quarter': sqlalchemy.types.Integer,
                                       'Transaction_type': sqlalchemy.types.VARCHAR(length=50),
                                       'Transaction_count': sqlalchemy.types.Integer,
                                       'Transaction_amount': sqlalchemy.types.FLOAT(precision=5, asdecimal=True)})

# 2
df_aggregated_user.to_sql('aggregated_user', engine, if_exists = 'replace', index=False,
                          dtype={'State': sqlalchemy.types.VARCHAR(length=50),
                                 'Year': sqlalchemy.types.Integer,
                                 'Quarter': sqlalchemy.types.Integer,
                                 'Brands': sqlalchemy.types.VARCHAR(length=50),
                                 'User_Count': sqlalchemy.types.Integer,
                                 'User_Percentage': sqlalchemy.types.FLOAT(precision=5, asdecimal=True)})
# 3
df_map_transaction.to_sql('map_transaction', engine, if_exists = 'replace', index=False,
                          dtype={'State': sqlalchemy.types.VARCHAR(length=50),
                                 'Year': sqlalchemy.types.Integer,
                                 'Quarter': sqlalchemy.types.Integer,
                                 'District': sqlalchemy.types.VARCHAR(length=50),
                                 'Transaction_Count': sqlalchemy.types.Integer,
                                 'Transaction_Amount': sqlalchemy.types.FLOAT(precision=5, asdecimal=True)})
# 4
df_map_user.to_sql('map_user', engine, if_exists = 'replace', index=False,
                   dtype={'State': sqlalchemy.types.VARCHAR(length=50),
                          'Year': sqlalchemy.types.Integer,
                          'Quarter': sqlalchemy.types.Integer,
                          'District': sqlalchemy.types.VARCHAR(length=50),
                          'Registered_User': sqlalchemy.types.Integer, })
# 5
df_top_transaction.to_sql('top_transaction', engine, if_exists = 'replace', index=False,
                         dtype={'State': sqlalchemy.types.VARCHAR(length=50),
                                'Year': sqlalchemy.types.Integer,
                                'Quarter': sqlalchemy.types.Integer,
                                'District_Pincode': sqlalchemy.types.Integer,
                                'Transaction_count': sqlalchemy.types.Integer,
                                'Transaction_amount': sqlalchemy.types.FLOAT(precision=5, asdecimal=True)})
# 6
df_top_user.to_sql('top_user', engine, if_exists = 'replace', index=False,
                   dtype={'State': sqlalchemy.types.VARCHAR(length=50),
                          'Year': sqlalchemy.types.Integer,
                          'Quarter': sqlalchemy.types.Integer,
                          'District_Pincode': sqlalchemy.types.Integer,
                          'Registered_User': sqlalchemy.types.Integer})

