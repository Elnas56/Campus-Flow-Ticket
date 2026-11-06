import json
import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not configured.")

client = genai.Client(
    api_key=api_key
)

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

def analyze_ticket(description):
    prompt = f"""
    You are a campus IT support assistant.

    Analyze this technical problem:
    {description}

    Provide:
    1. Possible causes.
    2. Recommended troubleshooting steps.
    3. Further investigation if the problem persists.
    """
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )
    print(interaction.output_text)

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
            analyze_ticket(ticket["description"])

        else:
            print("Ticket creation failed!")

main()

