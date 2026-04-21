import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import joblib

print("=" * 60)
print("ML MODEL COMPARISON - MATERNAL HEALTH RISK PREDICTION")
print("=" * 60)

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
y_encoded = le.fit_transform(y)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

print(f"\nDataset Info:")
print(f"   Total samples: {len(df)}")
print(f"   Training samples: {len(X_train)}")
print(f"   Testing samples: {len(X_test)}")
print(f"   Risk levels: {list(le.classes_)}")

# =====================================================
# MODEL 1: DECISION TREE
# =====================================================
print("\n" + "=" * 60)
print("MODEL 1: DECISION TREE CLASSIFIER")
print("=" * 60)

dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)
dt_pred = dt_model.predict(X_test)

dt_accuracy = accuracy_score(y_test, dt_pred)
dt_precision = precision_score(y_test, dt_pred, average='weighted')
dt_recall = recall_score(y_test, dt_pred, average='weighted')
dt_f1 = f1_score(y_test, dt_pred, average='weighted')

print(f"Accuracy:  {dt_accuracy:.4f} ({dt_accuracy*100:.2f}%)")
print(f"Precision: {dt_precision:.4f}")
print(f"Recall:    {dt_recall:.4f}")
print(f"F1-Score:  {dt_f1:.4f}")

# =====================================================
# MODEL 2: RANDOM FOREST
# =====================================================
print("\n" + "=" * 60)
print("MODEL 2: RANDOM FOREST CLASSIFIER")
print("=" * 60)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)

rf_accuracy = accuracy_score(y_test, rf_pred)
rf_precision = precision_score(y_test, rf_pred, average='weighted')
rf_recall = recall_score(y_test, rf_pred, average='weighted')
rf_f1 = f1_score(y_test, rf_pred, average='weighted')

print(f"Accuracy:  {rf_accuracy:.4f} ({rf_accuracy*100:.2f}%)")
print(f"Precision: {rf_precision:.4f}")
print(f"Recall:    {rf_recall:.4f}")
print(f"F1-Score:  {rf_f1:.4f}")

# =====================================================
# MODEL 3: LOGISTIC REGRESSION
# =====================================================
print("\n" + "=" * 60)
print("MODEL 3: LOGISTIC REGRESSION")
print("=" * 60)

lr_model = LogisticRegression(max_iter=1000, random_state=42)
lr_model.fit(X_train, y_train)
lr_pred = lr_model.predict(X_test)

lr_accuracy = accuracy_score(y_test, lr_pred)
lr_precision = precision_score(y_test, lr_pred, average='weighted')
lr_recall = recall_score(y_test, lr_pred, average='weighted')
lr_f1 = f1_score(y_test, lr_pred, average='weighted')

print(f"Accuracy:  {lr_accuracy:.4f} ({lr_accuracy*100:.2f}%)")
print(f"Precision: {lr_precision:.4f}")
print(f"Recall:    {lr_recall:.4f}")
print(f"F1-Score:  {lr_f1:.4f}")

# =====================================================
# COMPARISON SUMMARY
# =====================================================
print("\n" + "=" * 60)
print("COMPARISON SUMMARY")
print("=" * 60)

comparison = pd.DataFrame({
    'Model': ['Decision Tree', 'Random Forest', 'Logistic Regression'],
    'Accuracy': [dt_accuracy, rf_accuracy, lr_accuracy],
    'Precision': [dt_precision, rf_precision, lr_precision],
    'Recall': [dt_recall, rf_recall, lr_recall],
    'F1-Score': [dt_f1, rf_f1, lr_f1]
})

print("\n" + comparison.to_string(index=False))

# Find best model
best_idx = comparison['Accuracy'].idxmax()
best_model_name = comparison.loc[best_idx, 'Model']
best_accuracy = comparison.loc[best_idx, 'Accuracy']

print("\n" + "=" * 60)
print(f"*** BEST MODEL: {best_model_name} ***")
print(f"   Accuracy: {best_accuracy:.4f} ({best_accuracy*100:.2f}%)")
print("=" * 60)

# =====================================================
# DETAILED CLASSIFICATION REPORT (BEST MODEL)
# =====================================================
print(f"\nDetailed Report for {best_model_name}:")
print("-" * 60)

if best_model_name == 'Decision Tree':
    print(classification_report(y_test, dt_pred, target_names=le.classes_))
    best_model = dt_model
elif best_model_name == 'Random Forest':
    print(classification_report(y_test, rf_pred, target_names=le.classes_))
    best_model = rf_model
else:
    print(classification_report(y_test, lr_pred, target_names=le.classes_))
    best_model = lr_model

# =====================================================
# SAVE BEST MODEL
# =====================================================
joblib.dump(best_model, "model.pkl")
joblib.dump(le, "label_encoder.pkl")

print(f"\n[SUCCESS] Best model ({best_model_name}) saved as model.pkl")
print("[SUCCESS] Label encoder saved as label_encoder.pkl")
print("\n" + "=" * 60)
print("COMPARISON COMPLETE!")
print("=" * 60)
