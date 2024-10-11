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
from tkinter.font import Font

def convert_date(date_str):
    """
    Convertit une chaîne de caractères en objet datetime.
    """
    return datetime.strptime(date_str, '%Y-%m-%d')

def center(window):
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

def search_transactions(positive_var, negative_var, transaction_period_var, person_name_var, transaction_listbox):
    search_criteria = {}

    # Vérifiez les cases à cocher
    if positive_var.get() == 1 and negative_var.get() == 1:
        search_criteria["montant"] = {"$exists": True}
    elif positive_var.get() == 1:
        search_criteria["montant"] = {"$gte": 0}
    elif negative_var.get() == 1:
        search_criteria["montant"] = {"$lt": 0}

    # Critère sur la période
    period = transaction_period_var.get()
    end_date = datetime.now()

    if period != "Tout temps":
        if period == "1 mois":
            start_date = end_date - timedelta(days=30)
        elif period == "3 mois":
            start_date = end_date - timedelta(days=90)
        elif period == "6 mois":
            start_date = end_date - timedelta(days=180)
        elif period == "12 mois":
            start_date = end_date - timedelta(days=365)

        search_criteria["date"] = {"$gte": start_date.strftime('%Y-%m-%d'), "$lte": end_date.strftime('%Y-%m-%d')}

    # Critère sur le nom de la personne
    person_name = person_name_var.get().strip()
    if person_name:
        search_criteria["personne"] = person_name

    # Recherche dans la base de données
    transactions = collection.find(search_criteria)

    # Nettoyage et affichage des résultats
    transaction_listbox.delete(0, END)

    for transaction in transactions:
        # Convertir la date de chaîne en datetime
        transaction_date = convert_date(transaction["date"])
        formatted_date = transaction_date.strftime('%Y-%m-%d')
        listbox_entry = f"Montant: {transaction['montant']:>8} | Raison: {transaction['raison']:<20} | Date: {formatted_date} | Personne: {transaction.get('personne', 'Inconnue')}"
        transaction_listbox.insert(END, listbox_entry)

win = ThemedTk(theme='equilux')
win.title('Gestion des Transactions')
win.minsize(1530, 860)
win.maxsize(1530, 860)
win.resizable(0, 0)
center(win)
win.iconphoto(False, PhotoImage(file='source/icon-3.png'))
win['bg'] = '#464646'

lstbox_Font = Font(win, size=16)

# Connection à MongoDB
try:
    client = MongoClient("mongodb+srv://BDE_O3D:V83wB8kGm@transactions.np7bx.mongodb.net/?retryWrites=true&w=majority&appName=transactions")
    db = client['transactions']
    collection = db['transactions']
except ConnectionError:
    messagebox.showerror("Erreur", "Impossible de se connecter à la base de données.")
    exit()

border_color = "#6A6A6A"
frame_left = ttk.Frame(win, width=400, height=550, relief="flat")
frame_left.grid(row=0, column=0, sticky="sw")
frame_left.grid_propagate(False)

frame_left.grid_columnconfigure(0, weight=0)
frame_left.grid_columnconfigure(1, weight=0)
frame_left.grid_columnconfigure(2, weight=1)

frame_right = ttk.Frame(win, width=1071, height=860, relief="flat")
frame_right.grid(row=0, column=1, sticky="nsew")
frame_right.grid_propagate(False)

positive_var = IntVar(value=1)  
negative_var = IntVar(value=1)  

for widget in frame_left.winfo_children():
    widget.grid_forget()

type_label = ttk.Label(frame_left, text='Type de transactions :')
type_label.grid(row=0, column=0, sticky='w', padx=10, pady=10)

positive_checkbutton = ttk.Checkbutton(frame_left, text="Versements", variable=positive_var)
negative_checkbutton = ttk.Checkbutton(frame_left, text="Débit", variable=negative_var)

positive_checkbutton.grid(row=0, column=1, sticky="nsew")
negative_checkbutton.grid(row=0, column=1, sticky="nsew", padx=100)

# Affichage de l'état du compte
total_amount = sum(transaction['montant'] for transaction in collection.find())

account_status_frame = ttk.Frame(frame_right)
account_status_frame.grid(row=0, column=0, sticky="nw")

account_status_label = ttk.Label(account_status_frame, text="État du compte :", font=('Arial', 14))
account_status_label.grid(row=0, column=0, pady=10, sticky="w")

total_label = ttk.Label(account_status_frame, text=f"Total : {total_amount} €", font=('Arial', 16))
total_label.grid(row=1, column=0, pady=10, sticky="w")

account_status_frame['borderwidth'] = 2
account_status_frame['relief'] = 'flat'

transaction_listbox = Listbox(frame_right, font=lstbox_Font, height=800, width=200, bg='#464646', bd=0, fg="#AFAFAF", highlightbackground="#2F2F2F", relief="flat")
transaction_listbox.grid(row=2, column=0, sticky="se", columnspan=3, rowspan=3)

# Combobox pour la période de transactions
period_label = ttk.Label(frame_left, text='Période de transactions :')
transaction_period_var = StringVar()
period_combobox = ttk.Combobox(frame_left, textvariable=transaction_period_var)
period_combobox['values'] = ("Tout temps", "1 mois", "3 mois", "6 mois", "12 mois")
period_combobox.current(0)
period_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)
period_combobox.grid(row=2, column=1, sticky="w", padx=10, pady=10)

# Champ pour le nom de la personne
person_label = ttk.Label(frame_left, text='Nom de la personne :')
person_label.grid(row=3, column=0, sticky="w", padx=10, pady=10)

person_name_var = StringVar()
person_entry = ttk.Entry(frame_left, textvariable=person_name_var, width=30, font=lstbox_Font)
person_entry.grid(row=3, column=1, sticky="w", padx=10, pady=10)

# Bouton de recherche
search_button = ttk.Button(frame_left, text="Rechercher", command=lambda: search_transactions(positive_var, negative_var, transaction_period_var, person_name_var, transaction_listbox))
search_button.grid(row=5, column=0, sticky="nsew", columnspan=3)

# Affichage initial des transactions
transaction_listbox.delete(0, END)
for transaction in collection.find():
        # Assurez-vous que la date est un objet datetime
        if isinstance(transaction["date"], str):
            transaction_date = datetime.strptime(transaction["date"], '%Y-%m-%d')
        else:
            transaction_date = transaction["date"]  # Doit être un datetime

        formatted_date = transaction_date.strftime('%Y-%m-%d')
        listbox_entry = f"Montant: {transaction['montant']:>8} | Raison: {transaction['raison']:<20} | Date: {formatted_date} | Personne: {transaction.get('personne', 'Inconnue')}"
        transaction_listbox.insert(END, listbox_entry)

win.mainloop()
