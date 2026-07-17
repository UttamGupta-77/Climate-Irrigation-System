# 🌱 Climate Smart Irrigation System

An AI-powered Smart Irrigation System that predicts irrigation requirements using Machine Learning and provides a user-friendly web interface built with Flask. The application integrates with Firebase Realtime Database to store irrigation records and enables efficient monitoring and management of irrigation decisions.

---

## 📌 Features

- 🌾 Predicts irrigation requirements using a trained Machine Learning model
- 💧 Supports climate-based irrigation decision making
- 🔥 Firebase Realtime Database integration
- 🌐 Interactive Flask web application
- 📊 Stores historical irrigation records
- 📁 Export irrigation data
- ⚡ Fast and lightweight prediction model

---

## 🛠️ Tech Stack

- Python
- Flask
- Scikit-learn
- Pandas
- NumPy
- Firebase Admin SDK
- HTML
- CSS
- JavaScript
- Joblib

---

## 📂 Project Structure

```
Climate-Irrigation-System/
│
├── templates/
│   └── index.html
│
├── app.py
├── train_model.py
├── export_data.py
├── irrigation_model.pkl
├── status_encoder.pkl
├── irrigation_data.csv
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/UttamGupta-77/Climate-Irrigation-System.git
```

### Navigate to the project

```bash
cd Climate-Irrigation-System
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Firebase Configuration

Download your Firebase Admin SDK JSON file and place it in the project directory.

Update the filename inside `app.py` if necessary.

### Run the application

```bash
python app.py
```

---

## 📈 Machine Learning Workflow

1. Collect irrigation dataset
2. Preprocess the data
3. Train the Machine Learning model
4. Save the trained model using Joblib
5. Load the model into the Flask application
6. Predict irrigation requirements
7. Store prediction results in Firebase

---

## 📷 Screenshots

Add screenshots here after uploading the project.

Example:

```
images/
    home.png
    prediction.png
    firebase.png
```

---

## 🔮 Future Improvements

- IoT Sensor Integration
- Weather API Integration
- Crop Recommendation System
- Mobile Application
- Email/SMS Notifications
- Dashboard Analytics

---

## 👨‍💻 Author

**Uttam Gupta**

GitHub: https://github.com/UttamGupta-77

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.