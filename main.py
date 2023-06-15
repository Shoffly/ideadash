# Imports
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build


#google sheet connection
SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials= None

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1eHy6zAqeMuJp3T2CJ5PYssfMLsDTJyEnr_cFTpy3byM'

service = build('sheets', 'v4', credentials=credentials)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="A2:h12163").execute()
values = result.get('values', [])

print(values)

# Convert the array of arrays to a pandas DataFrame
df = pd.DataFrame(values, columns=['Date','Name','Department','Category','Recommendation','picture'])


# Category Side selection
cat_select = df['Category'].unique()
cat = st.sidebar.selectbox("Pick an idea category", cat_select)



#page contents
st.title(f"{cat} | Ideas forum")
st.write(f'''
''')

# Dataframe filtered for the idea category
fil_df = df[((df['Category'].isin([cat])))]

# Number of ideas submitted
st.metric(label="Number of submissions",value= fil_df['Category'].count(), delta="Ideas")


# Assume 'df' is your DataFrame
for index, row in fil_df.iterrows():
    # Access row data using column names or indices
    #Acess the date
    date = row['Date']
    dept = row['Department']
    idea = row['Recommendation']
    pl = row['picture']
    # Create the callout message
    callout_message = f"Date: {date}\n\nRecommendation:\n\n{idea}\n\nDepartment: {dept}\n\nPicture: {pl}"


    # Display the callout using st.info()
    st.info(callout_message)