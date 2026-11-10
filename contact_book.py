import json
import os
import re

# File where contact data is stored
DATA_FILE = "contacts.json"


def load_contacts():
    """Load contacts from the JSON file. Return an empty dictionary if missing or broken."""
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            # Ensure the top-level structure is a dictionary
            if isinstance(data, dict):
                return data
            return {}
    except (json.JSONDecodeError, OSError):
        print("\nWarning: Could not read contacts file (it might be corrupted). Starting fresh.")
        return {}


def save_contacts(contacts):
    """Save the contacts dictionary back to the JSON file."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(contacts, f, indent=4)
    except OSError as e:
        print(f"\nError saving contacts to disk: {e}")


def is_valid_phone(phone):
    """Validate phone: allows optional '+' and digits, must be 7-15 digits."""
    clean_digits = re.sub(r"\D", "", phone)
    return 7 <= len(clean_digits) <= 15


def is_valid_email(email):
    """Validate email with a basic pattern check."""
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


def get_valid_input(prompt, validator, error_msg):
    """Repeatedly ask user for input until it passes the validator function."""
    while True:
        value = input(prompt).strip()
        if validator(value):
            return value
        print(f"Error: {error_msg}")


def add_contact(contacts):
    """Add a new contact to the directory."""
    print("\n--- Add New Contact ---")
    name = input("Enter contact name: ").strip()
    if not name:
        print("Name cannot be empty. Returning to menu.")
        return

    # Check for existing contact
    if name.lower() in [k.lower() for k in contacts]:
        print(f"A contact named '{name}' already exists! Use the update option instead.")
        return

    phone = get_valid_input(
        "Enter phone number (7-15 digits): ",
        is_valid_phone,
        "Please enter a valid phone number (digits only, 7 to 15 numbers)."
    )

    email = get_valid_input(
        "Enter email address: ",
        is_valid_email,
        "Please enter a valid email address (e.g., student@example.com)."
    )

    contacts[name] = {"phone": phone, "email": email}
    save_contacts(contacts)
    print(f"Success: '{name}' added to contacts!")


def view_all_contacts(contacts):
    """Display all contacts in a formatted table."""
    print("\n--- All Contacts ---")
    if not contacts:
        print("No contacts found. Your contact book is empty.")
        return

    print(f"{'Name':<22} | {'Phone':<18} | {'Email':<30}")
    print("-" * 75)
    for name, details in sorted(contacts.items()):
        print(f"{name:<22} | {details.get('phone', 'N/A'):<18} | {details.get('email', 'N/A'):<30}")


def search_contact(contacts):
    """Search for contacts by partial name matching."""
    print("\n--- Search Contact ---")
    query = input("Enter name to search: ").strip().lower()
    if not query:
        print("Search query cannot be empty.")
        return

    matches = {name: info for name, info in contacts.items() if query in name.lower()}

    if not matches:
        print(f"No contacts matching '{query}'.")
        return

    print(f"\nFound {len(matches)} match(es):")
    for name, details in matches.items():
        print(f"- {name}: Phone: {details['phone']}, Email: {details['email']}")


def update_contact(contacts):
    """Update phone number, email, or both for an existing contact."""
    print("\n--- Update Contact ---")
    name_to_find = input("Enter the exact name of the contact to update: ").strip()

    # Case-insensitive search for existing key
    exact_key = None
    for name in contacts:
        if name.lower() == name_to_find.lower():
            exact_key = name
            break

    if not exact_key:
        print(f"Contact '{name_to_find}' not found.")
        return

    current = contacts[exact_key]
    print(f"Updating '{exact_key}'. (Press Enter to keep current value)")

    # Update Phone
    new_phone = input(f"New phone [{current['phone']}]: ").strip()
    if new_phone:
        while not is_valid_phone(new_phone):
            print("Invalid phone format.")
            new_phone = input(f"New phone [{current['phone']}]: ").strip()
            if not new_phone:
                break
        if new_phone:
            current['phone'] = new_phone

    # Update Email
    new_email = input(f"New email [{current['email']}]: ").strip()
    if new_email:
        while not is_valid_email(new_email):
            print("Invalid email format.")
            new_email = input(f"New email [{current['email']}]: ").strip()
            if not new_email:
                break
        if new_email:
            current['email'] = new_email

    save_contacts(contacts)
    print(f"Success: Updated '{exact_key}'.")


def delete_contact(contacts):
    """Delete a contact with confirmation."""
    print("\n--- Delete Contact ---")
    name_to_find = input("Enter the name of the contact to delete: ").strip()

    exact_key = None
    for name in contacts:
        if name.lower() == name_to_find.lower():
            exact_key = name
            break

    if not exact_key:
        print(f"Contact '{name_to_find}' not found.")
        return

    confirm = input(f"Are you sure you want to delete '{exact_key}'? (y/n): ").strip().lower()
    if confirm == "y":
        del contacts[exact_key]
        save_contacts(contacts)
        print(f"Deleted '{exact_key}' successfully.")
    else:
        print("Deletion canceled.")


def main():
    """Main program loop."""
    contacts = load_contacts()

    while True:
        print("\n==============================")
        print("         CONTACT BOOK         ")
        print("==============================")
        print("1. View All Contacts")
        print("2. Add Contact")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            view_all_contacts(contacts)
        elif choice == "2":
            add_contact(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            update_contact(contacts)
        elif choice == "5":
            delete_contact(contacts)
        elif choice == "6":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()