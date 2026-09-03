import sqlite3

# This file is used to initialize a clean database. Running this file will delete all previously saved/modified data
# and reset the database to its initial state.
if __name__ == "__main__":
    conn = sqlite3.connect('Challenge_DB.db')
    cursor = conn.cursor()

    fd = open("initial_data.sql", 'r')
    sqlFile = fd.read()
    fd.close()

    sqlCommands = sqlFile.split(';')

    for command in sqlCommands:
        cursor.execute(command)

    conn.commit()
    cursor.close()
    conn.close()