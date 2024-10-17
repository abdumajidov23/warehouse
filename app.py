import json
import os

def load_storages(file_name='storage.json'):
    if os.path.exists(file_name):
        try:
            with open(file_name, 'r') as file:
                storages = json.load(file)
                for storage in storages:
                    if 'products' not in storage:
                        storage['products'] = []
                return storages
        except json.JSONDecodeError:
            print("Error: There was a problem reading the JSON file.")
            return []
    return []

storages = load_storages()

def add_storage():
    name = input("Enter the name of the new storage: ")
    length = float(input("Enter the length of the storage (meters): "))
    width = float(input("Enter the width of the storage (meters): "))
    height = float(input("Enter the height of the storage (meters): "))
    
    storage_volume = length * width * height
    
    storage = {
        "name": name,
        "length": length,
        "width": width,
        "height": height,
        "volume": storage_volume,
        "products": []
    }
    
    storages.append(storage)
    
    with open('storage.json', 'w') as file:
        json.dump(storages, file, indent=4)
    
    print(f"{name} storage has been added.")

def view_storages():
    if storages:
        print("Storages:")
        for index, storage in enumerate(storages):
            remaining_space = storage['volume']
            print(f"{index + 1}. Name: {storage['name']}, Volume: {storage['volume']} cubic meters, Remaining space: {remaining_space} cubic meters")
    else:
        print("No storages currently available.")

def delete_storage():
    if not storages:
        print("No storages currently available.")
        return
    
    view_storages()
    
    try:
        choice = int(input("Which storage would you like to delete (enter the number): "))
        if 1 <= choice <= len(storages):
            storage_name = storages[choice - 1]['name']
            storages.pop(choice - 1)
            
            with open('storage.json', 'w') as file:
                json.dump(storages, file, indent=4)
                
            print(f"{storage_name} storage has been deleted.")
        else:
            print("Invalid storage selected.")
    except ValueError:
        print("Invalid number entered. Please enter a number.")

def add_product():
    while True:
        product_name = input("Enter the product name: ")

        print("\nStorages:")
        for index, storage in enumerate(storages):
            print(f"{index + 1}. {storage['name']}")

        try:
            choice = int(input("Which storage would you like to place the product in (enter the number): "))
            
            if 1 <= choice <= len(storages):
                selected_storage = storages[choice - 1]
            else:
                print("Invalid storage selected.")
                return
        except ValueError:
            print("Invalid number entered. Please enter a number.")
            continue

        while True:
            try:
                load_length = float(input(f"Enter the load length for {product_name} (meters): "))
                load_width = float(input(f"Enter the load width for {product_name} (meters): "))
                load_height = float(input(f"Enter the load height for {product_name} (meters): "))
                break
            except ValueError:
                print("Invalid value entered. Please enter a number.")

        load_volume = load_length * load_width * load_height
        
        if load_volume > selected_storage['volume']:
            print(f"Not enough space for {product_name}!")
            return

        selected_storage['volume'] -= load_volume
        
        product = {
            "name": product_name,
            "length": load_length,
            "width": load_width,
            "height": load_height,
            "volume": load_volume
        }
        
        selected_storage['products'].append(product)
        
        with open('storage.json', 'w') as file:
            json.dump(storages, file, indent=4)
        
        print(f"{product_name} has been added to {selected_storage['name']} storage.")
        
        add_more = input("Would you like to add another product? (yes / no): ").lower()
        if add_more not in ['yes', 'y']:
            break

def view_products():
    if not storages:
        print("No storages currently available.")
        return

    for storage in storages:
        print(f"\nProducts in {storage['name']} storage:")
        if 'products' in storage and storage['products']:
            for product in storage['products']:
                print(f"Product: {product['name']}, Volume: {product['volume']} cubic meters")
        else:
            print("No products available.")

def menu():
    while True:
        print("\nMenu:")
        print("1. Add new storage")
        print("2. View storages")
        print("3. Delete storage")
        print("4. Add product")
        print("5. View products")
        print("6. Exit program")
        
        choice = input("Select: ")
        
        if choice == '1':
            add_storage()
        elif choice == '2':
            view_storages()
        elif choice == '3':
            delete_storage()
        elif choice == '4':
            add_product()
        elif choice == '5':
            view_products()
        elif choice == '6':
            print("Exiting program.")
            break
        else:
            print("Invalid choice, please try again.")

menu()
