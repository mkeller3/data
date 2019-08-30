accounts = [
    {
        'account_id': 123456789,
        'venue_guests': 150, 
        'venue_date': '2020-08-14',
        'venue_name': 'Hoosier Grove Barn',
        'venue_address': '700 W Irving Park Rd, Streamwood, IL 60107',
        'venue_latitude': 42.018771,
        'venue_longitude': -88.195320,
        'contacts': [
            {
                'id': 1,
                'account_id': 123456789,
                'full_name': 'Tyler',
                'phone': 7082759904
            },{
                'id': 2,
                'account_id': 123456789,
                'full_name': 'Bob',
                'phone': 7082759904
            },{
                'id': 3,
                'account_id': 123456789,
                'full_name': 'Larry',
                'phone': 7082759904
            },{
                'id': 4,
                'account_id': 123456789,
                'full_name': 'Matt',
                'phone': 7082759904
            },
        ],
        'groups':[
            {
                'id': 1,
                'account_id': 123456789,
                'group_name': 'Best Friends',
                'contacts':[1,2,3],
            },{
                'id': 2,
                'account_id': 123456789,
                'group_name': 'Colleagues',
                'contacts':[4,5]
            }
        ],
        'scheduled_texts':[
            {
                'id': 1,
                'account_id': 123456789,
                'text_message': 'Test message',
                'group_message': True,
                'group_id': 1,
                'run_time': '2019-08-19 10:28',
            },{
                'id': 2,
                'account_id': 123456789,
                'text_message': 'Test message 2',
                'group_message': False,
                'group_id': '',
                'run_time': '2019-08-19 10:28',
            }
        ]
    }
]

# for account in accounts:
#     for contact in account['contacts']:
#         print(contact)

# for account in accounts:
#     for message in account['scheduled_texts']:
#         if message['group_message'] == True:
#             print('Group')
#         elif message['group_message'] == False:
#             print('Text Everyone')


import psycopg2
from psycopg2.extras import RealDictCursor
import string
import random
import datetime
databaseHost = 'localhost'
databaseName = 'texting_service'
databaseUser = 'postgres'
databasePassword = 'P0stgr3sadmin'



def id_generator(size=50, chars=string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

def createAccount(venue_date,venue_name,venue_address,venue_latitude,venue_longitude):

    #Database Connection
    conn = psycopg2.connect(f"host={databaseHost} dbname={databaseName} user={databaseUser} password={databasePassword}")
    cur = conn.cursor(cursor_factory=RealDictCursor)

  
    # Create account in database
    cur.execute("INSERT INTO accounts (account_id, venue_date, venue_name, venue_address, venue_latitude, venue_longitude, created_on) VALUES (%s, %s, %s, %s, %s, %s, now());",
    (id_generator(), venue_date, venue_name, venue_address, venue_latitude, venue_longitude))

    # Close connections
    conn.commit()
    cur.close()
    conn.close()

def deleteAccount(account_id):

    # Database Connection
    conn = psycopg2.connect(f"host={databaseHost} dbname={databaseName} user={databaseUser} password={databasePassword}")
    cur = conn.cursor(cursor_factory=RealDictCursor)

  
    # Delete account in database
    cur.execute("DELETE FROM accounts WHERE account_id = %s;", (account_id,))

    # Delete contacts in database
    cur.execute("DELETE FROM contacts WHERE account_id = %s;", (account_id,))

    # Delete groups in database
    cur.execute("DELETE FROM groups WHERE account_id = %s;", (account_id,))

    # Delete text_messages in database
    cur.execute("DELETE FROM scheduled_texts WHERE account_id = %s;", (account_id,))

    # Close connections
    conn.commit()
    cur.close()
    conn.close()

def updateAccount(account_id,venue_date,venue_name,venue_address,venue_latitude,venue_longitude):

    # Database Connection
    conn = psycopg2.connect(f"host={databaseHost} dbname={databaseName} user={databaseUser} password={databasePassword}")
    cur = conn.cursor(cursor_factory=RealDictCursor)

  
    # Update account in database
    cur.execute("UPDATE accounts SET venue_date = %s, venue_name = %s, venue_address = %s, venue_latitude = %s, venue_longitude = %s WHERE account_id = %s;",
    (venue_date, venue_name, venue_address, venue_latitude, venue_longitude, account_id))

    # Close connections
    conn.commit()
    cur.close()
    conn.close()

def createContact(account_id,first_name,last_name,phone_number):
    full_name = first_name+' '+last_name,
    # Database Connection
    conn = psycopg2.connect(f"host={databaseHost} dbname={databaseName} user={databaseUser} password={databasePassword}")
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Create contact in database
    cur.execute("INSERT INTO contacts (account_id, first_name, last_name, full_name, phone_number) VALUES (%s, %s, %s, %s, %s);",
    (account_id, first_name, last_name, full_name, phone_number))

    # Close connections
    conn.commit()
    cur.close()
    conn.close()

def updateContact(unique_id,first_name,last_name,phone_number):

    # Database Connection
    conn = psycopg2.connect(f"host={databaseHost} dbname={databaseName} user={databaseUser} password={databasePassword}")
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Update contact in database
    cur.execute("UPDATE contacts SET first_name = %s, last_name = %s, full_name = %s, phone_number = %d WHERE id = %d;",
    (first_name, last_name, first_name+' '+last_name, phone_number, unique_id))

    # Close connections
    conn.commit()
    cur.close()
    conn.close()

def deleteContact(unique_id):

    # Database Connection
    conn = psycopg2.connect(f"host={databaseHost} dbname={databaseName} user={databaseUser} password={databasePassword}")
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Get account id
    cur.execute("SELECT account_id FROM contacts WHERE id = %s;", (unique_id,))
    account_id = cur.fetchone()

    # Grab all groups with user about to be deleted
    cur.execute("SELECT id, group_name, contacts FROM groups WHERE account_id = %s;", (account_id['account_id'],))
    groups_contacts = cur.fetchall()

    # Loop through groups to see if user is in group and update to remove
    for group in groups_contacts:
        contact_array = group['contacts'].split(',')
        if str(unique_id) in group['contacts']:
            contact_array.remove(str(unique_id))
            updated_contacts = ','.join(contact_array)
            updateGroup(group['id'],group['group_name'],updated_contacts)

    
    # Delete contact in database
    cur.execute("DELETE FROM contacts WHERE id = %s;", (unique_id,))

    # Close connections
    conn.commit()
    cur.close()
    conn.close()

def createGroup(account_id,group_name,contacts):

    # Database Connection
    conn = psycopg2.connect(f"host={databaseHost} dbname={databaseName} user={databaseUser} password={databasePassword}")
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Create group in database
    cur.execute("INSERT INTO groups (account_id, group_name, contacts) VALUES (%s, %s, %s);",
    (account_id, group_name, contacts))

    # Close connections
    conn.commit()
    cur.close()
    conn.close()

def updateGroup(unique_id,group_name,contacts):

    # Database Connection
    conn = psycopg2.connect(f"host={databaseHost} dbname={databaseName} user={databaseUser} password={databasePassword}")
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Update group in database
    cur.execute("UPDATE groups SET group_name = %s, contacts = %s WHERE id = %s;",
    (group_name, contacts, unique_id))

    # Close connections
    conn.commit()
    cur.close()
    conn.close()

def deleteGroup(unique_id):

    # Database Connection
    conn = psycopg2.connect(f"host={databaseHost} dbname={databaseName} user={databaseUser} password={databasePassword}")
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Delete group in database
    cur.execute("DELETE FROM groups WHERE id = %s;", (unique_id,))

    # Delete text_messages in database linked to group
    cur.execute("DELETE FROM scheduled_texts WHERE group_id = %s;", (str(unique_id),))

    # Close connections
    conn.commit()
    cur.close()
    conn.close()

def createTextMessage(account_id,text_message,group_message,group_ids,run_time):

    # Database Connection
    conn = psycopg2.connect(f"host={databaseHost} dbname={databaseName} user={databaseUser} password={databasePassword}")
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Create text_message in database
    cur.execute("INSERT INTO scheduled_texts (account_id, text_message, group_message, group_ids, run_time) VALUES (%s, %s, %s, %s, %s);",
    (account_id, text_message, group_message, group_ids, run_time))

    # Close connections
    conn.commit()
    cur.close()
    conn.close()

def updateTextMessage(unique_id,text_message,group_message,group_ids,run_time):

    # Database Connection
    conn = psycopg2.connect(f"host={databaseHost} dbname={databaseName} user={databaseUser} password={databasePassword}")
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Update text_message in database
    cur.execute("UPDATE scheduled_texts SET text_message = %s, group_message = %s, group_ids = %s, run_time = %s WHERE id = %s;",
    (text_message, group_message, group_ids, run_time, unique_id))

    # Close connections
    conn.commit()
    cur.close()
    conn.close()

def deleteTextMessage(unique_id):

    # Database Connection
    conn = psycopg2.connect(f"host={databaseHost} dbname={databaseName} user={databaseUser} password={databasePassword}")
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Delete text_message in database
    cur.execute("DELETE FROM scheduled_texts WHERE id = %s;", (unique_id,))

    # Close connections
    conn.commit()
    cur.close()
    conn.close()

current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M")

def sendScheduledTextMessages():
    # Database Connection
    conn = psycopg2.connect(f"host={databaseHost} dbname={databaseName} user={databaseUser} password={databasePassword}")
    cur = conn.cursor(cursor_factory=RealDictCursor)

    formatted_time = '2019-09-29 11:28:00'

    # Get account id
    cur.execute("SELECT * FROM scheduled_texts WHERE run_time = %s;", (formatted_time,))
    scheduled_texts = cur.fetchall()

    for text in scheduled_texts:
        if text['group_message'] == False:
            cur.execute("SELECT * FROM contacts WHERE account_id = %s;", (text['account_id'],))
            contacts = cur.fetchall()
            for contact in contacts:
                print('All Message')
        elif text['group_message'] == True:
            groups = text['group_ids'].split(',')
            for group in groups:
                cur.execute("SELECT contacts FROM groups WHERE id = %s;", (group,))
                contacts = cur.fetchone()
                contact_array = contacts['contacts'].split(',')
                contact_array = "','".join(contact_array)
                cur.execute("SELECT * FROM contacts WHERE id IN  ('"+contact_array+"');")
                contacts = cur.fetchall()
                for contact in contacts:
                    print('Group Text')







# createAccount('2019-09-06 16:00','Hoosier Grove Barn','700 W Irving Park Rd, Streamwood, IL 60107',42.018771,-88.195320)
# createContact('vwdyuwydswpdstbjrojjsgwicrnirtfovhhebtjxivhwffsiji','Michael','Keller',7082759904)
# createContact('vwdyuwydswpdstbjrojjsgwicrnirtfovhhebtjxivhwffsiji','Bob','Keller',7082759904)
# createContact('vwdyuwydswpdstbjrojjsgwicrnirtfovhhebtjxivhwffsiji','Marry','Matthews',8154547145)
# createContact('vwdyuwydswpdstbjrojjsgwicrnirtfovhhebtjxivhwffsiji','Larry','Chuck',6304521458)
# createContact('vwdyuwydswpdstbjrojjsgwicrnirtfovhhebtjxivhwffsiji','Sally','Mayes',3125452145)
# createContact('vwdyuwydswpdstbjrojjsgwicrnirtfovhhebtjxivhwffsiji','Charles','Buck',7085248951)
# createGroup('vwdyuwydswpdstbjrojjsgwicrnirtfovhhebtjxivhwffsiji','Sample Group','1,3,5')
# createTextMessage('vwdyuwydswpdstbjrojjsgwicrnirtfovhhebtjxivhwffsiji','Sample Group Text',True,4,'2019-09-29 11:28')
# createTextMessage('vwdyuwydswpdstbjrojjsgwicrnirtfovhhebtjxivhwffsiji','Sample All Text',False,'','2019-09-29 11:28')
# updateAccount('vwdyuwydswpdstbjrojjsgwicrnirtfovhhebtjxivhwffsiji','2019-09-06 17:00','Hoosier Grove Barn','700 W Irving Park Rd, Streamwood, IL 60107',42.018771,-88.195320)
# updateTextMessage(4,'We are now updated',False,'','2019-09-29 11:28')
# updateGroup(4,'Sample Group','22,23')
# deleteContact(21)
# deleteTextMessage(6)
# deleteGroup(3)
# deleteAccount('vwdyuwydswpdstbjrojjsgwicrnirtfovhhebtjxivhwffsiji')

sendScheduledTextMessages()

