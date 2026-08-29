from sqlalchemy import text

from database import engine


with open("schema.sql", "r", encoding="utf-8") as file:
    schema = file.read()


with engine.begin() as connection:
    connection.execute(text(schema))


print("Tables created successfully.")