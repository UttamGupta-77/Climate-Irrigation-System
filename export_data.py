import firebase_admin
from firebase_admin import credentials,db
import pandas as pd

cred = credentials.Certificate("smartirrigationsystem-4b612-firebase-adminsdk-fbsvc-5ab717133e.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://smartirrigationsystem-4b612-default-rtdb.asia-southeast1.firebasedatabase.app/'})

ref = db.reference('irrigation_data')
data = ref.get()

df = pd.DataFrame.from_dict(data, orient='index')
df.to_csv('irrigation_data.csv', index=False)
print("data exported")