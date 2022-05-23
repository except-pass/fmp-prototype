import pandas as pd

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
    row = new_address({})
    row = new_owner(row)
    row = new_sn(row)

    rows = [row]
    for _ in range(num_rows):
        row = rows[-1].copy()
        print(row)        
        row = new_sn(row)
        action = random.choice(actions)
        rows.append(action(row))
    if as_df:
        return pd.DataFrame(rows)
    else:
        return rows

if __name__ == '__main__':
    from pprint import pprint
    print(make(10))