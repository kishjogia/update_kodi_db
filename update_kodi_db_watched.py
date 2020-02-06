# ToDo
# [x] 1. Connect to a Kodi MySQL DB
# [x] 2. Get the correct id for the path
# [x] 3. Increase the playCount of files
# [x] 4. Have the db information in a file
# [ ] 5. Connect to remote Kodi MySQL DB

import mysql.connector

# Config moved to options file
#config = {
#    'user': 'kodi_admin',
#    'password': 'kodi_admin',
#    'database': 'MyVideos116',
#    'host': '192.168.1.199'
#}
mysql_option_file = 'mysql_config.cnf'      # mysql options file, assume it is in the same directory
movie_path = '/Multimedia/Movies/'          # path of the Moives that have been watched

def connect_database():
#    connection = mysql.connector.connect(**config)          # connect to the DB usinf parameters in config
    connection = mysql.connector.connect(option_files=mysql_option_file)

    if connection:
        print ('DB connection open')
    else:
        print ('Failed to connect to DB')

    return connection

def close_database(db_connection):
    db_connection.close()                       # close connection to DB

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

            sql_str = "SELECT idFile, playCount FROM files WHERE idPath = " + str(path_id)
            cursor.execute(sql_str)
            blocks = cursor.fetchall()

            # Increment the playCount of films matching this path
            for block in blocks:
                film_id = block[0]
                if block[1] == None:
                    film_playCount = 1
                else:
                    film_playCount = block[1] + 1

                # Update the playCount for all files
                sql_str = "UPDATE files SET playCount = " + str(film_playCount) + " WHERE idFile = " + str(film_id)
                cursor.execute(sql_str)

            # Appling changes to DB
            db_connection.commit()

    cursor.close()

    return

#********
# Main
#********

cnx = connect_database()

update_played_count(cnx)

close_database(cnx)