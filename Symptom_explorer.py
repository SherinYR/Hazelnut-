#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import sqlite3
import hashlib
import os
import matplotlib.pyplot as plt

DB_FILE = "users.db"

# ===================== USER SYSTEM =====================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_users():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
    """)
    conn.commit()

    users = [
        ("admin", hash_password("admin123"), "admin"),
        ("student1", hash_password("password123"), "user"),
        ("student2", hash_password("password123"), "user"),
        ("student3", hash_password("password123"), "user")
    ]

    for u in users:
        try:
            c.execute("INSERT INTO users VALUES (?,?,?)", u)
        except:
            pass
    conn.commit()
    conn.close()

def login():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    u = input("Username: ")
    p = hash_password(input("Password: "))

    c.execute("SELECT role FROM users WHERE username=? AND password=?", (u,p))
    row = c.fetchone()
    conn.close()

    if row:
        print("Login successful.")
        return u, row[0]
    else:
        print("Invalid login.")
        return None, None

# ===================== DATA LOADING =====================

def load_data():
    df = pd.read_csv("synthetic_medical_symptoms_and_diagnosis_dataset.csv")

    symptom_columns = [
        'fever','cough','fatigue','headache','muscle_pain','nausea','vomiting',
        'diarrhea','skin_rash','loss_smell','loss_taste'
    ]

    return df, symptom_columns

# ===================== STATISTICS =====================

def show_stats(df, symptoms):
    print("\nMost common diagnoses:")
    print(df["diagnosis"].value_counts().head())

    print("\nMost common symptoms:")
    for s in symptoms:
        print(s, ":", df[s].sum())

    avg = df[symptoms].sum(axis=1).mean()
    print("\nAverage number of symptoms per patient:", round(avg,2))

# ===================== PLOTS =====================

def plot_symptoms(df, symptoms):
    counts = df[symptoms].sum()
    counts.plot(kind="bar")
    plt.title("Symptom Frequency")
    plt.show()

# ===================== DIAGNOSIS CHECKER =====================

def symptom_checker(df, symptoms):
    user_input = input("Enter symptoms separated by commas: ").lower().split(",")

    scores = {}
    for diag in df["diagnosis"].unique():
        subset = df[df["diagnosis"]==diag]
        score = 0
        for s in user_input:
            s=s.strip()
            if s in symptoms:
                score += subset[s].mean()
        scores[diag]=score

    print("\nLikely diagnoses:")
    for d in sorted(scores,key=scores.get,reverse=True)[:3]:
        print(d)

# ===================== MAIN =====================

def main():
    init_users()
    print("\nSymptom Explorer\n")

    user, role = login()
    if not user:
        return

    df, symptoms = load_data()

    while True:
        print("\n1. View statistics")
        print("2. Plot symptoms")
        print("3. Symptom checker")
        print("4. Exit")

        choice = input("Choose: ")

        if choice=="1":
            show_stats(df, symptoms)
        elif choice=="2":
            plot_symptoms(df, symptoms)
        elif choice=="3":
            symptom_checker(df, symptoms)
        elif choice=="4":
            break

main()

