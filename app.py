import streamlit as st
import requests
import pandas as pd
import json

def fix_multiline_strings(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == '@last_seen' and value is None:
                data[key] = 'N/A'
            elif isinstance(value, str) and '\n' in value:
                data[key] = value.replace('\n', ' ')
            elif isinstance(value, (dict, list)):
                fix_multiline_strings(value)
    elif isinstance(data, list):
        for item in data:
            fix_multiline_strings(item)

def beautify_json(json_data):  # Modify this function to accept JSON data directly
    fix_multiline_strings(json_data)
    
    return json_data

headers = {
        'traceparent': '00-ee262cb3b6da441bbb683d8871074331-ece35bcbab0f4d47-00',
        'newrelic': 'eyJ2IjpbMCwyXSwiZCI6eyJ0eSI6Ik1vYmlsZSIsImFjIjoiMTIxNzEwMSIsImFwIjoiMTM4NTk1MjMwMSIsInRyIjoiZWUyNjJjYjNiNmRhNDQxYmJiNjgzZDg4NzEwNzQzMzEiLCJpZCI6ImVjZTM1YmNiYWIwZjRkNDciLCJ0aSI6MTcxMTkzNjgyNjY1MiwidGsiOiIxMjE3MTAxIn19',
        'tracestate': '1217101@nr=0-2-1217101-1385952301-ece35bcbab0f4d47----1711936826652',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjA1MmQ5OTBlMzYzNWU3NjI1MWM5ZDkzYmQyOGZiZjJjMmE0ZWU2Yjg3OGYyZDQ4YjNiYWNjZGQ2ZGIzMGVkMjgwYzRkNmU0NDA2MTRjYjVkIn0.eyJhdWQiOiIxIiwianRpIjoiMDUyZDk5MGUzNjM1ZTc2MjUxYzlkOTNiZDI4ZmJmMmMyYTRlZTZiODc4ZjJkNDhiM2JhY2NkZDZkYjMwZWQyODBjNGQ2ZTQ0MDYxNGNiNWQiLCJpYXQiOjE3MTE5MzY3NjgsIm5iZiI6MTcxMTkzNjc2OCwiZXhwIjoxNzQzNDcyNzY4LCJzdWIiOiIzNDM0MzcyNDYiLCJzY29wZXMiOltdfQ.MjlfvMDnXn3vygDOCjuBcpyhtWgzXPONsiMzKrPGiFuREWUY2OU6uDwtD5ZtFF1eSUDZHjbcseipnZhIWfjm6u04_vUvKItuzGVJmbGPyUswScasGADHujIgQAbzwC1YDAHRIRH_QUn4zDpv3JJppnAFwFO0rk3OphUOxQOPq4tGXbX01rGl1IkrnCPJjNKd1lgQ-gUMYULp6PrAFQRiFSxtBUxqglJdTOfKd8viUyeClYeUuw2ls6TQUxc6tJgUwu-z_K7g7l_PT6JIykBzEqV0WHNWq4p3Wpara6AvaPjr2kK4lCHms6PP_3WEbfHgd_zpOdW5L_juMyWluUn54uR5Gi7CWlYs8WxOYkU3GTkQK-HkQ6mAr2mU_wCUHlHJgs0PFnd0eJbaRuAcuIXbZdTT9nklZmtTDrvJrgGfjVyjWpar2eESvVS53IAdeOmOXkpKQWBA2H8uoIa8Nie2x0qp1LOyOzWY3-nty8e_lZ915ZuGITg5DCmYP4h6yi5F70RtbjtW71MnUcVH2AOQ5K7cOkRTqSCy36EvEkV8KZ9bACtsKZTUS3NNDen2Rb8cUUk-pilJ-YEv4kPhW_O1_hyzwX2nc2yOxCLU3_r-_poWPZVC_p0xn_BSAzbrg0Bs5VhyvYc2Amv9YdadqMYCnagWrFua25Y8PowUT9BvseI',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/5.0.0-alpha.2',
        'X-NewRelic-ID': 'VQQGVldTCRABV1lXDgQFVVQA',
    }

def search_by_phone(phonenumber):
    url = 'https://api.whoapp.us/api/mobile/search/v2/by-phone?phone=' + phonenumber
    response = requests.get(url, headers=headers)
    return response

def search_by_fullname(fullname):
    url = 'https://api.whoapp.us/api/mobile/search/v2/by-name?raw_name=' + fullname
    response = requests.get(url, headers=headers)
    return response

def main():
    st.set_page_config(
        layout="wide",
        page_title="Infotrace v1.0",
        page_icon=":sunglasses:",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/atiilla/infotrace',
            'Report a bug': "https://github.com/atiilla/infotrace/issues",
            'About': "Infotrace v1.0"
        } 
    )

    # Hide the Streamlit footer
    st.markdown(
        """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title("Infotrace v1.0")
    st.markdown("""
    Search by phone number or fullname.\n
    Warning: I'm not responsible for any misuse of this service.
""")
    

    tab = st.sidebar.radio("Navigation", ["Search by Fullname", "Search by Phone Number"])

    if tab == "Search by Fullname":
        fullname = st.text_input("Enter Fullname")
        if st.button("Search Now"):
            # Call search function by fullname
            st.write("Search results by Fullname")
            response = search_by_fullname(fullname)
            # Display results as table
            if response.status_code == 200:
                # data = response.json()
                # st.write(data)  # You can format the data as a table
                
                    # Parse JSON
                data = beautify_json(response.json())
                
                # Extract persons data
                persons = data.get('persons', [])
         
                # Prepare data for DataFrame
                rows = []

                

                for obj in persons:
                    last_seen = 'N/A'
                    phones = obj.get('phones', [])
                    print(len(phones))
                    if len(phones) > 0:
                        last_seen = phones[0].get('@last_seen', 'N/A')
                    names = obj.get('names', [])
                    addresses = obj.get('addresses', [])
                    jobs = obj.get('jobs', [])
                    educations = obj.get('educations', [])
                    languages = obj.get('languages', [])

                    row = {
                            'Phone': phones[0]['_hidden_phone_mapper'] if phones else 'No Data',
                            'Last Seen': last_seen,
                            'Name': names[0]['display'] if names else 'No Data',
                            'Country': addresses[0]['country_en'] if addresses else 'No Data',
                            'City': addresses[0]['city_en'] if addresses else 'No Data',
                            'Jobs': ', '.join([f"{job['title']} at {job['display']}" for job in jobs]) if jobs else 'No Data',
                            'Education': ', '.join([f"{edu['school']}" for edu in educations]) if educations else 'No Data',
                            'Languages': ', '.join([lang['display'] for lang in languages]) if languages else 'No Data'
                        }
                    rows.append(row)
                # Create DataFrame
                df = pd.DataFrame(rows)

                st.table(df)


            else:
                st.write("Error:", response.status_code)

    elif tab == "Search by Phone Number":
        phonenumber = st.text_input("Enter Phone Number")
        if st.button("Search Now"):
            # Call search function by phone number
            st.write("Search results by Phone Number")
            response = search_by_phone(phonenumber)
            # Display results as table
            if response.status_code == 200:
                data = response.json()
                st.write(data)  # You can format the data as a table
            else:
                st.write("Error:", response.status_code)

        

if __name__ == "__main__":
    main()
