from sqlalchemy import text
from langchain_core.tools import tool

from database import engine


# def get_available_beds(ward_type: str):
#     query = text("""
#         SELECT bed_number
#         FROM beds
#         WHERE ward_type = :ward_type
#         AND status = 'available'
#         ORDER BY bed_number
#     """)

#     with engine.connect() as connection:
#         result = connection.execute(
#             query,
#             {"ward_type": ward_type}
#         )

#         beds = [row[0] for row in result]

#     return beds

#==================================================

# def get_available_beds(ward_type: str):

#     query = text("""
#         SELECT bed_number
#         FROM beds
#         WHERE ward_type = :ward_type
#         AND status = 'available'
#         ORDER BY bed_number
#     """)

#     with engine.connect() as connection:
#         result = connection.execute(
#             query,
#             {"ward_type": ward_type}
#         )

#         beds = [row[0] for row in result]

#     return {
#         "ward_type": ward_type,
#         "available_count": len(beds),
#         "beds": beds
#     }

#==================================================

@tool
def get_available_beds(ward_type: str):
    """
    Check the number and list of available hospital beds
    for a specific ward type such as ICU, General, or Emergency.
    """

    query = text("""
        SELECT bed_number
        FROM beds
        WHERE ward_type = :ward_type
        AND status = 'available'
        ORDER BY bed_number
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"ward_type": ward_type}
        )

        beds = [row[0] for row in result]

    return {
        "ward_type": ward_type,
        "available_count": len(beds),
        "beds": beds
    }

@tool
def get_equipment_status(equipment_name: str):
    """
    Check the current status and location of a specific hospital
    equipment such as MRI, ECG, CT Scanner, Ventilator, or X-Ray.
    """

    query = text("""
        SELECT name, location, status
        FROM equipment
        WHERE LOWER(name) = LOWER(:equipment_name)
        LIMIT 1
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"equipment_name": equipment_name}
        )

        row = result.fetchone()

    if not row:
        return {
            "found": False,
            "equipment": equipment_name,
            "message": f"No equipment found with the name '{equipment_name}'."
        }

    return {
        "found": True,
        "equipment": row.name,
        "location": row.location,
        "status": row.status
    }


@tool
def create_maintenance_ticket(
    equipment_name: str,
    location: str,
    issue: str
):
    """
    Create a maintenance ticket for hospital equipment that
    requires repair or inspection.
    """

    query = text("""
        INSERT INTO maintenance_tickets
        (equipment_name, location, issue, status)
        VALUES (:equipment_name, :location, :issue, 'open')
        RETURNING id, equipment_name, location, issue, status, created_at
    """)

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {
                "equipment_name": equipment_name,
                "location": location,
                "issue": issue
            }
        )

        row = result.fetchone()

    return {
        "success": True,
        "ticket_id": row.id,
        "equipment": row.equipment_name,
        "location": row.location,
        "issue": row.issue,
        "status": row.status,
        "created_at": str(row.created_at)
    }