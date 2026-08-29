from sqlalchemy import text

from database import engine


beds = [
    ("ICU", "ICU-01", "available"),
    ("ICU", "ICU-02", "occupied"),
    ("ICU", "ICU-03", "available"),
    ("General", "GEN-01", "available"),
    ("General", "GEN-02", "occupied"),
    ("Emergency", "ER-01", "occupied"),
    ("Emergency", "ER-02", "available"),
]

equipment = [
    ("MRI", "Radiology Room 1", "operational"),
    ("ECG", "Room 3", "operational"),
    ("CT Scanner", "Radiology Room 2", "maintenance"),
    ("Ventilator", "ICU", "operational"),
    ("X-Ray", "Radiology Room 3", "operational"),
]


with engine.begin() as connection:

    for bed in beds:
        connection.execute(
            text("""
                INSERT INTO beds
                (ward_type, bed_number, status)
                VALUES (:ward_type, :bed_number, :status)
            """),
            {
                "ward_type": bed[0],
                "bed_number": bed[1],
                "status": bed[2]
            }
        )

    for item in equipment:
        connection.execute(
            text("""
                INSERT INTO equipment
                (name, location, status)
                VALUES (:name, :location, :status)
            """),
            {
                "name": item[0],
                "location": item[1],
                "status": item[2]
            }
        )


print("Sample data inserted successfully.")