import os
import json
import streamlit as st
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError
import base64
import pandas as pd

def load_env_file(file_path=".env"):
    """
    Simple parser to load environment variables from a .env file.
    """
    try:
        with open(file_path, "r") as env_file:
            for line in env_file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()
    except FileNotFoundError:
        st.error(f"No {file_path} file found. Make sure it exists in the current directory.")

# Load the .env file to set the environment variables
load_env_file()

# Retrieve AWS credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

def show_pdf(file_obj):
    """
    Display the PDF file in an iframe using base64 encoding.
    """
    file_obj.seek(0)
    base64_pdf = base64.b64encode(file_obj.read()).decode('utf-8')
    pdf_display = f'''
        <iframe src="data:application/pdf;base64,{base64_pdf}" 
                width="700" height="1000" type="application/pdf">
        </iframe>
    '''
    st.markdown(pdf_display, unsafe_allow_html=True)

def show_csv(file_obj):
    """
    Display the CSV file as a DataFrame in Streamlit.
    """
    file_obj.seek(0)
    df = pd.read_csv(file_obj)
    st.dataframe(df)

def upload_to_s3(file_obj, bucket_name, s3_file_name):
    """
    Upload a file-like object to S3 using boto3.
    """
    s3 = boto3.client(
        's3',
        region_name=AWS_DEFAULT_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    try:
        file_obj.seek(0)
        s3.upload_fileobj(file_obj, bucket_name, s3_file_name)
        st.success("Upload to S3 successful!")
        return True
    except (BotoCoreError, NoCredentialsError) as e:
        st.error(f"Upload failed: {str(e)}")
        return False

def call_lambda_function():
    """
    Call the AWS Lambda function 'myFn' and return its result.
    """
    lambda_client = boto3.client(
        'lambda',
        region_name=AWS_DEFAULT_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    payload = {}
    try:
        response = lambda_client.invoke(
            FunctionName='myFn',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        response_payload = response['Payload'].read().decode('utf-8')
        try:
            result = json.loads(response_payload)
        except json.JSONDecodeError:
            result = response_payload
        st.success("Lambda function call successful!")
        return result
    except Exception as e:
        st.error(f"Lambda function call failed: {e}")
        return None

# --- Streamlit App Layout ---
st.title("File Uploader & Lambda Caller with Streamlit")

# File uploader widget (accepts both PDF and CSV files)
uploaded_file = st.file_uploader("Upload a file (PDF or CSV)", type=["pdf", "csv"])

if uploaded_file is not None:
    st.write("Filename:", uploaded_file.name)
    
    if uploaded_file.name.endswith(".pdf"):
        show_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".csv"):
        show_csv(uploaded_file)
    
    # S3 configuration
    bucket_name = "veolia-data"  # Replace with your actual bucket name
    s3_file_name = uploaded_file.name    

    # Button to trigger the S3 upload
    if st.button("Upload to S3"):
        success = upload_to_s3(uploaded_file, bucket_name, s3_file_name)
        if success:
            st.write(f"File uploaded to s3://{bucket_name}/{s3_file_name}")
