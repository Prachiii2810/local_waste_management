import sqlite3
import pandas as pd

# Connect to database file
conn = sqlite3.connect('food_waste_management.db')
cursor = conn.cursor()

# Enable foreign key constraint support in SQLite
cursor.execute("PRAGMA foreign_keys = ON;")

# 1. Create Providers Schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS Providers (
    Provider_ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Type TEXT,
    Address TEXT,
    City TEXT,
    Contact TEXT
)''')

# 2. Create Receivers Schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS Receivers (
    Receiver_ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Type TEXT,
    City TEXT,
    Contact TEXT
)''')

# 3. Create Food Listings Schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS Food_Listings (
    Food_ID INTEGER PRIMARY KEY,
    Food_Name TEXT NOT NULL,
    Quantity INTEGER NOT NULL,
    Expiry_Date TEXT,
    Provider_ID INTEGER,
    Provider_Type TEXT,
    Location TEXT,
    Food_Type TEXT,
    Meal_Type TEXT,
    FOREIGN KEY(Provider_ID) REFERENCES Providers(Provider_ID) ON DELETE CASCADE
)''')

# 4. Create Claims Schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS Claims (
    Claim_ID INTEGER PRIMARY KEY,
    Food_ID INTEGER,
    Receiver_ID INTEGER,
    Status TEXT DEFAULT 'Pending',
    Timestamp TEXT,
    FOREIGN KEY(Food_ID) REFERENCES Food_Listings(Food_ID) ON DELETE CASCADE,
    FOREIGN KEY(Receiver_ID) REFERENCES Receivers(Receiver_ID) ON DELETE CASCADE
)''')
conn.commit()

# Load the Kaggle dataframes into the database
pd.read_csv('providers_data.csv').to_sql('Providers', conn, if_exists='append', index=False)
pd.read_csv('receivers_data.csv').to_sql('Receivers', conn, if_exists='append', index=False)
pd.read_csv('food_listings_data.csv').to_sql('Food_Listings', conn, if_exists='append', index=False)
pd.read_csv('claims_data.csv').to_sql('Claims', conn, if_exists='append', index=False)

print("🚀 Relational database successfully generated from Kaggle datasets!")
conn.close()
