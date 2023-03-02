# Modules
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# credentials to connect to firebase
cred = credentials.Certificate('https://bi---datascience-default-rtdb.firebaseio.com/')


# get the root reference
root = db.reference()

# get the data reference
data_ref = root.child('Data Consulta')

# Create a webapp
st.title('Data Consulta')

# get the user inputs
paciente = st.text_input('Paciente')
idade = st.number_input('Idade')
ultima_consulta = st.date_input('Ultima Consulta')
tipo_consulta = st.selectbox('Tipo de Consulta', ['Clinica', 'Laboratorial'])
valor_consulta = st.number_input('Valor da Consulta')
status_paciente = st.selectbox('Status Paciente', ['Ativo', 'Inativo'])

# store the data into firebase
if st.button('Confirmar'):
    data_ref.push({
        'Paciente': paciente,
        'Idade': idade,
        'Ultima Consulta': ultima_consulta,
        'Tipo de Consulta': tipo_consulta,
        'Valor da Consulta': valor_consulta,
        'Status Paciente': status_paciente
    })
    st.balloons()

# display the dashboard
st.subheader('Dashboard')
data = data_ref.get()

if data:
    df = pd.DataFrame.from_dict(data, orient='index')
    st.dataframe(df)