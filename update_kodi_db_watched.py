# ToDo
# [x] 1. Connect to Kodi MySQL DB
# [x] 2. Get the correct id for the path
# [ ] 3. Increase the playCount of files

import mysql.connector

config = {
    'user': 'kodi',
    'password': 'kodi',
    'database': 'MyVideos116',
    'host': '127.0.0.1'
}
movie_path = '/Multimedia/Movies/'

def connect_database():
    connection = mysql.connector.connect(**config)          # connect to the DB usinf parameters in config

    print ('DB connection opened to ', config['database'], '@', config['host'])

    return connection

def close_database(db_connection):
    db_connection.close()

    return

def update_played_count(db_connection):
    cursor = db_connection.cursor(buffered = True)
    # Get the id for the correct path that needs to have the values updated
    sql_str = "SELECT idPath, strPath FROM path WHERE strPath LIKE '%" + movie_path + "%'"
    cursor.execute(sql_str)
    rows = cursor.fetchall()
    
    if len(rows) != 1:
        print ('There are multiple IDs for this path: ' + movie_path)
        print ('Rename the directory and rebuild the library')
    else:
        for row in rows:
            path_id = row[0]

            # Update the playCount for all files in the right directory to 1
            sql_str = "UPDATE files SET playCount = 1 WHERE idPath = " + str(path_id)
            cursor.execute(sql_str)
            db_connection.commit()

    cursor.close()

    return

#********
# Main
#********

cnx = connect_database()

update_played_count(cnx)

close_database(cnx)