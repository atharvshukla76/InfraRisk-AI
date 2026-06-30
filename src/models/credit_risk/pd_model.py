import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc
import shap
import joblib
import os

class CreditRiskModel:
    """
    XGBoost model for predicting the Probability of Default (PD) for infrastructure projects.
    """
    def __init__(self, model_dir="data/models"):
        self.model = None
        self.model_dir = model_dir
        os.makedirs(self.model_dir, exist_ok=True)
        self.features = []

    def train(self, df: pd.DataFrame, target_col: str = 'default_flag'):
        """
        Trains the XGBoost model.
        df should contain preprocessed numerical features and the binary target.
        """
        if target_col not in df.columns:
            raise ValueError(f"Target column '{target_col}' not found in dataframe.")
            
        y = df[target_col]
        X = df.drop(columns=[target_col])
        self.features = X.columns.tolist()
        
        # Split data (time-aware split or random depending on dataset, assuming random for now)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        # Calculate scale_pos_weight for imbalanced datasets (defaults are usually rare)
        pos_weight = (len(y_train) - sum(y_train)) / sum(y_train) if sum(y_train) > 0 else 1.0
        
        # Initialize model
        self.model = xgb.XGBClassifier(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=5,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=pos_weight,
            objective='binary:logistic',
            eval_metric='auc',
            random_state=42
        )
        
        print("Training XGBoost PD Model...")
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_train, y_train), (X_test, y_test)],
            verbose=False
        )
        
        # Evaluate
        preds_proba = self.model.predict_proba(X_test)[:, 1]
        roc_auc = roc_auc_score(y_test, preds_proba)
        
        # PR AUC (better for imbalanced)
        precision, recall, _ = precision_recall_curve(y_test, preds_proba)
        pr_auc = auc(recall, precision)
        
        print(f"Model Training Complete. ROC-AUC: {roc_auc:.4f}, PR-AUC: {pr_auc:.4f}")
        return {"roc_auc": roc_auc, "pr_auc": pr_auc}
        
    def predict_pd(self, df: pd.DataFrame) -> np.ndarray:
        """
        Predicts Probability of Default for new data.
        """
        if self.model is None:
            raise ValueError("Model is not trained or loaded.")
            
        # Ensure column order matches
        X = df[self.features]
        return self.model.predict_proba(X)[:, 1]
        
    def explain(self, df: pd.DataFrame):
        """
        Generates SHAP values for model interpretability.
        Returns the explainer and shap values.
        """
        if self.model is None:
            raise ValueError("Model is not trained or loaded.")
            
        X = df[self.features]
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(X)
        return explainer, shap_values

    def save(self, filename="pd_xgboost.pkl"):
        """Saves the model to disk."""
        if self.model is None:
            raise ValueError("No model to save.")
        
        path = os.path.join(self.model_dir, filename)
        joblib.dump({'model': self.model, 'features': self.features}, path)
        print(f"Model saved to {path}")
        
    def load(self, filename="pd_xgboost.pkl"):
        """Loads the model from disk."""
        path = os.path.join(self.model_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file not found: {path}")
            
        data = joblib.load(path)
        self.model = data['model']
        self.features = data['features']
        print(f"Model loaded from {path}")

if __name__ == "__main__":
    # Synthetic test
    np.random.seed(42)
    dummy_data = pd.DataFrame({
        'dscr_avg': np.random.uniform(0.8, 2.5, 1000),
        'gearing': np.random.uniform(0.3, 0.9, 1000),
        'country_risk_score': np.random.uniform(1, 10, 1000),
        'gdp_growth': np.random.uniform(-3, 8, 1000),
        'default_flag': np.random.binomial(1, 0.05, 1000)
    })
    
    # Introduce some correlation so the model learns something
    dummy_data.loc[dummy_data['dscr_avg'] < 1.0, 'default_flag'] = 1
    
    model = CreditRiskModel()
    metrics = model.train(dummy_data)
    model.save()
