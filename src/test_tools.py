from tools.hospital_tools import (get_available_beds, get_equipment_status,create_maintenance_ticket)


# beds = get_available_beds("ICU")

# print("Available ICU beds:")
# print(beds)
#================================================

# print("ICU:")
# print(get_available_beds("ICU"))

# print("\nGeneral:")
# print(get_available_beds("General"))

# print("\nEmergency:")
# print(get_available_beds("Emergency"))

#================================================

print("Available ICU beds:")
print(
    get_available_beds.invoke({
        "ward_type": "ICU"
    })
)


print("\nMRI status:")
print(
    get_equipment_status.invoke({
        "equipment_name": "MRI"
    })
)

print("\nCT Scanner status:")
print(
    get_equipment_status.invoke({
        "equipment_name": "CT Scanner"
    })
)

print("\nECG status:")
print(
    get_equipment_status.invoke({
        "equipment_name": "ECG"
    })
)

print("\nUltrasound status:")
print(
    get_equipment_status.invoke({
        "equipment_name": "Ultrasound"
    })
)

result = create_maintenance_ticket.invoke({
    "equipment_name": "ECG",
    "location": "Room 3",
    "issue": "Machine is not working"
})

print("\nMaintenance ticket:")
print(result)