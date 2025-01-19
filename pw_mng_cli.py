import manager as password_manager


# CLI for Scenario 1: Vault exists
def cli_scenario_1():
    # Step 1: Check if the vault exists
    if password_manager.exists_vault():
        print("Vault exists, please authenticate.")

        # Step 2: Authenticate
        vault_name = input("Enter the vault name: ")
        password = input("Enter your master password: ")

        # Step 3: Authenticate user and retrieve encryption key salt
        encryption_key_salt = password_manager.authenticate(vault_name, password)

        if encryption_key_salt:
            print("Authentication successful.")
            action = input("Do you want to (1) view all passwords or (2) create a new password entry? (Enter 1 or 2): ")

            if action == "1":
                # Step 4: View all passwords
                password_manager.retrieve_all_passwords(password, vault_name)
            elif action == "2":
                # Step 5: Create a new password entry
                what_for = input("What is this password for? (e.g., email, social media, etc.): ")
                new_password = input("Enter the new password to store: ")
                uname = input("Enter the username (optional): ")
                em_addr = input("Enter the email address (optional): ")
                password_manager.create_password(vault_name, password, what_for, new_password, uname, em_addr)
        else:
            print("Authentication failed. Please check your credentials.")
    else:
        print("Vault does not exist. Please create a vault first.")
        create_new_vault()


# Create a new vault if one doesn't exist
def create_new_vault():
    vault_name = input("Enter a name for your new vault: ")
    new_password = password_manager.create_vault(vault_name)
    print(f"Vault created successfully. Your new vault password is: {new_password}. Please keep it safe!")


def cli_main_menu():
    while True:
        print("\nWelcome to your Password Manager CLI!")
        print("1. Login to an existing vault")
        print("2. Create a new vault")
        print("3. Exit")

        choice = input("Please choose an option (1, 2, 3): ")

        if choice == "1":
            # Scenario 1: Vault exists
            vault_name = input("Enter the vault name: ")
            password = input("Enter the vault password: ")
            if password_manager.authenticate(vault_name, password):
                print(f"Logged in successfully to {vault_name}")
                cli_vault_operations(vault_name, password)
            else:
                print("Authentication failed. Please try again.")

        elif choice == "2":
            # Scenario 2: Vault does not exist
            print("No vault found. Let's create a new vault.")
            vault_name = input("Enter a name for your new vault: ")
            new_password = password_manager.create_vault(vault_name)
            print(f"Vault created successfully. Your new vault password is: {new_password}. Please keep it safe!")
            cli_vault_operations(vault_name, new_password)

        elif choice == "3":
            print("Goodbye!")
            break  # Exit the loop and end the application
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def cli_vault_operations(vault_name, master_password):
    while True:
        print(f"\nVault Operations for {vault_name}:")
        print("1. View all stored passwords")
        print("2. Add a new password")
        print("3. Log out of the vault")

        choice = input("Choose an operation (1, 2, 3): ")

        if choice == "1":
            # View all stored passwords
            password_manager.retrieve_all_passwords(master_password, vault_name)

        elif choice == "2":
            # Add a new password entry
            what_for = input("What is this password for? (e.g., email, social media, etc.): ")
            new_password = input("Enter the new password to store: ")
            uname = input("Enter the username (optional): ")
            em_addr = input("Enter the email address (optional): ")
            password_manager.create_password(vault_name, master_password, what_for, new_password, uname, em_addr)

        elif choice == "3":
            print(f"Logging out of {vault_name}...")
            break  # Exit the vault operations loop and go back to the main menu

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


cli_main_menu()

