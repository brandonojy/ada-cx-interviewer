import pandas as pd
import requests
import streamlit as st
from openai import OpenAI
import time
import json
api_key = st.secrets["api_key"]

client = OpenAI(api_key=api_key)
st.header('UX Segments Auto Insurance', divider='blue')

re = requests.get("https://yvpmakjfsvzjewrsskcj.supabase.co/rest/v1/interview_results?apikey=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl2cG1ha2pmc3Z6amV3cnNza2NqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDEzMjc2NjQsImV4cCI6MjAxNjkwMzY2NH0.EiEYbVLrabEun7KHtI_ulF2O88eEqVUSQ5XpjfEjpgE")

prompt = """
You are a analyst who has received interview results done by a customer interviewer on auto insurance. 

Categorise these customers provided to you into 2 - 4 personas. Return the personas together with the interview results below in a single json format. 

The json format should look like { "personas": [ { "name": "Persona Name", "description": "Persona description", "customers": [List of customers provided]}]} 
"""

completion = client.chat.completions.create(
    model="gpt-4o",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": json.dumps(re.json())}
    ]
)

#st.write(json.loads(completion.choices[0].message.content))

for persona in json.loads(completion.choices[0].message.content)["personas"]:
    st.subheader(persona["name"])
    st.caption(persona["description"])
    for customer in persona["customers"]:
        with st.expander(f"{customer['results']['summary']}"):
            interview_df = pd.DataFrame(customer['results']['customer_journey_process'])
            st.text("Customer Joruney")
            st.write(interview_df)
            qna_df = pd.DataFrame(customer['results']['qna'])
            st.text("Interview Questions")
            st.write(qna_df)
