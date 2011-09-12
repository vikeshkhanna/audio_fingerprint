#!/usr/bin/python
import MySQLdb


conn = MySQLdb.connect (host = "localhost",
                        user = "root",
                        passwd = "rishabh",
                        db = "btp")


cursor = conn.cursor ()
cursor.execute ("DROP TABLE IF EXISTS animal")
cursor.execute ("""
    CREATE TABLE animal
    (
      name     CHAR(40),
      category CHAR(40)
    )
  """)
cursor.execute ("""
    INSERT INTO animal (name, category)
    VALUES
      ('snake', 'reptile'),
      ('frog', 'amphibian'),
      ('tuna', 'fish'),
      ('racoon', 'mammal')
  """)
print "Number of rows inserted: %d" % cursor.rowcount


print "Content-Type: text/html"
print
print "Hello, world"
