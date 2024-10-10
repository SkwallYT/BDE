#####################################################
# Author : DETUNCQ Valentin                         #
#                                                   #
# Retrouver compte dans db 'montant, raison, date'  #
#####################################################

from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter.simpledialog import *
from tkinter import messagebox
import sqlite3
import os

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

# Create Window
win = ThemedTk(theme='equilux')

# Window parameter
win.title('Retrouver versements')
win.minsize(1530,860)
center(win)
win.iconbitmap('source/icon.ico')
win['bg'] = '#4F4F4F'

# Charger la db
if not os.path.exists('data'):
    os.mkdir('data')
    
if not os.path.exists('data/money_history.db'):
    a = sqlite3.connect('data/money_history.db')
    a.commit()
    a.close()
    
mh_db = sqlite3.connect('data/money_history.db')

ttk.Button(win, text='Hello World !').pack()


win.mainloop()