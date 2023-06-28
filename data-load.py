import requests
import configparser
import psycopg2
from datetime import datetime


def api_cotd_load(length, start_offset, end_offset):
    length = length
    offset = start_offset

    cotd = []

    try:
        headers = {'user-agent': 'cotd-data-analysis/0.0.1'}

        while(offset < end_offset):
            URL = f'https://competition.trackmania.nadeo.club/api/competitions?length={length}&offset={offset}'
            print(URL)

            r = requests.get(URL, headers=headers)
            print(r.status_code)
            if(r.status_code != 200):
                raise Exception(f'''Status code not OK:200
                                    Status code = {r.status_code}
                                    Offset = {offset}
                                ''')

            for i in r.json():
                if( (i['name'].startswith('COTD') or i['name'].startswith('Cup of the Day'))
                    and ( i['name'].find('#2') == -1 and i['name'].find('#3') == -1 )
                    and ( i['partition'] == 'crossplay' ) 
                    ):
                    cotd.append([i['id'], '\''+i['liveId']+'\'', '\''+i['creator']+'\'', '\''+i['name']+'\'', '\''+i['participantType']+'\'', 
                                 '\''+str(datetime.fromtimestamp(i['startDate']))+'\'', i['startDate'], '\''+str(datetime.fromtimestamp(i['endDate']))+'\'', i['endDate'], 
                                 i['matchesGenerationDate'], i['nbPlayers'], i['leaderboardId'], '\''+i['partition']+'\''])
            
            offset = offset + length

    except (Exception) as error:
        print(error)

    return cotd
        
    



def insert_to_database(tablename, columns, values):
    config = configparser.ConfigParser()
    config.read('config.txt')

    DATABASE = config['Database']['database']
    HOST = config['Database']['host']
    PORT = config['Database']['port']
    USER = config['Database']['user']
    PWD = config['Database']['pwd']

    columns = '(' + ', '.join(columns) + ')'

    valTemp = []
    for i in values:
        valTemp.append('(' + ', '.join(str(j) for j in i) + ')')
    values = ',\n'.join(valTemp)

    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            database=DATABASE, 
            host=HOST,
            port=PORT,
            user=USER,
            password=PWD)
        
        cur = conn.cursor()

        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)

        sql = f'''INSERT INTO {tablename}
                    {columns}
                    VALUES
                    {values}
                '''
        print(sql)
        cur.execute(sql)

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close
            print('Database connection closed.')


cotd = api_cotd_load(25, 0, 100)
columns = ['competition_id', 'liveid', 'creator', 'competition_name', 'participanttype', 'startdate', 'starttimestamp', 'enddate', 'endtimestamp', 'matchesgenerationdate', 'nbplayers', 'leaderboardid', 'partition']
insert_to_database('competitions', columns, cotd)