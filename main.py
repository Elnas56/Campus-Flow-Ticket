
import json
import os

from google import genai
from openai import OpenAI
from huggingface_hub import InferenceClient


def get_api_key(provider):
    api_keys = {
        "Gemini": "GEMINI_API_KEY",
        "OpenAI": "OPENAI_API_KEY",
        "OpenRouter": "OPENROUTER_API_KEY",
        "Hugging Face": "HF_TOKEN"
    }

    if provider not in api_keys:
        print("Unsupported AI provider.")
        return None

    api_key_name = api_keys[provider]
    api_key = os.getenv(api_key_name)

    if not api_key:
        print(f"{provider} key is not configured.")
        return None

    return api_key


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


def analyze_ticket(description, provider):

    api_key = get_api_key(provider)

    if not api_key:
        print("AI analysis is currently unavailable.")
        return

    prompt = f"""
    Analyze this technical problem:

    {description}

    Provide:
    1. Possible causes.
    2. Troubleshooting steps.
    3. Recommended investigation.
    """

    try:

        if provider == "Gemini":

            client = genai.Client(
                api_key=api_key,
                http_options={"timeout": 120000}
            )

            interaction = client.interactions.create(
                model="gemini-3.5-flash-lite",
                input=prompt
            )

            result = interaction.output_text

        elif provider == "OpenAI":

            client = OpenAI(api_key=api_key)

            response = client.chat.completions.create(
                model="gpt-5.5",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            result = response.choices[0].message.content

        elif provider == "OpenRouter":

            client = OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1"
            )

            response = client.chat.completions.create(
                model="openai/gpt-5.5",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            result = response.choices[0].message.content

        elif provider == "Hugging Face":

            client = InferenceClient(
                api_key=api_key
            )

            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            result = response.choices[0].message.content

        else:
            print("Unsupported AI provider.")
            return

        print("\nAI Ticket Analysis:")
        print(result)

    except Exception as error:
        print("AI analysis failed:", type(error).__name__)
        print("Error details:", str(error))


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

            ai_providers = (
                "Gemini",
                "OpenAI",
                "OpenRouter",
                "Hugging Face"
            )

            print("\nChoose an AI provider:")

            for index, name in enumerate(ai_providers, start=1):
                print(f"{index}. {name}")

            try:
                choice = int(input("Enter your choice (1-4): "))

                if 1 <= choice <= 4:

                    provider = ai_providers[choice - 1]

                    print(f"\nSelected provider: {provider}")

                    analyze_ticket(
                        ticket["description"],
                        provider
                    )

                else:
                    print(
                        "Invalid choice. Please select between 1 and 4."
                    )

            except ValueError:
                print("Invalid input. Please enter a number.")

        else:
            print("Ticket creation failed!")


if __name__ == "__main__":
    main()
