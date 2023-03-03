import streamlit as st
import firebase_admin
from firebase_admin import db
import pyrebase
import pandas as pd
import math
import json
import pandas as pd
from firebase_admin import credentials, firestore, storage, auth

# Config Key

firebaseConfig = {
  "apiKey": "AIzaSyAmBXxP5Pic-zKNINznE1xoJ7_lKU1g5LI",
  "authDomain": "bi---datascience.firebaseapp.com",
  "databaseURL": "https://bi---datascience-default-rtdb.firebaseio.com/",
  "projectId": "bi---datascience",
  "storageBucket": "bi---datascience.appspot.com",
  "messagingSenderId": "400644886094",
  "appId": "1:400644886094:web:5ce1a183051c64983efd1f",
  "measurementId": "G-PPRBG91BF0"
};

# Firebase Auth

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
data_ref = db.child('data')

st.title('CADASTRO DE PACIENTE')

with st.form(key='include_paciente'):
    input_name = st.text_input('Insira o nome do Paciente')
    input_age = st.number_input("Insira Idade")
    input_1date = st.date_input('Data Primeira Consulta')
    input_Udate = st.date_input('Data Ultima Consulta')
    tipo_consulta = st.selectbox('Tipo de Consulta',
                            ['Anamnse', 'Retorno', 'Ação de MKT'])
    input_status = st.selectbox('Selecione o Status do Paciente',
                            ['Ativo','Inativo'])
    input_valor = st.number_input('Digite o Valor da Consulta')
    input_plano = st.selectbox('Plano',
                            ['Plano Mensal', 'Plano Trimestral', 'Plano Semestral'])
    input_button_submit = st.form_submit_button('Submit')
      

if input_button_submit: 
    data_ref.push({
        'Nome Paciente': input_name,
        'Idade Paciente': input_age,
        'Data da Primeira Consulta': str(input_1date),
        'Data da Ultima Consulta': str(input_Udate),
        'Valor da Consulta': input_valor,
        'Tipo da Consulta': tipo_consulta,
        'Tipo de Plano': input_plano,
        'Status Paciente': input_status
    })
    st.success('Dados Salvos com Sucesso')


data_ = data_ref.get()


# Dataframe

if st.checkbox('Mostrar Dataframe'):
    st.markdown('## Dashboard')
    st.dataframe(data_.val())


# Filter Paciente data
if st.checkbox('Filtro de Pacientes'):
  filter_name = st.text_input('Insira o Nome do Paciente')
  for data in data_.each():
    if data.val()["Nome Paciente"] == filter_name:
      data_ref.child(data.key()).remove()
      st.table(data.val())

      
    
  



  







