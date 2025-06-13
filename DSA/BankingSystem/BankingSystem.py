# Node class for singly linked list of accounts
class Node:
    def __init__(self, acc):
        self.acc_no = acc           # Account number
        self.balance = 1000         # Initial balance set to 1000
        self.next = None            # Pointer to next node in the list

# Singly Linked List class for managing accounts
class SLL:
    def __init__(self):
        self.first = None           # Pointer to the first node
        self.last = None            # Pointer to the last node
        self.length = 0             # Length of the linked list

    # Method to add a new account node
    def push_node(self, acc):
        new_node = Node(acc)
        if self.length == 0:
            self.first = self.last = new_node
        else:
            self.last.next = new_node
            self.last = new_node
        self.length += 1

    # Method to find a node by account number
    def find_node(self, acc):
        temp = self.first
        while temp is not None:
            if temp.acc_no == acc:
                return temp
            temp = temp.next
        return None

    # Method to perform deposit or withdrawal transaction
    def transaction(self, acc, mode, val):
        process_node = self.find_node(acc)
        if process_node is not None:
            if mode == 'D':
                process_node.balance += val    # Deposit
            elif mode == 'W':
                process_node.balance -= val    # Withdrawal

    # Method to print number of accounts with balance >= x
    def print_bal_more_x(self, x):
        count = 0
        temp = self.first
        while temp is not None:
            if temp.balance >= x:
                count += 1
            temp = temp.next
        print(f"Number of accounts with balance >= {x}: {count}")

    # Method to print account number(s) with maximum balance
    def print_max_balance(self):
        max_balance = -1
        temp = self.first

        # Find maximum balance
        while temp is not None:
            if temp.balance > max_balance:
                max_balance = temp.balance
            temp = temp.next

        # Print account number(s) with maximum balance
        temp = self.first
        result = []
        while temp is not None:
            if temp.balance == max_balance:
                result.append(str(temp.acc_no))
            temp = temp.next
        print("Account(s) with max balance: "," ".join(result))

    # Method to print balance of account with given account number
    def print_bal_x(self, x):
        temp = self.find_node(x)
        if temp is not None:
            print(temp.balance)
            
    def transfer_amount(self, from_acc, to_acc, amount, dll):
        from_node = self.find_node(from_acc)
        to_node = self.find_node(to_acc)
        if from_node is None or to_node is None:
            print("One or Both account numbers are invalid")
        if from_node.balance < amount:
            print("Amount is greater than Account Balance, Insufficient Funds")
            return
        from_node.balance -= amount
        to_node.balance += amount
        dll.push_d_node(from_acc, 'W', amount)
        dll.push_d_node(to_acc,'D', amount)
        print(f'{amount} has been transferred from account {from_acc} to account {to_acc}')

# Node class for doubly linked list of transactions
class DNode:
    def __init__(self, acc=-1, action='A', val=-1):
        self.acc = acc              # Account number
        self.action = action        # Transaction type (Deposit 'D' or Withdrawal 'W')
        self.amount = val           # Amount of transaction
        self.next = None            # Pointer to next node
        self.prev = None            # Pointer to previous node

# Doubly Linked List class for managing transactions
class DLL:
    def __init__(self):
        self.head = DNode()         # Head sentinel node
        self.tail = DNode()         # Tail sentinel node
        self.head.next = self.tail
        self.tail.prev = self.head
        self.cursor = self.head     # Pointer to current node
        self.d_len = 0              # Length of the doubly linked list
        self.cursor_idx = 0         # Index of current node

    # Method to add a new transaction node
    def push_d_node(self, a, b, c):
        new_node = DNode(a, b, c)
        new_node.prev = self.tail.prev
        self.tail.prev.next = new_node
        new_node.next = self.tail
        self.tail.prev = new_node
        self.d_len += 1

    # Method to process next x transactions on account list l1
    def process_x(self, x, l1):
        while self.cursor.next != self.tail and x > 0:
            self.cursor = self.cursor.next
            self.cursor_idx += 1
            l1.transaction(self.cursor.acc, self.cursor.action, self.cursor.amount)
            x -= 1

    # Method to undo last y transactions on account list l1
    def undo_y(self, y, l1):
        while self.cursor != self.head and y > 0:
            l1.transaction(self.cursor.acc, self.cursor.action, -(self.cursor.amount))
            self.cursor = self.cursor.prev
            self.cursor_idx -= 1
            y -= 1

    # Method to insert a new transaction node at position k
    def insert_node_k(self, a, b, c, k, l1):
        if 1 <= k <= self.d_len:
            add_node = DNode(a, b, c)
            temp = self.head
            for i in range(k):
                temp = temp.next
            temp.next.prev = add_node
            add_node.next = temp.next
            temp.next = add_node
            add_node.prev = temp
            if temp != self.cursor:
                l1.transaction(a, b, c)
            self.d_len += 1

    # Method to delete m transactions for account acc on account list l1
    def delete_am(self, acc, m, l1):
        temp = self.cursor.next
        while temp != self.tail and m != 0:
            if temp.acc == acc:
                del_node = temp
                temp.prev.next = temp.next
                temp.next.prev = temp.prev
                temp = temp.next
                del del_node
                self.d_len -= 1
                m -= 1
            else:
                temp = temp.next
        self.cursor.next = temp

    # Method to process all transactions on account list l1
    def process_all(self, l1):
        self.process_x(self.d_len, l1)

    # Method to print all transactions for account acc
    def print_all_of_y(self, acc):
        temp = self.head.next
        while temp != self.tail:
            if temp.acc == acc:
                print(f"{temp.acc} {temp.action} {temp.amount}")
            temp = temp.next

# MAIN DRIVER FUNCTION
def main():
    accounts = SLL()        # Create an instance of SLL for accounts
    transactions = DLL()    # Create an instance of DLL for transactions

    # Input number of accounts and initialize accounts list
    c = int(input("Enter number of accounts to create: "))
    for i in range(c):
        acs = int(input(f"Enter account number for account {i+1}: "))
        accounts.push_node(acs)

    # Input number of transactions and initialize transactions list
    n = int(input("Enter number of transactions to record: "))
    for i in range(n):
        print(f"Enter transaction {i+1} in the format: <account number> <D for Deposit / W for Withdrawal> <amount>")
        # (e.g., 101 D 500 → deposit ₹500 to account 101)
        line = input("Transaction: ").split()
        acs = int(line[0])
        dw = line[1]
        am = int(line[2])
        transactions.push_d_node(acs, dw, am)

    transactions.process_all(accounts)  # Process all recorded transactions immediately

    print("\n--- Enter Commands ---")
    print("F x: Process next x transactions")
    print("R y: Undo last y transactions")
    print("I a b c k: Insert transaction (a = acc, b = D/W, c = amount, k = position)")
    print("D acc m: Delete m transactions for acc")
    print("C: Process all remaining transactions")
    print("S y: Show all transactions for account y")
    print("G x: Show count of accounts with balance >= x")
    print("M: Show account(s) with max balance")
    print("V x: Show balance of account x")
    print("E: Exit\n")
    
    # Process user commands until 'E' (exit) is encountered
    while True:
        choice = input("\nEnter your command (F, R, I, D, C, S, G, M, V, E to exit): ").strip()

        if choice == 'E':           # Exit the program
            print("Exiting the program. Goodbye!")
            break

        elif choice.startswith('F'):    # Process next x transactions
            x = int(choice.split()[1]) if len(choice.split()) > 1 else int(input("Enter number of transactions to process: "))
            transactions.process_x(x, accounts)
            print(f"Processed {x} transaction(s).")

        elif choice.startswith('R'):    # Undo last y transactions
            y = int(choice.split()[1]) if len(choice.split()) > 1 else int(input("Enter number of transactions to undo: "))
            transactions.undo_y(y, accounts)
            print(f"Undid last {y} transaction(s).")

        elif choice.startswith('I'):    # Insert transaction at position k
            parts = choice.split()
            if len(parts) >= 5:
                acs = int(parts[1])
                dw = parts[2]
                am = int(parts[3])
                k = int(parts[4])
            else:
                print("Enter transaction details in the format: <account number> <D/W> <amount> <position>")
                line = input("Transaction: ").split()
                acs = int(line[0])
                dw = line[1]
                am = int(line[2])
                k = int(line[3])
            transactions.insert_node_k(acs, dw, am, k, accounts)
            print(f"Inserted transaction at position {k}.")

        elif choice.startswith('D'):    # Delete m transactions for account acs
            parts = choice.split()
            if len(parts) >= 3:
                acs = int(parts[1])
                m = int(parts[2])
            else:
                print("Enter deletion details in the format: <account number> <number of transactions to delete>")
                line = input("Delete: ").split()
                acs = int(line[0])
                m = int(line[1])
            transactions.delete_am(acs, m, accounts)
            print(f"Deleted {m} transaction(s) for account {acs}.")

        elif choice == 'C':         # Process all remaining transactions
            transactions.process_all(accounts)
            print("Processed all remaining transactions.")

        elif choice.startswith('S'):    # Print all transactions for account y
            y = int(choice.split()[1]) if len(choice.split()) > 1 else int(input("Enter account number to view transactions: "))
            print(f"Transactions for account {y}:")
            transactions.print_all_of_y(y)

        elif choice.startswith('G'):    # Print number of accounts with balance >= x
            x = int(choice.split()[1]) if len(choice.split()) > 1 else int(input("Enter the minimum balance to check: "))
            print(f"Number of accounts with balance >= {x}:")
            accounts.print_bal_more_x(x)

        elif choice == 'M':         # Print account number(s) with maximum balance
            print("Account(s) with maximum balance:")
            accounts.print_max_balance()

        elif choice.startswith('V'):    # Print balance of account with account number x
            x = int(choice.split()[1]) if len(choice.split()) > 1 else int(input("Enter account number to view balance: "))
            print(f"Balance for account {x}: ")
            accounts.print_bal_x(x)
            
        elif choice == 'T':  # Transfer money between accounts
            from_acc, to_acc, amount = map(int, input("Enter transfer details (from account, to account, amount): ").split())
            result = accounts.transfer_amount(from_acc, to_acc, amount, dll=transactions)

if __name__ == "__main__":
    main()