import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT into primes (num, prime) VALUES (?,?)",
            (1, 2))
cur.execute("INSERT into primes (num, prime) VALUES (?,?)",
            (2, 3))
cur.execute("INSERT into primes (num, prime) VALUES (?,?)",
            (3, 5))

connection.commit()
connection.close()