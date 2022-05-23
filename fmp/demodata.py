from posixpath import lexists
import streamlit as st
import pandas as pd
import numpy as np
import random
import faker

fake = faker.Faker()

states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

def random_state():
    return random.choice(states)

def random_serial_number():
    y = str(random.randint(2000, 2022))
    m = str(random.randint(1, 12)).zfill(2)
    s = str(random.randint(1, 10000)).zfill(5)
    return "{y}{m}{s}".format(y=y, m=m, s=s)

def new_owner(row):
    row['namefirst'] = fake.first_name()
    row['namelast'] = fake.last_name()
    row = new_address(row)
    return row

def new_address(row):
    row['address'] = fake.street_address()
    row['state'] = random_state()
    row['postcode'] = fake.postcode()
    row['city'] = fake.city()
    return row

def new_sn(row):
    row['sn'] = random_serial_number()
    return row

def new_owner_new_address(row):
    row = new_owner(row)
    row = new_address(row)
    return row

#same owner, new address = new_address
#same owner, same address = new_sn
#new owner, new address
actions = [new_address, new_owner_new_address] + [new_sn]*3

def make(num_rows=100, as_df=True):
    row = new_address({'product': 'eFlex'})
    row = new_owner(row)
    row = new_sn(row)

    rows = [row]
    for _ in range(num_rows):
        row = rows[-1].copy()
        row = new_sn(row)
        action = random.choice(actions)
        rows.append(action(row))
    if as_df:
        return pd.DataFrame(rows)
    else:
        return rows

def search_df(df, search_text):
    if not search_text:
        return df
    for col in df.columns:
        mask = np.column_stack([df[col].str.contains("(?i){}".format(search_text), regex=True) for col in df])

    return df.loc[mask.any(axis=1)]    


@st.cache
def get_map_df(address):
    return pd.DataFrame(
         np.random.randn(1, 2) / [20,20] + [40.039422, -75.321275],
         columns=['lat', 'lon'])

def extract_address(pdf, grid_response):
    data = grid_response['data']
    selected = grid_response['selected_rows']

    active_address = pdf.address
    if selected:
        active_address = selected[0]['address']
    return active_address

@st.cache
def get_site_data(site_id):
    soc = np.random.randn(200) + 85
    voltage = np.random.randn(200) + 50
    amps = np.random.randn(200) * 10
    chast = np.random.randint(0, 6, size=200)
    faults = np.random.randint(0, 20, size=200)
    return soc, voltage, amps, chast, faults        

def search_df_for_row(df, row):
    '''
    where row is a dictionary of {column_name: desired value}
    '''

    mask = (df[list(row)]== pd.Series(row)).all(axis=1)
    return df.loc[mask]

if __name__=='__main__':
    df = make(5)
    print(df)
    addy = df.drop_duplicates(subset=['address', 'state', 'postcode', 'city'])
    addy.drop('sn', axis=1, inplace=True)
    print(addy)

    records = df.to_dict('records')
    row = {}
    row['address'] = records[0]['address']
    row['state'] = records[0]['state']
    print(search_df_for_row(df, row))

    print(row)