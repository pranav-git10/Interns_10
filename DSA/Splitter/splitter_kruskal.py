import math
from typing import List, Dict, Optional

class Expense:
    def __init__(self, payer: str = "", category: str = "", amount: float = 0.0, participants: Optional[List[str]] = None):
        self.payer = payer
        self.category = category
        self.amount = amount
        self.participants = participants if participants is not None else []

class Transfer:
    def __init__(self, from_person: str = "", to_person: str = "", amount: float = 0.0):
        self.from_person = from_person
        self.to_person = to_person
        self.amount = amount

class Edge:
    def __init__(self, from_node: int = 0, to_node: int = 0, weight: float = 0.0):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight

def line(n: int) -> None:
    print("-" * n)

class Group:
    def __init__(self, group_name: str, num_people: int, people_dict: Dict[str, int]):
        self.group_name = group_name
        self.number_of_persons = num_people
        self.people_arr = people_dict
        self.people_included_in_expense_arr: Dict[str, int] = {}
        self.graph = [[0.0 for _ in range(num_people)] for _ in range(num_people)]
        self.expense_history: List[Expense] = []
        self.transfer_history: List[Transfer] = []
    
    def get_minimum(self, array: List[float]) -> int:
        min_index = 0
        for i in range(1, self.number_of_persons):
            if array[i] < array[min_index]:
                min_index = i
        return min_index
    
    def get_maximum(self, array: List[float]) -> int:
        max_index = 0
        for i in range(1, self.number_of_persons):
            if array[i] > array[max_index]:
                max_index = i
        return max_index
    
    def minimum_of_two(self, number1: float, number2: float) -> float:
        return number1 if number1 < number2 else number2
    
    def find_name_for_index(self, index: int) -> str:
        for name, idx in self.people_arr.items():
            if idx == index:
                return name
        return ""
    
    def min_cash_flow_recursion(self, amount: List[float]) -> None:
        max_credit = self.get_maximum(amount)
        max_debit = self.get_minimum(amount)
        
        if amount[max_credit] <= 0.01 and amount[max_debit] <= 0.01:
            return
        
        minimum = self.minimum_of_two(-amount[max_debit], amount[max_credit])
        amount[max_credit] -= minimum
        amount[max_debit] += minimum
        
        print(f"{self.find_name_for_index(max_debit)} pays {minimum} to {self.find_name_for_index(max_credit)}.")
        
        self.min_cash_flow_recursion(amount)
    
    def min_cash_flow(self) -> None:
        amount = [0.0] * self.number_of_persons
        
        for p in range(self.number_of_persons):
            for i in range(self.number_of_persons):
                amount[p] += (self.graph[i][p] - self.graph[p][i])
        
        self.min_cash_flow_recursion(amount)
    
    def settle(self) -> None:
        line(64)
        print("\n\n")
        self.min_cash_flow()
        print("\n\n")
        line(64)
        print("\n\n")
    
    def transfer(self) -> None:
        person_who_transferred = input("Who transferred: ")
        
        if person_who_transferred not in self.people_arr:
            print("Person not found in the group. Transfer cancelled.")
            return
        
        transferred_to = input("Transferred to: ")
        
        if transferred_to not in self.people_arr:
            print("Person not found in the group. Transfer cancelled.")
            return
        
        try:
            transfer_money = float(input("How much transferred: "))
            if transfer_money <= 0:
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter a positive number.")
            return
        
        self.graph[self.people_arr[transferred_to]][self.people_arr[person_who_transferred]] += transfer_money
        
        transfer = Transfer(person_who_transferred, transferred_to, transfer_money)
        self.transfer_history.append(transfer)
    
    def add_expense(self) -> None:
        try:
            expense = float(input(f"Enter expense amount to group {self.group_name}: "))
            if expense <= 0:
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter a positive number.")
            return
        
        person_who_paid = input("Who paid: ")
        
        if person_who_paid not in self.people_arr:
            print("\nWrong name entered. Expense addition cancelled. \n")
            return
        
        try:
            n = int(input("Enter the number of people paid for: "))
            if n <= 0 or n > self.number_of_persons:
                raise ValueError
        except ValueError:
            print(f"Invalid input. Please enter a number between 1 and {self.number_of_persons}.")
            return
        
        category = input("Enter the category of the expense: ")
        
        participants = []
        for i in range(n):
            peop = input(f"Enter {i + 1} person: ")
            if peop not in self.people_arr:
                print("Wrong name entered. Enter again.\n\n")
                return
            participants.append(peop)
        
        each_person_expense = expense / n
        
        for participant in participants:
            self.graph[self.people_arr[participant]][self.people_arr[person_who_paid]] += each_person_expense
        
        new_expense = Expense(person_who_paid, category, expense, participants)
        self.expense_history.append(new_expense)
    
    def generate_report(self) -> None:
        print(f"\n********** Expense Report and Transfer History for Group {self.group_name} **********\n\n")
        
        if self.expense_history:
            print("Expense History:")
            for i, exp in enumerate(self.expense_history):
                print(f"Expense {i + 1}:")
                print(f"  Payer: {exp.payer}")
                print(f"  Category: {exp.category}")
                print(f"  Amount: {exp.amount}")
                print(f"  Participants: {' '.join(exp.participants)}")
                print("\n")
        else:
            print("No expenses recorded.\n")
        
        if self.transfer_history:
            print("Transfer History:")
            for i, transfer in enumerate(self.transfer_history):
                print(f"Transfer {i + 1}:")
                print(f"  From: {transfer.from_person}")
                print(f"  To: {transfer.to_person}")
                print(f"  Amount: {transfer.amount}")
                print("\n")
        else:
            print("No transfers recorded.\n")
    
    def edit_expense(self) -> None:
        self.generate_report()
        try:
            index = int(input("Enter the index of the expense to edit: "))
            if index < 1 or index > len(self.expense_history):
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter a valid index.")
            return
        
        exp = self.expense_history[index - 1]
        print(f"Editing Expense {index}:")
        print(f"  Current Payer: {exp.payer}")
        new_payer = input("  Enter new payer (or press Enter to keep the same): ")
        if new_payer:
            exp.payer = new_payer
        
        print(f"  Current Category: {exp.category}")
        new_category = input("  Enter new category (or press Enter to keep the same): ")
        if new_category:
            exp.category = new_category
        
        print(f"  Current Amount: {exp.amount}")
        new_amount_str = input("  Enter new amount (or press Enter to keep the same): ")
        if new_amount_str:
            try:
                new_amount = float(new_amount_str)
                exp.amount = new_amount
            except ValueError:
                print("Invalid amount. Keeping the original amount.")
        
        print(f"  Current Participants: {' '.join(exp.participants)}")
        new_participants_str = input("  Enter new participants separated by space (or press Enter to keep the same): ")
        if new_participants_str:
            new_participants = new_participants_str.split()
            exp.participants = new_participants
    
    def delete_expense(self) -> None:
        self.generate_report()
        try:
            index = int(input("Enter the index of the expense to delete: "))
            if index < 1 or index > len(self.expense_history):
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter a valid index.")
            return
        
        self.expense_history.pop(index - 1)
    
    def edit_transfer(self) -> None:
        self.generate_report()
        try:
            index = int(input("Enter the index of the transfer to edit: "))
            if index < 1 or index > len(self.transfer_history):
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter a valid index.")
            return
        
        transfer = self.transfer_history[index - 1]
        print(f"Editing Transfer {index}:")
        print(f"  Current Sender: {transfer.from_person}")
        new_sender = input("  Enter new sender (or press Enter to keep the same): ")
        if new_sender:
            transfer.from_person = new_sender
        
        print(f"  Current Receiver: {transfer.to_person}")
        new_receiver = input("  Enter new receiver (or press Enter to keep the same): ")
        if new_receiver:
            transfer.to_person = new_receiver
        
        print(f"  Current Amount: {transfer.amount}")
        new_amount_str = input("  Enter new amount (or press Enter to keep the same): ")
        if new_amount_str:
            try:
                new_amount = float(new_amount_str)
                transfer.amount = new_amount
            except ValueError:
                print("Invalid amount. Keeping the original amount.")
    
    def delete_transfer(self) -> None:
        self.generate_report()
        try:
            index = int(input("Enter the index of the transfer to delete: "))
            if index < 1 or index > len(self.transfer_history):
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter a valid index.")
            return
        
        self.transfer_history.pop(index - 1)
    
    def get_edges(self) -> List[Edge]:
        edges = []
        for i in range(self.number_of_persons):
            for j in range(i + 1, self.number_of_persons):
                if self.graph[i][j] != 0:
                    e = Edge(i, j, self.graph[i][j])
                    edges.append(e)
        return edges
    
    def minimum_spanning_tree(self) -> List[Edge]:
        edges = self.get_edges()
        edges.sort(key=lambda x: x.weight)
        
        mst = []
        tree_id = list(range(self.number_of_persons))
        
        for edge in edges:
            a = edge.from_node
            b = edge.to_node
            w = edge.weight
            if tree_id[a] != tree_id[b]:
                mst.append(edge)
                old_id = tree_id[b]
                new_id = tree_id[a]
                for i in range(self.number_of_persons):
                    if tree_id[i] == old_id:
                        tree_id[i] = new_id
        return mst

# Dictionary to store groups
groups: Dict[str, Group] = {}

def display_menu(group: str) -> None:
    g1 = groups[group]
    option = 0
    while option != 9:
        print("\n\n******** MAIN MENU ********")
        print(f"\n\n 1. Add expense to {group}")
        print(f"\n 2. Transfer in {group}")
        print(f"\n 3. Settle up {group}")
        print(f"\n 4. Generate and Display Expense Report and Transfer History")
        print(f"\n 5. Edit an Expense")
        print(f"\n 6. Delete an Expense")
        print(f"\n 7. Edit a Transfer")
        print(f"\n 8. Delete a Transfer")
        print(f"\n 9. Exit \n")
        line(64)
        print("\nEnter your option: ", end="")
        
        try:
            option = int(input())
            if option < 1 or option > 9:
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")
            continue
        
        if option == 1:
            g1.add_expense()
        elif option == 2:
            g1.transfer()
        elif option == 3:
            g1.settle()
        elif option == 4:
            g1.generate_report()
        elif option == 5:
            g1.edit_expense()
        elif option == 6:
            g1.delete_expense()
        elif option == 7:
            g1.edit_transfer()
        elif option == 8:
            g1.delete_transfer()
    
    print("\n\n\n\n")

def form_new_group() -> None:
    group = ""
    while True:
        group = input("Enter name of the group: ")
        
        if group in groups:
            print("Group already exists. Enter a new group: ")
        else:
            break
    
    try:
        num_people = int(input(f"Enter the number of people in group {group}: "))
        if num_people <= 0:
            raise ValueError
    except ValueError:
        print("Invalid input. Please enter a positive number.")
        return
    
    people = {}
    print(f"Enter the names of people in group {group}: ")
    for i in range(num_people):
        name = input()
        people[name] = i
    
    g = Group(group, num_people, people)
    groups[group] = g
    
    display_menu(group)

def enter_old_group() -> None:
    if not groups:
        print("\n\nNo groups formed. Form a new group first.\n")
        return
    
    name = ""
    while True:
        print("\n\nEnter group name: ", end="")
        name = input()
        if name not in groups:
            print("No such group exists. Enter again: ")
        else:
            break
    
    display_menu(name)

def initial_display_menu() -> None:
    choice = 0
    while choice != 3:
        line(64)
        print("\n WELCOME TO SPLITTER \n")
        line(64)
        
        print("\n\n1. Add a new group")
        print("\n2. Enter in old group")
        print("\n3. Exit\n")
        line(64)
        print("\nEnter your choice: ", end="")
        
        try:
            choice = int(input())
            if choice < 1 or choice > 3:
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 3.")
            continue
        
        if choice == 1:
            form_new_group()
        elif choice == 2:
            enter_old_group()

def main() -> int:
    initial_display_menu()
    return 0

if __name__ == "__main__":
    main()
