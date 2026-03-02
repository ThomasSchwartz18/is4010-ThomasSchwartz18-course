import json


def save_contacts_to_json(contacts, filename):
    """Save a list of contact dictionaries to a JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)


def load_contacts_from_json(filename):
    """Load contacts from a JSON file, returning an empty list if missing."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


if __name__ == "__main__":
    contacts_file = "contacts.json"
    my_contacts = load_contacts_from_json(contacts_file)
    print(f"Loaded {len(my_contacts)} contact(s).")

    new_contact = {"name": "Charles Babbage", "email": "charles@computers.org"}
    my_contacts.append(new_contact)
    print(f"Added a new contact for {new_contact['name']}.")

    save_contacts_to_json(my_contacts, contacts_file)
    print("Saved contacts to disk.")