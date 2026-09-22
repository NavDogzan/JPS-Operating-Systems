import pickle

with open("cred.dat", "wb") as file:
    pickle.dump("password123", file)

with open("cred.dat", "rb") as file:
    password = pickle.load(file)

print(password)
