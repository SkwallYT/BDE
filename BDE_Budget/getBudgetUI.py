#####################################################
# Author : DETUNCQ Valentin                         #
#                                                   #
# Retrouver compte dans db 'montant, raison, date'  #
#####################################################

# mongodb+srv://BDE_O3D:V83wB8kGm@transactions.np7bx.mongodb.net/?retryWrites=true&w=majority&appName=transactions

from tkinter import *
from tkinter import ttk, messagebox, StringVar, IntVar
from ttkthemes import ThemedTk
from datetime import datetime, timedelta
from pymongo import MongoClient

def center(window):
    """
    centrer la fenetre
    :param window: la fenetre a centrer
    """
    window.update_idletasks()
    width = window.winfo_width()
    frm_width = window.winfo_rootx() - window.winfo_x()
    win_width = width + 2 * frm_width
    height = window.winfo_height()
    titlebar_height = window.winfo_rooty() - window.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = window.winfo_screenwidth() // 2 - win_width // 2
    y = window.winfo_screenheight() // 2 - win_height // 2
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    window.deiconify()

def search_transactions(transaction_type_var, transaction_period_var, person_name_var, transaction_listbox):
    search_criteria = {}
    
    if transaction_type_var.get() == 0:  
        search_criteria["montant"] = {"$gte": 0}  
    elif transaction_type_var.get() == 1:
        search_criteria["montant"] = {"$lt": 0}  

  
    period = transaction_period_var.get()
    if period != "Tout temps":
        if period == "1 mois":
            start_date = datetime.now() - timedelta(days=30)
        elif period == "3 mois":
            start_date = datetime.now() - timedelta(days=90)
        elif period == "6 mois":
            start_date = datetime.now() - timedelta(days=180)
        elif period == "12 mois":
            start_date = datetime.now() - timedelta(days=365)

        search_criteria["date"] = {"$gte": start_date}

    person_name = person_name_var.get().strip()
    if person_name:
        search_criteria["personne"] = person_name

    transactions = collection.find(search_criteria)

    transaction_listbox.delete(0, END)

    for transaction in transactions:
        
        transaction_date = datetime.strptime(transaction["date"], '%Y-%m-%d')
        formatted_date = transaction_date.strftime('%d-%m-%Y')
        listbox_entry = f"Montant: {transaction['montant']}, Raison: {transaction['raison']}, Date: {formatted_date}, Personne: {transaction.get('personne', 'Inconnue')}"
        transaction_listbox.insert(END, listbox_entry)


win = ThemedTk(theme='equilux')

win.title('Gestion des Transactions')
win.minsize(1530, 860)
win.maxsize(1530, 860)
win.resizable(0, 0)
center(win)
win.iconbitmap('source/icon.ico')
win['bg'] = '#4F4F4F'

# Connection a MongoDB
try:
    client = MongoClient("mongodb+srv://BDE_O3D:V83wB8kGm@transactions.np7bx.mongodb.net/?retryWrites=true&w=majority&appName=transactions")
    db = client['transactions']
    collection = db['transactions']
except ConnectionError:
    messagebox.showerror("Erreur", "Impossible de se connecter à la base de données.")
    exit()

# Ajout dans la db pour le debug
# transaction = {
#      "id": 2,  # Identifiant personnalisé
#      "montant": -150,
#      "raison": "Test d'initiation de db",
#      "date": datetime.now().strftime('%Y-%m-%d'),
#      "personne": "Maxime"  # Ajout de la date actuelle
# }
#
# collection.insert_one(transaction)

transactions = collection.find()
for trans in transactions:
    print(trans)

border_color = "#6A6A6A"
frame_left = ttk.Frame(win, width=459, height=860, relief="flat")
frame_left.grid(row=0, column=0, sticky="nsew")
frame_left.grid_propagate(False)

frame_right = ttk.Frame(win, width=1071, height=860, relief="flat")
frame_right.grid(row=0, column=1, sticky="nsew")
frame_right.grid_propagate(False)

radio_label = ttk.Label(frame_left, text='Type de transaction :')

transaction_type = IntVar()
positive_button = ttk.Radiobutton(frame_left, text="Versements", variable=transaction_type, value=0)
negative_button = ttk.Radiobutton(frame_left, text="Débit", variable=transaction_type, value=1)

radio_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
positive_button.grid(row=0, column=1, sticky="w", padx=10, pady=10)
negative_button.grid(row=0, column=2, sticky="w", padx=10, pady=10)

transaction_listbox = Listbox(frame_right, height=860, width=200, bg='#464646')
transaction_listbox.grid(row=0, column=0, sticky="e")

period_label = ttk.Label(frame_left, text='Periode de transactions :')
transaction_period_var = StringVar()
period_combobox = ttk.Combobox(frame_left, textvariable=transaction_period_var)
period_combobox['values'] = ("Tout temps", "1 mois", "3 mois", "6 mois", "12 mois")
period_combobox.current(0)
period_label.grid(row=1, column=0, columnspan=1, sticky="w", padx=10, pady=10)
period_combobox.grid(row=1, column=1, columnspan=2, sticky="w", padx=10, pady=10)

person_label = ttk.Label(frame_left, text='Nom de la personne :')
person_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)

person_name_var = StringVar()
person_entry = ttk.Entry(frame_left, textvariable=person_name_var, width=30)
person_entry.grid(row=2, column=1, columnspan=2, sticky="w", padx=10, pady=10)

search_button = ttk.Button(frame_left, text="Rechercher", width=75 , command=lambda: search_transactions(transaction_type, transaction_period_var, person_name_var, transaction_listbox))
search_button.grid(row=4, column=0, sticky="nsew", columnspan=3)

transactions = collection.find()

transaction_listbox.delete(0, END)

for transaction in transactions:
    transaction_date = datetime.strptime(transaction["date"], '%Y-%m-%d')
    formatted_date = transaction_date.strftime('%d-%m-%Y')
    listbox_entry = f"Montant: {transaction['montant']}, Raison: {transaction['raison']}, Date: {formatted_date}, Personne: {transaction.get('personne', 'Inconnue')}"
    transaction_listbox.insert(END, listbox_entry)

win.mainloop()
