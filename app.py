import tkinter as tkr
from frame import ScrollableFrame
from tkinter.messagebox import askokcancel, WARNING, showinfo, INFO, ERROR

#######################################3#
#LOGIKA
#########################################

def log_in_check(username: str, password: str):#returns entry if login successful, empty str if unsuccesful
    with open("users.txt") as db:
        users = db.readlines()
    for user in users:
        if user.split(";")[0] == username and user.split(";")[1] == password:
            return user
    return ""



def get_trip_title(trip_id: int):#returns str containing given trips title
    with open("wyjazd.txt") as db:
        trips = db.readlines()
    for trip in trips:
        if int(trip.split(";")[0]) == trip_id:
            return trip.split(";")[2]

def get_expenses_for_trip(trip_id: int):#returns list of tuples:(name of user declaring an expense, list of expense-related data: name|amount|status|id)
    with open("wydatki.txt") as db:
        expenses = db.readlines()
    result = []
    for expense in expenses:
        expense_split = expense.split(";")
        if int(expense_split[0]) == trip_id:
            result.append((get_user_data_from_id(int(expense_split[1]))[3],[expense_split[2],expense_split[3],expense_split[4],int(expense_split[5])]))
    return result


def get_user_data_from_id(user_id: int):#returns str list containing split user data login|pass|id|full name
    with open("users.txt") as db:
        users = db.readlines()
    for user in users:
        user_split = user.split(";")
        user_split[3] = user_split[3].strip()
        if int(user_split[2]) == user_id:
            return user_split

def get_trip_admin(trip_id: int):#returns int id of given trips admin
    with open("wyjazd.txt") as db:
        trips = db.readlines()
    for trip in trips:
        if int(trip.split(";")[0]) == trip_id:
            return int(trip.split(";")[1])

def get_user_list_for_trip(trip_id: int):#returns int list of all user ids in given trip
    with open("wyjazd.txt") as db:
        trips = db.readlines()
    with open("users.txt") as db:
        users = db.readlines()
    for trip in trips:
        if trip_id == int(trip.split(";")[0]):
            trip_users = [int(i) for i in trip.split(";")[3].split(",")]
            break
    result = []
    for user in users:
        if int(user.split(";")[2]) in trip_users:
            result.append(int(user.split(";")[2]))
    return result

def get_trip_data_list_for_user(user_id: int):#returns tuple  of lists (int,str) ([ids],[names])
    with open("wyjazd.txt") as db:
        trips = db.readlines()
    result_ids = []
    result_names = []
    for trip in trips:
        trip_split = trip.split(";")
        user_list = get_user_list_for_trip(int(trip_split[0]))
        if user_id in user_list:
            result_ids.append(int(trip_split[0]))
            result_names.append(trip_split[2])
    return (result_ids,result_names)

def get_user_id_from_entry(entry: str):#returns int id of user under given entry
    return int(entry.split(";")[2])

def get_avaiable_trip_id():#returns first avaiable id for a trip
    with open("wyjazd.txt") as db:
        trips = db.readlines()
    return int(trips[-1].split(";")[0])+1


def create_new_trip(user:str,name:str,new_id:int):#creates a new trip with given user as admin
    user_id = user.split(";")[2]
    with open("wyjazd.txt","a") as db:
        db.write(str(new_id)+";"+user_id+";"+name+";"+user_id+"\n")

def get_expense_data(expense_id: int):#returns a list containing data for given expense [userid,name,amount,status]
    with open("wydatki.txt") as db:
        expenses = db.readlines()
    for expense in expenses:
        expense_split = expense.split(";")
        if expense_id == int(expense_split[5]):
            return [int(expense_split[1]),expense_split[2],expense_split[3],expense_split[4]]

def accept(expense_id: int):#asks for confirmation and eventually accepts the expense
    answer = askokcancel(title="Potwierdzenie",message="Czy na pewno chcesz zaakceptowac ten wydatek?",icon=WARNING)
    if answer:
        with open("wydatki.txt") as db:
            expenses = db.readlines()
        new_expenses = []
        for expense in expenses:
            expense_split = expense.split(";")
            if expense_id == int(expense_split[5]):
                to_append = expense_split[0] + ";" + expense_split[1] + ";" + expense_split[2] + ";" + expense_split[3] + ";Z;" + expense_split[5]
            else:
                to_append = expense
            new_expenses.append(to_append)
        with open("wydatki.txt","w") as db:
            for line in new_expenses:
                db.write(line)

def get_avaiable_expense_id():#returns first aviable id for an expense
    with open("wydatki.txt") as db:
        expenses = db.readlines()
    return int(expenses[-1].split(";")[5])+1

def create_new_expense(user_id: int, trip_id: int, expense_name: str, expense_amount: str, is_admin: bool):#asks for confirmation and eventually creates a new expense
    answer = askokcancel(title="Potwierdzenie",message="Czy na pewno chcesz dodac ten wydatek?",icon=WARNING)
    if answer:
        if is_admin:
            status = "Z"
        else:
            status = "NZ"
        expense = str(trip_id) + ";" + str(user_id) + ";" + expense_name + ";" + expense_amount + ";" + status + ";" + str(get_avaiable_expense_id()) + "\n"
        with open("wydatki.txt","a") as db:
            db.write(expense)
        if is_admin:
            showinfo(title="Dodano",message="Dodano nowy wydatek.",icon=INFO)
        else:
            showinfo(title="Dodano",message="Dodano nowy wydatek. Czeka on na zaakceptowanie",icon=INFO)

def add_user_to_trip(user_id: int, trip_id: int):#adds given user to given trip
    answer = askokcancel(title="Potwierdzenie",message="Czy na pewno chcesz dodac tego uzytkownika?",icon=WARNING)
    if answer:
        with open("wyjazd.txt") as db:
            trips = db.readlines()
        new_trips = []
        for trip in trips:
            trip_split = trip.split(";")
            if int(trip_split[0]) != trip_id:
                new_trips.append(trip)
            else:
                new_trips.append(trip.strip() + "," + str(user_id) + "\n")
        with open("wyjazd.txt","w") as db:
            for line in new_trips:
                db.write(line)
        showinfo(title="Dodano",message="Dodano nowego uczestnika.",icon=INFO)

        

def check_if_amount_correct(amount: str):#returns true if amount is correct
    try:
        amount = float(amount)
        if amount > 0:
            return True
        else:
            return False
    except ValueError:
        return False

def check_if_user_in_db_and_not_in_trip(user_id: str, trip_id: int):#returns true if user is correct and can be added to trip, false if not
    try:
        user_id = int(user_id)
        with open("users.txt") as db:
            users = db.readlines()
        for user in users:
            if int(user.split(";")[2]) == user_id and user_id not in get_user_list_for_trip(trip_id):
                return True
        return False
    except ValueError:
        return False
        

#########################################
#INTERFEJS#
##########################################


#KONKRETNY WYDATEK

def specific_expense(welcome_text: str,expense_id: int, trip_id: int, entry: str):
    global main_window
    global main_frame
    main_frame.destroy()
    main_frame = tkr.Frame(main_window,bg="white")
    main_frame.pack(expand=True,fill=tkr.BOTH)
    welcome_label = tkr.Label(main_frame,text=welcome_text,bd=10,bg="blue",font=('Calibri', 12,'normal'),wraplengt=400)
    welcome_label.pack(anchor=tkr.N)

    expense_data = get_expense_data(expense_id)
    added_by = get_user_data_from_id(expense_data[0])[3]
    if expense_data[3] == "Z":
        status = "Zaakceptowany"
    else:
        status = "Niezaakceptowany"

    name_label = tkr.Label(main_frame,borderwidth=2,highlightbackground="black",text="Wydatek: " + expense_data[1])
    name_label.pack(anchor=tkr.N,padx=10,pady=10)

    amount_label = tkr.Label(main_frame,borderwidth=2,highlightbackground="black",text="Koszt: " + expense_data[2])
    amount_label.pack(anchor=tkr.N,padx=10,pady=10)

    user_label = tkr.Label(main_frame,borderwidth=2,highlightbackground="black",text="Dodany przez: " + added_by)
    user_label.pack(anchor=tkr.N,pady=10,padx=10)

    status_label = tkr.Label(main_frame,borderwidth=2,highlightbackground="black",text="Status: " + status)
    status_label.pack(anchor=tkr.N,padx=10,pady=10)

    if expense_data[3] != "Z" and get_user_id_from_entry(entry) == get_trip_admin(trip_id):
        accept_button = tkr.Button(main_frame,width=8,height=2,text="Zaakceptuj",command=lambda:[accept(expense_id)])
        accept_button.pack(anchor=tkr.N,pady=10,padx=10)

    back_button = tkr.Button(main_frame,width=8,height=2,text="Powrot",command=lambda:[expense_list(welcome_text,trip_id,entry)])
    back_button.pack(anchor=tkr.N,padx=10,pady=10)



#LISTA UCZESTNIKOW


def user_list(welcome_text: str,entry: str, trip_id: int):
    global main_window
    global main_frame
    main_frame.destroy()
    main_frame = tkr.Frame(main_window,bg="white")
    main_frame.pack(expand=True,fill=tkr.BOTH)
    welcome_label = tkr.Label(main_frame,text=welcome_text,bd=10,bg="blue",font=('Calibri', 12,'normal'),wraplengt=400)
    welcome_label.pack(anchor=tkr.N)
    for user in get_user_list_for_trip(trip_id):
        user_data = get_user_data_from_id(user)
        if get_trip_admin(trip_id) == int(user_data[2]):
            color = "red"
        else:
            color = "black"
        temp = tkr.Label(main_frame,text=user_data[3],bd=3,bg="white",foreground=color,font=("Calibri",11,"normal"))
        temp.pack(anchor=tkr.N)
    back_button = tkr.Button(main_frame,text="Powrot",width=10,height=2,command=lambda:[main_menu(entry,trip_id)])
    back_button.pack(anchor=tkr.N)


#DODAWANIE WYDATKU

def add_expense(welcome_text: str, trip_id: int, entry: str, is_admin: bool):
    global main_window
    global main_frame
    main_frame.destroy()
    main_frame = tkr.Frame(main_window,bg="white")
    main_frame.pack(expand=True,fill=tkr.BOTH)
    welcome_label = tkr.Label(main_frame,text=welcome_text,bd=10,bg="blue",font=('Calibri', 12,'normal'),wraplengt=400)
    welcome_label.pack(anchor=tkr.N)
    
    title_label = tkr.Label(main_frame,text="Dodawanie wydatku")
    title_label.pack(anchor=tkr.N,pady=30)

    name_text = tkr.Entry(main_frame,width=30)
    name_text.insert(tkr.END,"nazwa")
    name_text.pack(anchor=tkr.N,pady=10)

    amount_text = tkr.Entry(main_frame,width=30)
    amount_text.insert(tkr.END,"cena")
    amount_text.pack(anchor=tkr.N,pady=10)

    def check():
        if check_if_amount_correct(amount_text.get()):
            create_new_expense(get_user_id_from_entry(entry),trip_id,name_text.get(),amount_text.get(),is_admin)
            expense_list(welcome_text,trip_id,entry)
        else:
            showinfo(title="Blad",message="Niepoprawna cena",icon=ERROR)


    confirm_button = tkr.Button(main_frame,width=10,height=2,text="Dodaj",command=lambda:check())
    confirm_button.pack(anchor=tkr.N,pady=40)

    back_button = tkr.Button(main_frame,text="Powrot",width=10,height=2,command=lambda: main_menu(entry,trip_id))
    back_button.pack(anchor=tkr.N)

#LISTA WYDATKOW

def expense_list(welcome_text: str, trip_id: int, entry: str):
    global main_window
    global main_frame
    main_frame.destroy()
    main_frame = tkr.Frame(main_window,bg="white")
    main_frame.pack(expand=True,fill=tkr.BOTH)
    welcome_label = tkr.Label(main_frame,text=welcome_text,bd=10,bg="blue",font=('Calibri', 12,'normal'),wraplengt=400)
    welcome_label.pack(anchor=tkr.N)
    scrollable = ScrollableFrame(main_frame)
    scrollable.pack(anchor=tkr.N,fill=tkr.BOTH,expand=True)
    left_frame = tkr.Frame(scrollable.scrollable_frame,borderwidth=2,relief=tkr.SOLID,highlightbackground="black")
    right_frame = tkr.Frame(scrollable.scrollable_frame,borderwidth=2,relief=tkr.SOLID,highlightbackground="black")
    left_frame.grid(column=0,row=0,sticky=tkr.W)
    right_frame.grid(column=1,row=0,sticky="nsew")

    left_upper_frame = tkr.Frame(left_frame,bg="grey")
    left_upper_frame.pack(anchor=tkr.N,fill=tkr.X)
    right_upper_frame = tkr.Frame(right_frame,bg="grey")
    right_upper_frame.pack(anchor=tkr.N,fill=tkr.X)

    left_label = tkr.Label(left_upper_frame,text="Uczestnik",bd=3,bg="grey",font=("Calibri",11,"normal"))
    left_label.pack(anchor=tkr.N,fill=tkr.X,padx=50)
    right_label = tkr.Label(right_upper_frame,text="Wydatek",bd=3,bg="grey",font=("Calibri",11,"normal"))
    right_label.pack(anchor=tkr.N,fill=tkr.X,padx=50)
    
    
    for expense in get_expenses_for_trip(trip_id):
        user_label = tkr.Label(left_frame,text=expense[0].strip())
        def make_lambda(x):
            return lambda ev: specific_expense(welcome_text,x,trip_id,entry)
        user_label.bind("<Button-1>",make_lambda(expense[1][3]))
        user_label.pack(anchor=tkr.N)
        expense_label = tkr.Label(right_frame,text=expense[1][0] + ", " + expense[1][1] + "zł, " + expense[1][2])
        expense_label.bind("<Button-1>",make_lambda(expense[1][3]))
        expense_label.pack(anchor=tkr.N)
    back_button = tkr.Button(main_frame,text="Powrot",width=10,height=2,command=lambda:[main_menu(entry,trip_id)])
    back_button.pack(anchor=tkr.N)
    
#DODAWANIE UZYTKOWANIKA (TYLKO DLA KIEROWNIKA)


def add_user(welcome_text: str, entry: str, trip_id: int):
    global main_window
    global main_frame
    main_frame.destroy()
    main_frame = tkr.Frame(main_window,bg="white")
    main_frame.pack(expand=True,fill=tkr.BOTH)
    welcome_label = tkr.Label(main_frame,text=welcome_text,bd=10,bg="blue",font=('Calibri', 12,'normal'),wraplengt=400)
    welcome_label.pack(anchor=tkr.N)
    add_user_entry = tkr.Entry(main_frame, width=10)
    add_user_entry.insert(tkr.END,"id")
    add_user_entry.pack(anchor=tkr.N,pady=20)

    def check():
        if check_if_user_in_db_and_not_in_trip(add_user_entry.get(),trip_id):
            add_user_to_trip(int(add_user_entry.get()),trip_id)
            main_menu(entry, trip_id)
        else:
            showinfo(title="Blad",message="Niepoprawne id uczestnika",icon=ERROR)


    confirm_button = tkr.Button(main_frame,text="Dodaj",height=2,width=10,command=lambda:check())
    confirm_button.pack(anchor=tkr.N)
    back_button = tkr.Button(main_frame,text="Powrot",width=10,height=2,command=lambda:[main_menu(entry,trip_id)])
    back_button.pack(anchor=tkr.N,pady=10)
    

#GŁÓWNE MENU PO ZALOGOWANIU

def main_menu(entry:str,trip_id:int):
    global main_window
    global main_frame
    main_frame.destroy()
    main_frame = tkr.Frame(main_window,bg="white")
    main_frame.pack(expand=True,fill=tkr.BOTH)
    user_data = entry.split(";")
    user_data[2] = int(user_data[2])


    trip_admin = get_trip_admin(trip_id)
    trip_title = get_trip_title(trip_id)


    
    if trip_admin == user_data[2]:
        placeholder1 = "kierownikiem"
        is_admin = True
    else:
        placeholder1 = "uczestnikiem"
        is_admin = False
    
    welcome_text = "Witaj! " + user_data[3].strip() + "! Jesteś " + placeholder1 + " wyjazdu " + trip_title


    welcome_label = tkr.Label(main_frame,text=welcome_text,bd=10,bg="blue",font=('Calibri', 12,'normal'),wraplengt=400)
    welcome_label.pack(anchor=tkr.N)

    expense_list_button = tkr.Button(main_frame,text="Lista wydatkow",width=30,height=5,command=lambda:[expense_list(welcome_text,trip_id,entry)])
    expense_list_button.pack(anchor=tkr.N,padx=5,pady=5)

    add_expense_button = tkr.Button(main_frame,text="Dodaj wydatek",width=30,height=5,command=lambda:[add_expense(welcome_text,trip_id,entry,is_admin)])
    add_expense_button.pack(anchor=tkr.N,padx=5,pady=5)

    user_list_button = tkr.Button(main_frame,text="Lista uczestnikow",width=30,height=5,command=lambda:[user_list(welcome_text,entry,trip_id)])
    user_list_button.pack(anchor=tkr.N,padx=5,pady=5)

    if is_admin:
        add_user_button = tkr.Button(main_frame,text="Dodaj uczestnika",width=30,height=5,command=lambda:[add_user(welcome_text,entry,trip_id)])
        add_user_button.pack(anchor=tkr.N,padx=5,pady=5)
    
    log_out_button = tkr.Button(main_frame,text="Wyloguj",height=5,width=30,command=lambda:[start_app()])
    log_out_button.pack(anchor=tkr.N,padx=5,pady=5)


#LOGOWANIE

def log_in(username:str, password:str):
    global main_window
    global main_frame

    logged = False
    

    entry = log_in_check(username,password)

    if entry != "":
        logged = True
        

    err_label = tkr.Label()

    if not logged:
        err_label = tkr.Label(main_frame,text="Zły login lub hasło",bd=10,bg="red",font=('Calibri', 18,'bold'))
        err_label.pack(anchor=tkr.N,pady=5)
    else:
        welcome_label = tkr.Label(main_frame,text="Zalogowano! Twoje id to " + str(get_user_id_from_entry(entry)))
        welcome_label.pack(anchor=tkr.N,pady=5)
        trips = get_trip_data_list_for_user(get_user_id_from_entry(entry))
        avaiable_ids = trips[0]
        avaiable_trips = trips[1]
        
        if len(avaiable_trips) != 0:
            chosen_trip = tkr.StringVar()
            chosen_trip.set(avaiable_trips[0])
            menu = tkr.OptionMenu(main_frame,chosen_trip,*avaiable_trips)
            menu.pack(anchor=tkr.N,pady=5)
            go_button = tkr.Button(main_frame,text="Wybierz",width=10,height=2,command=lambda:[main_menu(entry,int(avaiable_ids[avaiable_trips.index(chosen_trip.get())]))])
            go_button.pack(anchor=tkr.N,pady=5)
        
        or_label = tkr.Label(main_frame,text="Stwórz nowy wyjazd",bd=10,bg="white",font=('Calibri', 18,'bold'))
        or_label.pack(anchor=tkr.N,pady=5)
        trip_name = tkr.StringVar()
        new_trip = tkr.Entry(main_frame,width=30,textvariable=trip_name)
        new_trip.pack(anchor=tkr.N,pady=5)
        next_avaiable_id = get_avaiable_trip_id()
        new_button = tkr.Button(main_frame,text="Stworz",width=10,height=2,command=lambda:[create_new_trip(entry,trip_name.get(),next_avaiable_id),main_menu(entry,next_avaiable_id)])
        new_button.pack(anchor=tkr.N,pady=5)




#EKRAN STARTOWY


def start_app():
    global main_window
    global main_frame
    main_frame.destroy()
    main_frame = tkr.Frame(main_window,bg="white")
    main_frame.pack(expand=True,fill=tkr.BOTH)
    username = tkr.StringVar()
    password = tkr.StringVar()
    welcome_label = tkr.Label(main_frame,text="Witaj! Zaloguj się aby przejść dalej",bd=10,bg="blue",font=('Calibri', 18,'bold'))
    welcome_label.pack(anchor=tkr.N)

    login_label = tkr.Label(main_frame,text="Login",bd=10,bg="white",font=('Calibri', 13,'bold'))
    login_label.pack(anchor=tkr.N)
    login_text = tkr.Entry(main_frame,width=30,textvariable=username)
    login_text.pack(anchor=tkr.N)

    pass_label = tkr.Label(main_frame,text="Hasło",bd=10,bg="white",font=('Calibri', 13,'bold'))
    pass_label.pack(anchor=tkr.N)
    pass_text = tkr.Entry(main_frame,width=30,textvariable=password,show="*")
    pass_text.pack(anchor=tkr.N)

    login = tkr.Button(main_frame,text="Login",width=10,height=2,command=lambda:[log_in(username.get(),password.get())])
    login.pack(anchor=tkr.N)

    main_window.mainloop()


#INICJACJA APLIKACJI

if __name__ == "__main__":
    main_window = tkr.Tk()
    main_window.title("Wyjazdy grupowe")
    main_window.geometry("400x600")
    main_frame = tkr.Frame(main_window,bg="white")
    main_frame.pack(expand=True,fill=tkr.BOTH)
    start_app()