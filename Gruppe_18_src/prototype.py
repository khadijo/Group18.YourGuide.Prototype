import tkinter as tk
from tkinter import messagebox


def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "o" and password == "o":
        messagebox.showinfo("Velkommen", "Innlogging vellykket!")
        go_to_main_page()
    else:
        messagebox.showerror("Feil", "Feil brukernavn eller passord. Prøv igjen.")

def go_to_main_page():
    # Fjern innloggingskomponentene fra vinduet
    username_label.destroy()
    username_entry.destroy()
    password_label.destroy()
    password_entry.destroy()
    login_button.destroy()

    # Opprett komponenter for hovedsiden (flyreisebestillingssystem)
    welcome_label = tk.Label(root, text="Velkommen til YourGuide for Guided Turer", pady=5, padx=5)
    root.configure(bg="pink")
    welcome_label.pack()


root = tk.Tk()
root.title("YourGuide for Guided Turer")
root.configure(bg="grey")
root.geometry("800x500")

username_label = tk.Label(root, text="Brukernavn:", justify='left', padx=2, pady=2, bg='lightgrey')
username_label.pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack()
password_label = tk.Label(root, text="Passord:", justify='left', padx=2, pady=2, bg='lightgrey')
password_label.pack(pady=5)
password_entry = tk.Entry(root, show="*")  # Viser passord som stjerner
password_entry.pack()

login_button = tk.Button(root, text="Logg inn", command=login)
login_button.pack(pady=5)

root.mainloop()
