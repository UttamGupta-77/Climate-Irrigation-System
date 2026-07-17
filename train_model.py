import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from joblib import dump

df = pd.read_csv('irrigation_data.csv')

encoder = LabelEncoder()
df['irrigation_status'] = encoder.fit_transform(df['irrigation_status'])


X = df[['temperature', 'humidity', 'soil_moisture']]
y = df['irrigation_status']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


dump(model, 'irrigation_model.pkl')
dump(encoder, 'status_encoder.pkl')

print("✅ Model trained and saved as irrigation_model.pkl")
