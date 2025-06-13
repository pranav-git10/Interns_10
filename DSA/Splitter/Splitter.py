class Expense:
    def __init__(self, payer, category, amount, participants):
        self.payer = payer
        self.category = category
        self.amount = amount
        self.participants = participants

class Transfer:
    def __init__(self, from_person, to_person, amount):
        self.from_person = from_person
        self.to_person = to_person
        self.amount = amount

class Group:
    def __init__(self, group_name, number_of_persons, people_dict):
        self.group_name = group_name
        self.number_of_persons = number_of_persons
        self.people_dict = people_dict
        self.expense_history = []
        self.transfer_history = []
        # Initialize graph as 2D array with zeros
        self.graph = [[0.0 for _ in range(number_of_persons)] for _ in range(number_of_persons)]
    
    def line(self, n):
        print("-" * n)
    
    # finds the person who owes the most money
    def get_minimum_index(self, amount_array):
        min_index = 0
        for i in range(1, self.number_of_persons):
            if amount_array[i] < amount_array[min_index]:
                min_index = i
        return min_index
    
    # finds the person who is owed the most money in the group.
    def get_maximum_index(self, amount_array):
        max_index = 0
        for i in range(1, self.number_of_persons):
            if amount_array[i] > amount_array[max_index]:
                max_index = i
        return max_index
    
    def minimum_of_two(self, num1, num2):
        return min(num1, num2)
    
    def find_name_for_index(self, index):
        for name, idx in self.people_dict.items():
            if idx == index:
                return name
        return ""
    
    def min_cash_flow_recursion(self, amount):
        max_credit = self.get_maximum_index(amount)
        max_debit = self.get_minimum_index(amount)
        
        # Base case: if both credits and debits are negligible
        if amount[max_credit] <= 0.01 and amount[max_debit] >= -0.01:
            return
        
        # Calculate minimum transfer amount
        minimum = self.minimum_of_two(-amount[max_debit], amount[max_credit])
        amount[max_credit] -= minimum
        amount[max_debit] += minimum
        
        debtor_name = self.find_name_for_index(max_debit)
        creditor_name = self.find_name_for_index(max_credit)
        
        print(f"{debtor_name} pays {minimum:.2f} to {creditor_name}.")
        
        # Recursive call
        self.min_cash_flow_recursion(amount)
    
    def min_cash_flow(self):
        # Calculate net amount for each person
        amount = [0.0 for _ in range(self.number_of_persons)]
        
        for p in range(self.number_of_persons):
            for i in range(self.number_of_persons):
                # amount[p] += what others owe to p - what p owes to others
                amount[p] += (self.graph[i][p] - self.graph[p][i])
        
        self.min_cash_flow_recursion(amount)
    
    def settle(self):
        self.line(64)
        print("\n")
        self.min_cash_flow()
        print("\n")
        self.line(64)
        print("\n")
    
    def transfer(self):
        print("Who transferred: ", end="")
        person_who_transferred = input().strip()
        
        if person_who_transferred not in self.people_dict:
            print("Person not found in the group. Transfer cancelled.")
            return
        
        print("Transferred to: ", end="")
        transferred_to = input().strip()
        
        if transferred_to not in self.people_dict:
            print("Person not found in the group. Transfer cancelled.")
            return
        
        while True:
            try:
                transfer_money = float(input("How much transferred: "))
                if transfer_money <= 0:
                    print("Please enter a positive number.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        
        # Update graph: transferred_to owes less to person_who_transferred
        self.graph[self.people_dict[transferred_to]][self.people_dict[person_who_transferred]] += transfer_money
        
        # Record transfer
        transfer = Transfer(person_who_transferred, transferred_to, transfer_money)
        self.transfer_history.append(transfer)
        print("Transfer recorded successfully!")
    
    def add_expense(self):
        print(f"Enter expense amount to group {self.group_name}: ", end="")
        while True:
            try:
                expense = float(input())
                if expense <= 0:
                    print("Please enter a positive number: ", end="")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid number: ", end="")
        
        print("Who paid: ", end="")
        person_who_paid = input().strip()
        
        if person_who_paid not in self.people_dict:
            print("\nWrong name entered. Expense addition cancelled.\n")
            return
        
        print("Enter the number of people paid for: ", end="")
        while True:
            try:
                n = int(input())
                if n <= 0 or n > self.number_of_persons:
                    print(f"Please enter a number between 1 and {self.number_of_persons}: ", end="")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid number: ", end="")
        
        print("Enter the category of the expense: ", end="")
        category = input().strip()
        
        participants = []
        for i in range(n):
            print(f"Enter {i + 1} person: ", end="")
            person = input().strip()
            if person not in self.people_dict:
                print("Wrong name entered. Enter again.\n")
                return
            participants.append(person)
        
        # Calculate each person's share
        each_person_expense = expense / n
        
        # Update graph: each participant owes their share to the payer
        for participant in participants:
            self.graph[self.people_dict[participant]][self.people_dict[person_who_paid]] += each_person_expense
        
        # Record expense
        new_expense = Expense(person_who_paid, category, expense, participants)
        self.expense_history.append(new_expense)
        print("Expense added successfully!")
    
    def generate_report(self):
        print(f"\n********** Expense Report and Transfer History for Group {self.group_name} **********\n")
        
        if self.expense_history:
            print("Expense History:")
            for i, exp in enumerate(self.expense_history):
                print(f"Expense {i + 1}:")
                print(f"  Payer: {exp.payer}")
                print(f"  Category: {exp.category}")
                print(f"  Amount: {exp.amount:.2f}")
                print(f"  Participants: {' '.join(exp.participants)}")
                print()
        else:
            print("No expenses recorded.\n")
        
        if self.transfer_history:
            print("Transfer History:")
            for i, transfer in enumerate(self.transfer_history):
                print(f"Transfer {i + 1}:")
                print(f"  From: {transfer.from_person}")
                print(f"  To: {transfer.to_person}")
                print(f"  Amount: {transfer.amount:.2f}")
                print()
        else:
            print("No transfers recorded.\n")
    
    def edit_expense(self):
        if not self.expense_history:
            print("No expenses to edit.")
            return
        
        self.generate_report()
        print("Enter the index of the expense to edit: ", end="")
        while True:
            try:
                index = int(input())
                if index < 1 or index > len(self.expense_history):
                    print("Invalid index. Please enter a valid index: ", end="")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid number: ", end="")
        
        exp = self.expense_history[index - 1]
        print(f"Editing Expense {index}:")
        print(f"  Current Payer: {exp.payer}")
        new_payer = input("  Enter new payer (or press Enter to keep the same): ")
        if new_payer.strip():
            exp.payer = new_payer.strip()
        
        print(f"  Current Category: {exp.category}")
        new_category = input("  Enter new category (or press Enter to keep the same): ")
        if new_category.strip():
            exp.category = new_category.strip()
        
        print(f"  Current Amount: {exp.amount}")
        new_amount_str = input("  Enter new amount (or press Enter to keep the same): ")
        if new_amount_str.strip():
            try:
                exp.amount = float(new_amount_str)
            except ValueError:
                print("Invalid amount. Keeping original amount.")
        
        print(f"  Current Participants: {' '.join(exp.participants)}")
        new_participants_str = input("  Enter new participants separated by space (or press Enter to keep the same): ")
        if new_participants_str.strip():
            exp.participants = new_participants_str.strip().split()
        
        print("Expense updated successfully!")
    
    def delete_expense(self):
        if not self.expense_history:
            print("No expenses to delete.")
            return
        
        self.generate_report()
        print("Enter the index of the expense to delete: ", end="")
        while True:
            try:
                index = int(input())
                if index < 1 or index > len(self.expense_history):
                    print("Invalid index. Please enter a valid index: ", end="")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid number: ", end="")
        
        del self.expense_history[index - 1]
        print("Expense deleted successfully!")
    
    def edit_transfer(self):
        if not self.transfer_history:
            print("No transfers to edit.")
            return
        
        self.generate_report()
        print("Enter the index of the transfer to edit: ", end="")
        while True:
            try:
                index = int(input())
                if index < 1 or index > len(self.transfer_history):
                    print("Invalid index. Please enter a valid index: ", end="")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid number: ", end="")
        
        transfer = self.transfer_history[index - 1]
        print(f"Editing Transfer {index}:")
        print(f"  Current Sender: {transfer.from_person}")
        new_sender = input("  Enter new sender (or press Enter to keep the same): ")
        if new_sender.strip():
            transfer.from_person = new_sender.strip()
        
        print(f"  Current Receiver: {transfer.to_person}")
        new_receiver = input("  Enter new receiver (or press Enter to keep the same): ")
        if new_receiver.strip():
            transfer.to_person = new_receiver.strip()
        
        print(f"  Current Amount: {transfer.amount}")
        new_amount_str = input("  Enter new amount (or press Enter to keep the same): ")
        if new_amount_str.strip():
            try:
                transfer.amount = float(new_amount_str)
            except ValueError:
                print("Invalid amount. Keeping original amount.")
        
        print("Transfer updated successfully!")
    
    def delete_transfer(self):
        if not self.transfer_history:
            print("No transfers to delete.")
            return
        
        self.generate_report()
        print("Enter the index of the transfer to delete: ", end="")
        while True:
            try:
                index = int(input())
                if index < 1 or index > len(self.transfer_history):
                    print("Invalid index. Please enter a valid index: ", end="")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid number: ", end="")
        
        del self.transfer_history[index - 1]
        print("Transfer deleted successfully!")

# Global dictionary to store all groups
groups = {}

def display_menu(group_name):
    group = groups[group_name]
    
    while True:
        print("\n\n******** MAIN MENU ********")
        print(f"\n\n 1. Add expense to {group_name}")
        print(f" 2. Transfer in {group_name}")
        print(f" 3. Settle up {group_name}")
        print(" 4. Generate and Display Expense Report and Transfer History")
        print(" 5. Edit an Expense")
        print(" 6. Delete an Expense")
        print(" 7. Edit a Transfer")
        print(" 8. Delete a Transfer")
        print(" 9. Exit")
        print("-" * 64)
        
        while True:
            try:
                option = int(input("Enter your option: "))
                if option < 1 or option > 9:
                    print("Please enter a number between 1 and 9: ", end="")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 9: ", end="")
        
        if option == 1:
            group.add_expense()
        elif option == 2:
            group.transfer()
        elif option == 3:
            group.settle()
        elif option == 4:
            group.generate_report()
        elif option == 5:
            group.edit_expense()
        elif option == 6:
            group.delete_expense()
        elif option == 7:
            group.edit_transfer()
        elif option == 8:
            group.delete_transfer()
        elif option == 9:
            break
    
    print("\n\n\n")

def form_new_group():
    while True:
        group_name = input("Enter name of the group: ").strip()
        if group_name in groups:
            print("Group already exists. Enter a new group name.")
        else:
            break
    
    while True:
        try:
            num_people = int(input(f"Enter the number of people in group {group_name}: "))
            if num_people <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    print(f"Enter the names of people in group {group_name}:")
    people_dict = {}
    for i in range(num_people):
        name = input(f"Person {i + 1}: ").strip()
        people_dict[name] = i
    
    # Create new group
    group = Group(group_name, num_people, people_dict)
    groups[group_name] = group
    
    print(f"Group '{group_name}' created successfully!")
    display_menu(group_name)

def enter_old_group():
    if not groups:
        print("\n\nNo groups formed. Form a new group first.\n")
        return
    
    print("\nAvailable groups:")
    for group_name in groups.keys():
        print(f"  - {group_name}")
    
    while True:
        group_name = input("\nEnter group name: ").strip()
        if group_name not in groups:
            print("No such group exists. Please enter a valid group name.")
        else:
            break
    
    display_menu(group_name)

def initial_display_menu():
    while True:
        print("-" * 64)
        print(" WELCOME TO SPLITTER ")
        print("-" * 64)
        print("\n1. Add a new group")
        print("2. Enter in old group")
        print("3. Exit")
        print("-" * 64)
        
        while True:
            try:
                choice = int(input("Enter your choice: "))
                if choice < 1 or choice > 3:
                    print("Please enter a number between 1 and 3: ", end="")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 3: ", end="")
        
        if choice == 1:
            form_new_group()
        elif choice == 2:
            enter_old_group()
        elif choice == 3:
            print("Thank you for using Splitter!")
            break

def main():
    initial_display_menu()

if __name__ == "__main__":
    main()