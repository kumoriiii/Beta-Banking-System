
from tkinter import *
from PIL import ImageTk, Image
import os  
import re  
from datetime import datetime

font_tmp = ("Varela round", 16)

# main screen
master = Tk()
master.configure(background='#4966eb')
master.geometry("350x700")
master.title('Banking App')

# center
main_frame = Frame(master, bg='#4966eb')
main_frame.pack(expand=True)

# PIN validation function using regular expression (start, any digit, has to be 4, end)
def validate_pin(pin):
    return re.match(r'^\d{4}$', pin) is not None

#functions
def finish_reg():
    account_number = temp_number.get()
    name = temp_name.get()
    Pin = temp_PIN.get()
    initial_balance = temp_balance.get()  
    all_accounts = os.listdir()
    
    if account_number == "" or name == "" or Pin == "" or initial_balance == "":  
        notif.config(fg="red", text="All fields are required")
        return
    
    if not validate_pin(Pin):
        notif.config(fg="red", text="PIN must be 4 digits")
        return
    
    for name_check in all_accounts:
        if name_check == account_number:
            notif.config(fg="red", text="Account already exists")
            return
    
    # account file
    new_file = open(account_number, "w")
    new_file.write(account_number + "\n")
    new_file.write(name + "\n")
    new_file.write(Pin + "\n")
    new_file.write(initial_balance + "\n")
    
    # transaction history file
    new_file.write("Transaction History:\n")
    new_file.close()
    notif.config(fg="green", text="Account has been created")

def register():
    #Vars
    global temp_number
    global temp_name
    global temp_PIN
    global temp_balance
    global notif 
    
    temp_number = StringVar()
    temp_name = StringVar()
    temp_PIN = StringVar()
    temp_balance = StringVar()
    
    #Register Screen
    register_screen = Toplevel(master)
    register_screen.title('Register')
    
    #Labels
    Label(register_screen, text="Please enter your details below to register", font=font_tmp).grid(row=0, sticky=N, pady=10)
    Label(register_screen, text="Full Name", font=font_tmp).grid(row=1, sticky=W)
    Label(register_screen, text="Account Number", font=font_tmp).grid(row=2, sticky=W)
    Label(register_screen, text="Account PIN (4 digits)", font=font_tmp).grid(row=3, sticky=W)  
    Label(register_screen, text="Initial Balance", font=font_tmp).grid(row=4, sticky=W)
    notif = Label(register_screen, font=font_tmp)
    notif.grid(row=6, sticky=N, pady=10)
    
    #Entries 
    Entry(register_screen, textvariable=temp_name).grid(row=1, column=1)
    Entry(register_screen, textvariable=temp_number).grid(row=2, column=1)
    Entry(register_screen, textvariable=temp_PIN, show="*").grid(row=3, column=1)
    Entry(register_screen, textvariable=temp_balance).grid(row=4, column=1)
    
    #Buttons
    Button(register_screen, text="Register", command=finish_reg, font=font_tmp).grid(row=5, sticky=N, pady=10)

def login_session():
    global login_number
    all_accounts = os.listdir()
    login_number = temp_login_number.get()
    login_password = temp_login_password.get()
    
    if not validate_pin(login_password):
        login_notif.config(fg="red", text="PIN must be 4 digits")
        return
    
    for name in all_accounts:
        if name == login_number:
            file = open(name, "r")
            file_data = file.read()
            file_data = file_data.split('\n')
            name = file_data[1]
            password = file_data[2]
            
            if login_password == password:
                login_screen.destroy()
                account_dashboard = Toplevel(master)
                account_dashboard.title('Dashboard')
                
                Label(account_dashboard, text="Account Dashboard", font=font_tmp).grid(row=0, sticky=N, padx=10)
                Label(account_dashboard, text=f"Welcome Back, {name}", font=font_tmp).grid(row=1, sticky=N, pady=5)
                
                Button(account_dashboard, text="Check Balance", font=font_tmp, width=30, command=check_balance).grid(row=2, sticky=N, padx=10)
                Button(account_dashboard, text="Deposit", font=font_tmp, width=30, command=deposit).grid(row=3, sticky=N, padx=10)
                Button(account_dashboard, text="Withdraw", font=font_tmp, width=30, command=withdraw).grid(row=4, sticky=N, padx=10)
                Button(account_dashboard, text="Transaction History", font=font_tmp, width=30, command=transaction_history).grid(row=5, sticky=N, padx=10)
                Label(account_dashboard).grid(row=6, sticky=N, pady=10)
                return
            else:
                login_notif.config(fg="red", text="Incorrect PIN")
                return
        
    login_notif.config(fg="red", text="No account found")

def check_balance():
    file = open(login_number, 'r')
    file_data = file.read()
    user_details = file_data.split('\n')
    user_balance = user_details[3]
    balance_check_screen = Toplevel(master)
    balance_check_screen.title('Balance Details')
    Label(balance_check_screen, text="Your Current Balance Is: $"+user_balance, font=font_tmp).grid(row=1, sticky=N, pady=10)

def deposit():
    #Vars
    global amount
    global deposit_notif
    global current_balance_label
    amount=StringVar()
    file=open(login_number,"r")
    file_data=file.read()
    user_details=file_data.split("\n")
    details_balance= user_details[3]
    
    #Deposit_screen
    deposit_screen=Toplevel(master)
    deposit_screen.title('Deposit')
    
    #Label
    Label(deposit_screen, text="Deposit", font=font_tmp).grid(row=0, sticky=N, pady=10)
    current_balance_label=Label(deposit_screen, text="Current Balance: $"+details_balance, font=font_tmp)
    current_balance_label.grid(row=1,sticky=W)
    Label(deposit_screen, text="Amount", font=font_tmp).grid(row=2, sticky=W)
    deposit_notif=Label(deposit_screen, font=font_tmp)
    deposit_notif.grid(row=4,sticky=N, pady=5)
    
    #Entry
    Entry(deposit_screen,textvariable=amount).grid(row=2, column=1)
    #Button
    Button(deposit_screen, text="Finish", font=font_tmp, command=finish_deposit).grid(row=3,sticky=W,pady=5)

def finish_deposit():
    if amount.get()=="":
        deposit_notif.config(text='Amount is required!', fg="red")
        return
    if float(amount.get())<=0:
         deposit_notif.config(text='Negative currency is not accepted :I', fg="red")
         return
     
    file= open(login_number,'r+')
    file_data=file.read()
    details=file_data.split('\n')
    current_balance=details[3]
    updated_balance=current_balance
    updated_balance=float(updated_balance)+float(amount.get())
    
    # Update transaction history
    transaction_record = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Deposit: +${amount.get()}\n"
    file_data = file_data.replace(current_balance, str(updated_balance))
    file_data = file_data.replace("Transaction History:\n", f"Transaction History:\n{transaction_record}")
    
    file.seek(0)
    file.truncate(0)
    file.write(file_data)
    file.close()
    
    current_balance_label.config(text="Current Balance: $"+str(updated_balance),fg="green")
    deposit_notif.config(text="Balance Updated!",fg="green")

def withdraw():
    #Vars
    global withdraw_amount
    global withdraw_notif
    global current_balance_label
    withdraw_amount=StringVar()
    file=open(login_number,"r")
    file_data=file.read()
    user_details=file_data.split("\n")
    details_balance= user_details[3]
    
    #Withdraw_screen
    withdraw_screen=Toplevel(master)
    withdraw_screen.title('Withdraw')
    
    #Label
    Label(withdraw_screen, text="Withdraw", font=font_tmp).grid(row=0, sticky=N, pady=10)
    current_balance_label=Label(withdraw_screen, text="Current Balance: $"+details_balance, font=font_tmp)
    current_balance_label.grid(row=1,sticky=W)
    Label(withdraw_screen, text="Amount", font=font_tmp).grid(row=2, sticky=W)
    withdraw_notif=Label(withdraw_screen, font=font_tmp)
    withdraw_notif.grid(row=4,sticky=N, pady=5)
    
    #Entry
    Entry(withdraw_screen,textvariable=withdraw_amount).grid(row=2, column=1)
    #Button
    Button(withdraw_screen, text="Finish", font=font_tmp, command=finish_withdraw).grid(row=3,sticky=W,pady=5)

def finish_withdraw():
    if withdraw_amount.get()=="":
        withdraw_notif.config(text='Amount is required!', fg="red")
        return
    if float(withdraw_amount.get())<=0:
         withdraw_notif.config(text='Negative currency is not accepted :I', fg="red")
         return
     
    file= open(login_number,'r+')
    file_data=file.read()
    details=file_data.split('\n')
    current_balance=details[3]
    
    if float(withdraw_amount.get())>float(current_balance):
        withdraw_notif.config(text="Insufficient Funds (embarrassing..)",fg='red')
        return
    
    updated_balance=current_balance
    updated_balance=float(updated_balance)-float(withdraw_amount.get())
    
    # Update transaction history
    transaction_record = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Withdrawal: -${withdraw_amount.get()}\n"
    file_data = file_data.replace(current_balance, str(updated_balance))
    file_data = file_data.replace("Transaction History:\n", f"Transaction History:\n{transaction_record}")
    
    file.seek(0)
    file.truncate(0)
    file.write(file_data)
    file.close()
    
    current_balance_label.config(text="Current Balance: $"+str(updated_balance),fg="green")
    withdraw_notif.config(text="Balance Updated!",fg="green")

def transaction_history():
    file = open(login_number, 'r')
    file_data = file.read()
    user_details = file_data.split('\n')
    
    # Find the transaction history section
    history_start = file_data.find("Transaction History:")
    if history_start == -1:
        transaction_data = "No transactions found"
    else:
        transaction_data = file_data[history_start + len("Transaction History:"):].strip()
        if not transaction_data:
            transaction_data = "No transactions found"
    
    history_screen = Toplevel(master)
    history_screen.title('Transaction History')
    
    Label(history_screen, text="Transaction History", font=font_tmp).grid(row=0, sticky=N, pady=10)
    
    # Create a text widget with scrollbar
    text_frame = Frame(history_screen)
    text_frame.grid(row=1, sticky=NSEW, padx=10, pady=10)
    
    scrollbar = Scrollbar(text_frame)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    history_text = Text(text_frame, height=15, width=40, wrap=WORD, yscrollcommand=scrollbar.set, font=font_tmp)
    history_text.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=history_text.yview)
    
    history_text.insert(END, transaction_data)
    history_text.config(state=DISABLED)  # read-only
    
    
# Admin password 
adminPass = "AdminPassword:)"

def verify_admin_password():
    entered_password = temp_admin_password.get()
    if entered_password == adminPass:
        password_screen.destroy()
        admin()
    else:
        admin_notif.config(text="Incorrect admin password", fg="red")

def admin_login():
    global temp_admin_password
    global admin_notif
    global password_screen
    
    temp_admin_password = StringVar()
    
    password_screen = Toplevel(master)
    password_screen.title('Admin Authentication')
    
    Label(password_screen, text="Enter Admin Password", font=font_tmp).grid(row=0, sticky=N, pady=10)
    Entry(password_screen, textvariable=temp_admin_password, show='*').grid(row=1, sticky=N, pady=5)
    admin_notif = Label(password_screen, font=font_tmp)
    admin_notif.grid(row=2, sticky=N)
    Button(password_screen, text="Submit", command=verify_admin_password, font=font_tmp).grid(row=3, sticky=N, pady=5)

def admin():
    admin_screen = Toplevel(master)
    admin_screen.title('Admin Panel')
    
    Label(admin_screen, text="Admin Panel", font=font_tmp).grid(row=0, sticky=N, pady=10)
    
    # List all accounts
    all_accounts = os.listdir()
    accounts_list = []
    
    for account in all_accounts:
        if account.isdigit():  
            try:
                with open(account, 'r') as f:
                    account_data = f.read().split('\n')
                    accounts_list.append(f"Account: {account}, Name: {account_data[1]}, Balance: ${account_data[3]}")
            except:
                accounts_list.append(f"Account: {account} (corrupted file)")
    
    # scrollable frame
    canvas = Canvas(admin_screen)
    scrollbar = Scrollbar(admin_screen, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    for i, account_info in enumerate(accounts_list):
        Label(scrollable_frame, text=account_info, font=font_tmp).grid(row=i, sticky=W, padx=5, pady=2)
    
    canvas.grid(row=1, column=0, sticky="nsew")
    scrollbar.grid(row=1, column=1, sticky="ns")
    
    # Account deletion 
    Label(admin_screen, text="Delete Account", font=font_tmp).grid(row=2, sticky=N, pady=10)
    
    global admin_account_number
    global admin_account_name
    admin_account_number = StringVar()
    admin_account_name = StringVar()
    
    Label(admin_screen, text="Account Number:", font=font_tmp).grid(row=3, sticky=W)
    Entry(admin_screen, textvariable=admin_account_number).grid(row=3, column=1)
    
    Label(admin_screen, text="Account Name:", font=font_tmp).grid(row=4, sticky=W)
    Entry(admin_screen, textvariable=admin_account_name).grid(row=4, column=1)
    
    global admin_notif
    admin_notif = Label(admin_screen, font=font_tmp)
    admin_notif.grid(row=6, sticky=N, pady=5)
    
    Button(admin_screen, text="Delete Account", font=font_tmp, command=confirm_delete).grid(row=5, sticky=N, pady=5)

def confirm_delete():
    account_number = admin_account_number.get()
    account_name = admin_account_name.get()
    
    if not account_number or not account_name:
        admin_notif.config(text="Both account number and name are required", fg="red")
        return
    
    if not os.path.exists(account_number):
        admin_notif.config(text="Account not found", fg="red")
        return
    
    # account name matches?
    with open(account_number, 'r') as f:
        file_data = f.read().split('\n')
        if len(file_data) > 1 and file_data[1] != account_name:
            admin_notif.config(text="Account name doesn't match", fg="red")
            return
    
    #  confirm delete?
    confirm_screen = Toplevel(master)
    confirm_screen.title('Confirm Deletion')
    
    Label(confirm_screen, text=f"Are you sure you want to delete account {account_number}?", 
          font=font_tmp).grid(row=0, sticky=N, pady=10)
    Label(confirm_screen, text=f"Name: {account_name}", font=font_tmp).grid(row=1, sticky=N)
    
    def perform_delete():
        try:
            os.remove(account_number)
            admin_notif.config(text="Account deleted successfully", fg="green")
            confirm_screen.destroy()
            admin_screen = master.winfo_children()[1]  # Get the admin screen
            admin_screen.destroy()
            admin()  # Refresh admin panel
        except:
            admin_notif.config(text="Error deleting account", fg="red")
            confirm_screen.destroy()
    
    Button(confirm_screen, text="Confirm Delete", font=font_tmp, command=perform_delete).grid(row=2, sticky=N, pady=5)
    Button(confirm_screen, text="Cancel", font=font_tmp, command=confirm_screen.destroy).grid(row=3, sticky=N, pady=5)
def login():
    global temp_login_number
    global temp_login_password
    global login_notif
    global login_screen
    temp_login_number = StringVar()
    temp_login_password = StringVar()
    
    login_screen = Toplevel(master)
    login_screen.title('Login')
    
    Label(login_screen, text="Login to your account", font=font_tmp).grid(row=0, sticky=N, pady=10)
    Label(login_screen, text="Account Number", font=font_tmp).grid(row=1, sticky=W)
    Label(login_screen, text="PIN (4 digits)", font=font_tmp).grid(row=2, sticky=W)  
    login_notif = Label(login_screen, font=font_tmp)
    login_notif.grid(row=4, sticky=N)
    
    Entry(login_screen, textvariable=temp_login_number).grid(row=1, column=1, padx=5)
    Entry(login_screen, textvariable=temp_login_password, show='*').grid(row=2, column=1, padx=5)
    
    Button(login_screen, text="Login", command=login_session, width=15, font=font_tmp).grid(row=3, sticky=W, pady=5, padx=5)



# image import
img = Image.open('secure1.png')  
img = img.resize((200, 200))  
img = ImageTk.PhotoImage(img)

# Labels 
Label(main_frame, text="Custom Banking Beta", font=font_tmp, bg='#4966eb', fg="white").pack(pady=10)
Label(main_frame, text="Secure banking system", font=font_tmp, bg='#4966eb', fg="white").pack()
Label(main_frame, image=img, bg='#4966eb').pack(pady=20)

# Buttons 
Button(main_frame, text="Register", font=font_tmp, width=25, command=register).pack(pady=10)
Button(main_frame, text="Login", font=font_tmp, width=25, command=login).pack(pady=10)
Button(main_frame, text="Admin Menu", font=font_tmp, width=25, command=admin_login).pack(pady=10)

master.mainloop()
