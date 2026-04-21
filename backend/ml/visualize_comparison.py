import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 10)

print("Loading dataset and training models...")

# Load dataset
df = pd.read_excel("data/Maternal_Health_Risk_Dataset.xlsx")
df.columns = df.columns.str.strip().str.lower()

# Features & label
X = df[['age', 'systolicbp', 'diastolicbp', 'bs', 'bodytemp', 'heartrate']]
y = df['risklevel']
X.fillna(X.mean(), inplace=True)

# Encode label
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# Train models
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)
dt_pred = dt_model.predict(X_test)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)

lr_model = LogisticRegression(max_iter=1000, random_state=42)
lr_model.fit(X_train, y_train)
lr_pred = lr_model.predict(X_test)

# Calculate metrics
models = ['Decision Tree', 'Random Forest', 'Logistic Regression']
predictions = [dt_pred, rf_pred, lr_pred]

accuracy = [accuracy_score(y_test, pred) for pred in predictions]
precision = [precision_score(y_test, pred, average='weighted', zero_division=0) for pred in predictions]
recall = [recall_score(y_test, pred, average='weighted') for pred in predictions]
f1 = [f1_score(y_test, pred, average='weighted') for pred in predictions]

# Create figure with subplots
fig = plt.figure(figsize=(16, 12))

# =====================================================
# 1. BAR CHART - Overall Metrics Comparison
# =====================================================
ax1 = plt.subplot(2, 3, 1)
x = np.arange(len(models))
width = 0.2

bars1 = ax1.bar(x - 1.5*width, accuracy, width, label='Accuracy', color='#2ecc71')
bars2 = ax1.bar(x - 0.5*width, precision, width, label='Precision', color='#3498db')
bars3 = ax1.bar(x + 0.5*width, recall, width, label='Recall', color='#e74c3c')
bars4 = ax1.bar(x + 1.5*width, f1, width, label='F1-Score', color='#f39c12')

ax1.set_xlabel('Models', fontsize=12, fontweight='bold')
ax1.set_ylabel('Score', fontsize=12, fontweight='bold')
ax1.set_title('Performance Metrics Comparison', fontsize=14, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(models, rotation=15, ha='right')
ax1.legend()
ax1.set_ylim([0.85, 1.05])
ax1.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bars in [bars1, bars2, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}', ha='center', va='bottom', fontsize=8)

# =====================================================
# 2. ACCURACY COMPARISON (Larger)
# =====================================================
ax2 = plt.subplot(2, 3, 2)
colors = ['#2ecc71', '#3498db', '#e74c3c']
bars = ax2.barh(models, accuracy, color=colors)
ax2.set_xlabel('Accuracy Score', fontsize=12, fontweight='bold')
ax2.set_title('Accuracy Comparison', fontsize=14, fontweight='bold')
ax2.set_xlim([0.85, 1.05])

for i, (bar, acc) in enumerate(zip(bars, accuracy)):
    ax2.text(acc + 0.005, i, f'{acc*100:.2f}%', va='center', fontweight='bold')

# =====================================================
# 3. CONFUSION MATRIX - Decision Tree
# =====================================================
ax3 = plt.subplot(2, 3, 3)
cm_dt = confusion_matrix(y_test, dt_pred)
sns.heatmap(cm_dt, annot=True, fmt='d', cmap='Greens', 
            xticklabels=le.classes_, yticklabels=le.classes_, ax=ax3)
ax3.set_title('Decision Tree - Confusion Matrix', fontsize=12, fontweight='bold')
ax3.set_ylabel('Actual', fontsize=10)
ax3.set_xlabel('Predicted', fontsize=10)

# =====================================================
# 4. CONFUSION MATRIX - Random Forest
# =====================================================
ax4 = plt.subplot(2, 3, 4)
cm_rf = confusion_matrix(y_test, rf_pred)
sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Blues',
            xticklabels=le.classes_, yticklabels=le.classes_, ax=ax4)
ax4.set_title('Random Forest - Confusion Matrix', fontsize=12, fontweight='bold')
ax4.set_ylabel('Actual', fontsize=10)
ax4.set_xlabel('Predicted', fontsize=10)

# =====================================================
# 5. CONFUSION MATRIX - Logistic Regression
# =====================================================
ax5 = plt.subplot(2, 3, 5)
cm_lr = confusion_matrix(y_test, lr_pred)
sns.heatmap(cm_lr, annot=True, fmt='d', cmap='Reds',
            xticklabels=le.classes_, yticklabels=le.classes_, ax=ax5)
ax5.set_title('Logistic Regression - Confusion Matrix', fontsize=12, fontweight='bold')
ax5.set_ylabel('Actual', fontsize=10)
ax5.set_xlabel('Predicted', fontsize=10)

# =====================================================
# 6. METRICS RADAR CHART
# =====================================================
ax6 = plt.subplot(2, 3, 6, projection='polar')

categories = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
angles += angles[:1]

for i, model in enumerate(models):
    values = [accuracy[i], precision[i], recall[i], f1[i]]
    values += values[:1]
    ax6.plot(angles, values, 'o-', linewidth=2, label=model)
    ax6.fill(angles, values, alpha=0.15)

ax6.set_xticks(angles[:-1])
ax6.set_xticklabels(categories)
ax6.set_ylim(0.85, 1.05)
ax6.set_title('Metrics Radar Chart', fontsize=12, fontweight='bold', pad=20)
ax6.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
ax6.grid(True)

# =====================================================
# SAVE AND SHOW
# =====================================================
plt.tight_layout()
plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
print("\n[SUCCESS] Visualization saved as 'model_comparison.png'")
print("[INFO] Opening visualization...")
plt.show()
