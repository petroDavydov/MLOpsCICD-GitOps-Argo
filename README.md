# MLOpsCICD-GitOps-Argo
<!-- gitops repositiry:namespaces/application/nginx.yaml, ns.yaml; namespaces/infra-tools/ns.yaml; readme.md -->

!!! Цей репозиторій пов'язаний з [MLOpsCICD](https://github.com/petroDavydov/MLOpsCICD/tree/lesson-7) гілкою lesson-7.

## Структура проекту

```
MLOpsCICD-GitOps-Argo/
├── application/
│   ├── nginx-application.yaml
│   └── mlflow-application.yaml
├── values/
│   ├── nginx-values.yaml
│   └── mlflow-values.yaml
├── namespaces/
│   ├── application/ns.yaml
│   ├── infra-tools/ns.yaml
│   └── mlflow/ns.yaml
├── .gitignore
└── README.md


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