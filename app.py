import pyrebase 
import streamlit as st
from datetime import datetime


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
auth = firebase.auth()

# Database

db = firebase.database()
storage = firebase.storage()
st.sidebar.title('Dash Data')
# Authentication
choice = st.sidebar.selectbox('login/Signup', ['Login', 'Sign up'])

# Obtain User Input for email and password
email = st.sidebar.text_input('Please enter your email address')
password = st.sidebar.text_input('Please enter your password',type = 'password')

# App 

# Sign up Block
if choice == 'Sign up':
    handle = st.sidebar.text_input(
        'Please input your app handle name', value='Default')
    submit = st.sidebar.button('Create my account')

    if submit:
        user = auth.create_user_with_email_and_password(email, password)
        st.success('Your account is created suceesfully!')
        st.snow()
        # Sign in
        user = auth.sign_in_with_email_and_password(email, password)
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("ID").set(user['localId'])
        st.title('Welcome ' + handle)
        st.info('Login Created Successfully! ')

# Login Block
if choice == 'Login':
    login = st.sidebar.button('Login')
    if login:
        user = auth.sign_in_with_email_and_password(email,password)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        bio = st.radio('Select',['Home','Consultas & Pacentes', 'Settings'])
        
        
# Get the inputs
paciente = st.text_input('Paciente')
idade = st.number_input('Idade')
ultima_consulta = st.date_input('Ultima Consulta')
tipo_consulta = st.selectbox('Tipo de Consulta',
                            ['Consulta Geral', 'Consulta Especializada', 'Exame'])
valor_consulta = st.number_input('Valor da Consulta')
status_paciente = st.selectbox('Status do Paciente',
                              ['Ativo', 'Inativo', 'Aguardando'])

# Create a submit button
submit_button = st.button('Enviar')

# Create a delete button
delete_button = st.button('Deletar')

# Create a dataframe to store the data
data = {'Paciente': [paciente], 'Idade': [idade],
        'Ultima Consulta': [ultima_consulta],
        'Tipo de Consulta': [tipo_consulta],
        'Valor da Consulta': [valor_consulta],
        'Status Paciente': [status_paciente]}



# Store the data in Firebase
if st.button("Submit"):
    data = {
        'paciente': paciente,
        'idade': idade,
        'ultima_consulta': str(ultima_consulta),
        'tipo_consulta': tipo_consulta,
        'valor_consulta': valor_consulta,
        'status_paciente': status_paciente
    }
    ref.push(data)
    st.success("Data stored in Firebase")

# Check if the submit button is clicked
if submit_button:
    # Save the data to Firebase
    db.push('https://bi---datascience-default-rtdb.firebaseio.com/').push(data)
    st.success('Data Consulta salva com sucesso!')


# Display the data in a dashboard
st.subheader("Data Consulta Dashboard")
all_data = ref.get()
if all_data:
    df = pd.DataFrame(all_data)
    st.dataframe(df.T)