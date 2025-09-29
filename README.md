# MLOpsCICD-GitOps-Argo
<!-- gitops repositiry:namespaces/application/nginx.yaml, ns.yaml; namespaces/infra-tools/ns.yaml; readme.md -->

!!! Цей репозиторій пов'язаний з [MLOpsCICD](https://github.com/petroDavydov/MLOpsCICD/tree/lesson-8-9) гілкою lesson-8-9.

## Структура проекту

```
MLOpsCICD-GitOps-Argo/
├── application/
│   ├── nginx-application.yaml
│   ├── mlflow-application.yaml
│   ├── minio-application.yaml  - додано
│   ├── postgres-application.yaml  - додано
│   └── pushgateway-application.yaml   - додано
├── values/
│   ├── nginx-values.yaml
│   ├── mlflow-values.yaml
│   └── pushgateway-values.yaml  - додано
├── namespaces/
│   ├── application/ns.yaml
│   ├── infra-tools/ns.yaml
│   ├── mlflow/ns.yaml
│   └── monitoring/ns.yaml  - додано
├── experiments/
│   ├── train_and_push.py  - додано
│   └── requirements.txt  - додано
├── best_model/
│   └── model.pkl  - додається після запуску train_and_push.py
├── .gitignore
└── README.md  - додано нові зміни в кінці файлу

```


## Запуск terraform

Ці команди ви повинні виконати у папці eks-vps-clucter, по адресу https://github.com/petroDavydov/MLOpsCICD

```
terraform init
terraform plan
terraform apply
```

## Як перевірити, що ArgoCD працює

```
kubectl get pods -n infra-tools
```

## Як відкрити UI ArgoCD

```
kubectl port-forward svc/argocd-server -n infra-tools 8080:443
```

Після цього відкрий у браузері: https://localhost:8080

Логін за замовчуванням:
Username: admin

Password: отримати через команду:

```
kubectl get secret argocd-initial-admin-secret -n infra-tools -o jsonpath="{.data.password}" | base64 -d
```

## Перевірка deploy

```
kubectl get applications -n infra-tools
```

```
kubectl get pods -n application
```

```
kubectl get pods -n mlflow
```

## Як відкрити доступ до nginx

```
kubectl port-forward svc/nginx-app -n application 8081:80
```

* Після цього відкрий у браузері: http://localhost:8081

--------------------------------------------------------------------------------------------------------------------------------


## Деплой mlflow

MLflow деплоїться через Helm-чарт з community-charts.

```
kubectl get applications -n infra-tools
kubectl get pods -n mlflow
```

## Доступ до mlflow

```
kubectl port-forward svc/mlflow-service -n mlflow 5000:5000

```

Ви получите UI для трекінгу експериментів

* Після цього відкрийте у браузері: http://localhost:5000


# Робота з MLFlow та PushGateway


```
cd experiments
python(або python3) train_and_push.py
```

## Перевірка наявності MLFlow та PushGateway у кластері

```
kubectl get svc -n application | grep mlflow
kubectl get svc -n monitoring | grep pushgateway
```

## Порт форвардінг

```
kubectl port-forward svc/mlflow-service -n mlflow 5000:5000 &
kubectl port-forward svc/minio -n application 9000:9000 &
```

## Перевірка метрик

```
kubectl port-forward svc/pushgateway -n monitoring 9091:9091
```

## Перевірка метрик в UI

* Після цього відкрийте у браузері: http://localhost:9091/metrics

Перейти в Grafana → Explore → Prometheus
 Ввести:
  - `mlflow_accuracy`
  - `mlflow_loss`
- Побудувати графік або таблицю



* Можливо при встановлені певних бібліотек вам знадобиться створите віртуальне оточення для роботи команди pip