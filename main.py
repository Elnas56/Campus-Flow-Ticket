import json

def load_tickets():
    try:
        with open("tickets.json", "r", encoding="utf-8") as file:
            tickets = json.load(file)
            return tickets

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("Error: tickets.json contains invalid JSON.")
        raise SystemExit

    except OSError:
        print("Error: Unable to read tickets.json.")
        raise SystemExit

def save_tickets(tickets):
    try:
        with open("tickets.json", "w", encoding="utf-8") as file:
            json.dump(tickets, file, indent=4)
        
        return True

    except PermissionError:
        print("Permission denied.")
        return False

    except OSError:
        print("Unable to save tickets.")
        return False


def main():
    tickets = load_tickets()

    title = input("Enter ticket title: ")
    description = input("Enter ticket description: ")

    title = title.strip()
    description = description.strip()

    if not title or not description:
        print("Reject the input") 
    else:
        print("Accept the input")

        ticket_id = f"T{len(tickets) + 1:03d}"

        ticket = {
            "id": ticket_id,
            "title": title,
            "description": description
        }

        tickets.append(ticket)        
        saved = save_tickets(tickets)
        print("Save result:", saved)
        if saved:
            print("Ticket created successfully!")

        else:
            print("Ticket creation failed!")

main()

