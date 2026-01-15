# Diabetes Prediction Using Logistic Regression

## Project Overview
This project focuses on **early detection of diabetes risk** using machine learning.  
The goal is **screening support**, where **missing a diabetic patient (False Negative)** is far more costly than flagging healthy one (False Positive).

Hence, the project focuses on **high recall** over raw accuracy

# Methodology

### Exploratory Data Analysis (EDA)
- Checked class imbalance
- Analyzed feature distribution
- Identified medically relevant patterns

---

### Baseline Model
- **Model**: Logistic Regression
- **Purpose**: Establish reference performance
- **observation**: High recall but weak class seperation (low roc_auc_score)

Baseline Metrics:
- Recall = **0.86**
- ROC_AUC = **0.59**

### Feature Engineering
Added medically meaningful features such as:
- metabolic risk interactions
- Lifestyle-related risk combinations
- Non-linear feature interactions

Result:
- Improved class separation
- More stable predictions

Metrics:
- Recall = **0.84**
- ROC_AUC = **0.60**

### Hyperparameter Tuning (GridSearchCV)
- Model: Logistic Regression (`solver='saga'`)
- Handled class imbalance using `class_weight='balanced'`
- Optimized for **ROC-AUC**, not accuracy

Metrics after hyperparameter tuning:
- Recall = **0.59**
- ROC_AUC = **0.63**

After hyperparameter tuning the model is not blindly prediction diabetes which reduces recall but give good separation

GridSearchCV optimizes model parameters using a **fixed threshold (0.5)**, which can reduce recall.  
Therefore, **threshold tuning was performed separately**.

### Threshold Optimization
Since this is a **screening problem**, threshold tuning was used to maximize recall.
| Threshold | Recall | Precision |
|---------|--------|-----------|
| 0.50 | ~0.60 | ~0.75 |
| 0.30 | ~0.95 | ~0.65 |
| **0.25** | **~0.98** | **~0.64** |
| 0.20 | ~0.99 | ~0.63 |

**Final Chosen Threshold: 0.25**
Justification:
- Misses very few diabetic patients
- False positives are acceptable due to low-cost confirmatory tests

## Final Model Summary
- **Model**: Logistic Regression
- **Optimization Metric**: ROC_AUC
- **Decision Threshold**: 0.25
- **Primary Metrics**: Recall

## Final Performance
- **Recall**: ~98%
- **ROC-AUC**: ~0.63
- **Precision**: ~64%

## Streamlit Web Application

This project includes an interactive Streamlit web application for diabetes risk prediction.
The app allows users to enter lifestyle, and health-related information and returns the predicted probability of diabetes along with model insights.

### To Run the Application locally 
- Train the model and save it using joblib
- Run the app using `streamlit run app.py`