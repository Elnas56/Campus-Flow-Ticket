import uuid

title = input("Enter ticket title: ")
description = input("Enter ticket description: ")

if not title.strip() or not description.strip():
    print("Input is invalid")
else:
    print("Input is valid")    

    ticket_id = str(uuid.uuid4())
    ticket = {
        "id": ticket_id,
        "title": title,
        "description": description
    }
    print(ticket)

tickets = [
    {"id": "T001", "title": "Network Issues"},
    {"id": "T002", "title": "Keyboard Fault"}
]