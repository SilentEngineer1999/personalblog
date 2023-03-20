import psycopg2 as sql

con = sql.connect(
    database="test", user='ajays', 
  password='9110870379@Ab', host='localhost', port='5432'
)

#Create a Connection
cur = con.cursor()

#Drop users table if already exsist.
cur.execute("DROP TABLE IF EXISTS content;")
cur.execute("DROP TABLE IF EXISTS users;")


# #Create users table  in db_web database
sql = '''CREATE TABLE users (
	id BIGSERIAL UNIQUE PRIMARY KEY,
	UNAME VARCHAR(50) NOT NULL,
	email VARCHAR(50) NOT NULL,
    phone_number VARCHAR(10) NOT NULL,
	date_of_birth DATE NOT NULL,
    password VARCHAR(200) NOT NULL
);'''

content = '''CREATE TABLE content(
			UNAME VARCHAR(50) NOT NULL,
            email VARCHAR(50) NOT NULL,
            title VARCHAR(50) NOT NULL,
            date DATE NOT NULL,
            text VARCHAR
            );
		'''

cur.execute(sql)
cur.execute(content)

#commit changes
con.commit()

#close the connection
con.close()
print("db closed")