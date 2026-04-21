import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_excel("data/Maternal_Health_Risk_Dataset.xlsx")


# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Features & label
X = df[['age', 'systolicbp', 'diastolicbp', 'bs', 'bodytemp', 'heartrate']]
y = df['risklevel']

# Handle missing values
X.fillna(X.mean(), inplace=True)

# Encode label
le = LabelEncoder()
y = le.fit_transform(y)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "model.pkl")
joblib.dump(le, "label_encoder.pkl")

print("ML model trained successfully")
