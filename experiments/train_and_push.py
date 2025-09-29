# experiments/train_and_push.py

import os
import time
import joblib
import numpy as np
import mlflow
import mlflow.sklearn
from dotenv import load_dotenv
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss

# ==============================
# Конфігурація
# ==============================
load_dotenv()
mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
pushgateway_url = "http://pushgateway.monitoring.svc.cluster.local:9091"
experiment_name = "Iris MLflow PushGateway"

# Створюємо експеримент, якщо його немає
experiment = mlflow.get_experiment_by_name(experiment_name)
if experiment is None:
    experiment_id = mlflow.create_experiment(experiment_name)
else:
    experiment_id = experiment.experiment_id

# ==============================
# Дані
# ==============================
data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42
)

# ==============================
# Параметри для запусків
# ==============================
param_grid = [
    {"learning_rate": 0.01, "epochs": 50},
    {"learning_rate": 0.1, "epochs": 100},
    {"learning_rate": 0.05, "epochs": 75}
]

best_accuracy = -1
best_run_id = None
best_model = None

# ==============================
# Цикл запусків
# ==============================
for params in param_grid:
    with mlflow.start_run(experiment_id=experiment_id) as run:
        run_id = run.info.run_id
        lr = params["learning_rate"]
        epochs = params["epochs"]

        mlflow.log_param("learning_rate", lr)
        mlflow.log_param("epochs", epochs)

        model = LogisticRegression(max_iter=epochs, C=1/lr)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)

        acc = accuracy_score(y_test, y_pred)
        loss = log_loss(y_test, y_proba)

        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("loss", loss)
        mlflow.sklearn.log_model(model, "model")

        # PushGateway
        registry = CollectorRegistry()
        acc_gauge = Gauge("mlflow_accuracy", "Accuracy of model", ["run_id"], registry=registry)
        loss_gauge = Gauge("mlflow_loss", "Loss of model", ["run_id"], registry=registry)
        acc_gauge.labels(run_id=run_id).set(acc)
        loss_gauge.labels(run_id=run_id).set(loss)
        push_to_gateway(pushgateway_url, job="mlflow_model", registry=registry)

        print(f"✅ Run {run_id}: acc={acc:.4f}, loss={loss:.4f}")

        if acc > best_accuracy:
            best_accuracy = acc
            best_run_id = run_id
            best_model = model

# ==============================
# Збереження найкращої моделі
# ==============================
os.makedirs("best_model", exist_ok=True)
joblib.dump(best_model, "best_model/model.pkl")
print(f"\n Найкраща модель збережена (run_id={best_run_id}, accuracy={best_accuracy:.4f})")