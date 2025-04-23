import json

class bankAccount:
    def __init__(self, number, PIN, balance=0):
        self.number = number
        self.balance = balance
        self.PIN1 = PIN
        self.transcation_history = []

    def deposit(self, deposit_amount):
        self.balance += deposit_amount
        self.transcation_history.append(f"Deposited {deposit_amount} to account")

    def withdraw(self, withdraw_amount):
        if self.balance >= withdraw_amount:
            self.balance -= withdraw_amount
            self.transcation_history.append(f"Withdrew {withdraw_amount} from account")
        else:
            print("Insufficient funds :(")

    def check_balance(self):
        print(f"Your balance is {self.balance}")

    def printTransactionHistory(self):
        print(self.transcation_history)

    def checkPIN(self, userPIN):
        return userPIN == self.PIN1


class Bank:
    def __init__(self):
        self.user_accounts = {}
        self.load_from_json()  # load data 

    def load_from_json(self):
        try:
            with open("bank_data.json", "r") as file:
                data = json.load(file)
                for account_num, acc_data in data.items():
                    self.user_accounts[account_num] = bankAccount(
                        account_num,
                        acc_data["PIN"],
                        acc_data["balance"]
                    )
                    self.user_accounts[account_num].transcation_history = acc_data["transaction_history"]
        except FileNotFoundError:
            print("No previous data found")

    def save_to_json(self):
        with open("bank_data.json", "w") as file:
            data = {
                acc_num: {
                    "PIN": acc.PIN1,
                    "balance": acc.balance,
                    "transaction_history": acc.transcation_history
                }
                for acc_num, acc in self.user_accounts.items()
            }
            json.dump(data, file, indent=4)

    def find_account(self, accountNumber):
        return accountNumber in self.user_accounts

    def create_account(self, accountNumber, accountPIN, accountBalance):
        if not self.find_account(accountNumber):
            self.user_accounts[accountNumber] = bankAccount(accountNumber, accountPIN, accountBalance)
        else:
            print("Account already exists!")

    def delete_account(self, accountNumber):
        if self.find_account(accountNumber):
            del self.user_accounts[accountNumber]
            print(f"Account {accountNumber} deleted.")
        else:
            print("Account does not exist!")

    def printAllAccounts(self):
        for account_number, account in self.user_accounts.items():
            print(f"Account Number: {account_number}, Balance: {account.balance}, Transactions: {account.transcation_history}")

    def get_account(self, accountNumber):
        if self.find_account(accountNumber):
            account = self.user_accounts[accountNumber]
            return {
                "PIN": account.PIN1,
                "balance": account.balance,
                "transaction_history": account.transcation_history
            }
        else:
            print("Account does not exist!")
            return None


class ATM:
    @staticmethod #doesn't need an instance to use it
    def main_menu(bank):
        user_choice = 0
        while user_choice != 4:
            print("\nWelcome to the Banking System")
            print("1. Open New Account")
            print("2. Access Existing Account")
            print("3. Admin Menu")
            print("4. Exit")

            user_choice = int(input("Enter your choice: "))

            if user_choice == 1:
                ATM.new_account(bank)
            elif user_choice == 2:
                ATM.existing_acc(bank)
            elif user_choice == 3:
                ATM.admin_menu(bank)
            elif user_choice == 4:
                print("Exiting...")
                bank.save_to_json()  
                break

    @staticmethod
    def new_account(bank):
        accountNumber = input("Enter your account number: ")
        accountPIN = input("Enter your 4-digit PIN: ")

        while len(accountPIN) != 4:
            print("PIN number invalid!")
            accountPIN = input("Enter your 4-digit PIN: ")

        initialBalance = float(input("Enter your initial balance: "))
        while initialBalance < 0:
            print("Balance is invalid")
            initialBalance = float(input("Enter your initial balance again: "))

        bank.create_account(accountNumber, accountPIN, initialBalance)

    @staticmethod
    def pin_check(account):
        attempts = 3
        while attempts > 0:
            user_pin = input("Enter your PIN: ")
            if account.checkPIN(user_pin):
                print("Welcome back!")
                return True
            else:
                attempts -= 1
                print(f"Wrong PIN. Attempts left: {attempts}")
        if attempts == 0:
            print("Account locked. Too many failed attempts.")
            return False

    @staticmethod
    def existing_acc(bank):
        accountNumber = input("Enter your account number: ")

        if not bank.find_account(accountNumber):
            print("Account not found!")
            return

        account = bank.user_accounts[accountNumber]

        if ATM.pin_check(account): 
            print("1. Check balance")
            print("2. Deposit money")
            print("3. Withdraw money")
            print("4. View transaction history")
            print("5. Return to main menu")

            user_choice = int(input("Enter your choice: "))

            if user_choice == 1:
                account.check_balance()
            elif user_choice == 2:
                amount = float(input("Enter amount to deposit: "))
                account.deposit(amount)
            elif user_choice == 3:
                amount = float(input("Enter amount to withdraw: "))
                account.withdraw(amount)
            elif user_choice == 4:
                account.printTransactionHistory()
            elif user_choice == 5:
                bank.main_menu(bank)

    @staticmethod
    def admin_menu(bank):
        password = input("Enter Admin password: ")
        if password == "AdminPassword:)":
            print("Welcome back!")
            print("1. View all accounts")
            print("2. Delete account")
            print("3. Return to main menu")

            user_choice = int(input("Enter your choice: "))

            if user_choice == 1:
                bank.printAllAccounts()
            elif user_choice == 2:
                accountNumber = input("Enter the account number to delete: ")
                bank.delete_account(accountNumber)
            elif user_choice == 3:
                bank.main_menu(bank)


if __name__ == "__main__":
    bank = Bank()
    ATM.main_menu(bank)
