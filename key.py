from sqlalchemy import URL

# Create the connection string
connection_string = URL.create(
    "postgresql+asyncpg",
    username="postgres",  # Replace with your actual username
    password="@T25r5s540",  # Replace with your actual password
    host="localhost",  # Replace with your actual host
    database="assignment",  # Replace with your actual database name
)

# Print the connection string for debugging
print("Connection String:", connection_string)