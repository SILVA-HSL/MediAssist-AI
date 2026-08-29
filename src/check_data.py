from sqlalchemy import text

from database import engine


with engine.connect() as connection:

    print("\n--- BEDS ---")

    result = connection.execute(
        text("SELECT * FROM beds")
    )

    for row in result:
        print(row)


    print("\n--- EQUIPMENT ---")

    result = connection.execute(
        text("SELECT * FROM equipment")
    )

    for row in result:
        print(row)


    print("\n--- MAINTENANCE TICKETS ---")

    result = connection.execute(
        text("SELECT * FROM maintenance_tickets")
    )

    for row in result:
        print(row)