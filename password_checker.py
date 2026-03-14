import tkinter as tk
from tkinter import messagebox
import string
import hashlib
import json
import os

# File to store user data
USER_FILE = "users.json"

# Load existing users
if os.path.exists(USER_FILE):
    with open(USER_FILE, "r") as f:
        users = json.load(f)
else:
    users = {}

# Function to check missing password rules
def check_password(password):
    rules = []
    if len(password) < 8:
        rules.append("At least 8 characters")
    if not any(c.isupper() for c in password):
        rules.append("At least 1 uppercase letter")
    if not any(c.islower() for c in password):
        rules.append("At least 1 lowercase letter")
    if not any(c.isdigit() for c in password):
        rules.append("At least 1 number")
    if not any(c in string.punctuation for c in password):
        rules.append("At least 1 special character")
    return rules

# Function to calculate password strength
def password_strength(password):
    score = 0
    if len(password) >= 8: score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1

    if score <= 2:
        return "Weak", "red"
    elif score <= 4:
        return "Medium", "orange"
    else:
        return "Strong", "green"

# Handle signup
def signup():
    username = entry_username.get()
    password = entry_password.get()

    if username in users:
        messagebox.showerror("Error", "Username already exists!")
        return

    rules_missing = check_password(password)
    if rules_missing:
        feedback = "Password must contain:\n- " + "\n- ".join(rules_missing)
        messagebox.showwarning("Weak Password", feedback)
        return

    # Hash and save
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    users[username] = password_hash
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

    messagebox.showinfo("Success", "Account created successfully!")
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    label_strength.config(text="Strength: ", fg="white")  # reset strength label

# GUI setup
root = tk.Tk()
root.title("Sign-Up Page")
root.configure(bg="#1e1e1e")  # dark minimal background
root.geometry("500x400")      # slightly bigger window
root.resizable(False, False)

# Center frame
frame = tk.Frame(root, bg="#1e1e1e")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

tk.Label(frame, text="Sign Up", font=("Helvetica", 20), fg="white", bg="#1e1e1e").grid(row=0, column=0, columnspan=2, pady=(0,20))

tk.Label(frame, text="Username:", fg="white", bg="#1e1e1e").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_username = tk.Entry(frame, width=25)
entry_username.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Password:", fg="white", bg="#1e1e1e").grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_password = tk.Entry(frame, show="*", width=25)
entry_password.grid(row=2, column=1, padx=5, pady=5)

# Strength label
label_strength = tk.Label(frame, text="Strength: ", fg="white", bg="#1e1e1e")
label_strength.grid(row=2, column=2, padx=10, pady=5)

# Bind password entry to update strength dynamically
def update_strength_label(event):
    pw = entry_password.get()
    strength, color = password_strength(pw)
    label_strength.config(text=f"Strength: {strength}", fg=color)

entry_password.bind("<KeyRelease>", update_strength_label)

btn_signup = tk.Button(frame, text="Sign Up", width=20, command=signup, bg="#4a90e2", fg="white", relief="flat")
btn_signup.grid(row=3, column=0, columnspan=2, pady=20)

# Required password rules below in red
rules_text = "Password must contain:\n- At least 8 characters\n- 1 uppercase letter\n- 1 lowercase letter\n- 1 number\n- 1 special character"
tk.Label(root, text=rules_text, fg="red", bg="#1e1e1e", justify="left").pack(side="bottom", pady=10)

root.mainloop()