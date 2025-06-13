This repository contains a C++ program that simulates a simple banking system. It allows for managing multiple bank accounts and performing various transactions on them. The program utilizes linked lists (SLL for accounts and DLL for transactions) to efficiently store and process data.

Features Account Management:

Create new accounts. Retrieve account balances. Find accounts with maximum balance. Transaction Handling:

Deposit and withdraw funds from accounts. Undo recent transactions. Process batches of transactions. Usage Input Format The program expects input in the following format:

First, provide the number of accounts followed by their account numbers. Then, specify the number of transactions, each consisting of an account number, transaction type (D for deposit, W for withdrawal), and amount. After input initialization, enter commands to perform operations: F x: Process the next x transactions. R y: Undo the last y transactions. I acc action amount k: Insert a transaction for account acc with action (D or W), amount, at position k. D acc m: Delete m transactions for account acc. C: Process all remaining transactions. S acc: Print all transactions for account acc. G x: Print the number of accounts with balance greater than or equal to x. M: Print account number(s) with maximum balance. V acc: Print balance of account acc. E: Exit the program.