import sqlite3

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