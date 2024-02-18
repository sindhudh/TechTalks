import psycopg2

# Create a connection
try:
    connection = psycopg2.connect(
        user="YOURUSERNAME",
        password="YOURUPassward",
        host="YOURHOSTNAME",#This will be bydefault localhost
        port="YOURSERVERPORT",#5432
        database="DBName"
    )

    print("Connected to PostgreSQL")
    #--------------------Create Table-------------
    cursor = connection.cursor()

    create_table_query = "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY,username VARCHAR(50) NOT NULL, email VARCHAR(100) NOT NULL)"

    #print(cursor.execute(create_table_query))
    connection.commit()
    connection.close()
    cursor.close()
    
    print("Table 'users' created successfully")
    #----------------Insert into DB---------------
    insert_query = "INSERT INTO public.users (username, email) VALUES (%s, %s)"
    user_data = ("john_doe", "john.doe@example.com")

    cursor.execute(insert_query, user_data)
    connection.commit()
    print("Data inserted successfully")
    #-----------Querying the Data
    select_query = "SELECT * FROM users"

    cursor.execute(select_query)
    

    
    for row in cursor:
        print(f"ID: {row[0]}, Username: {row[1]}, Email: {row[2]}")
    #-------------Updating-------
    update_query = "UPDATE users SET email = %s WHERE username = %s"
    user_data = ("updated_email@example.com", "john_doe")
    
    cursor.execute(update_query, user_data)
    connection.commit()
    #----Delete --------------
    delete_query = "DELETE FROM users WHERE username = %s"
    user_data = ("john_doe",)

    cursor.execute(delete_query, user_data)
    connection.commit()
except psycopg2.Error as e:
    print(f"Error: {e}")