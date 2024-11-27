# flask-postgesql-app
This deploys flask app and postgres db docker containers on a Kubernetes cluster.

## Prerequisites

### Install kubectl on Amazon Linux 2
```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
kubectl version --short --client
```

### Install awscli on Amazon Linux 2
```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
```
#### Configure awscli on AL2 by executing below command on terminal and then enter your AWS IAM user's Access key, Secret key, AWS default region and press enter to select default values for other inputs.
```
aws configure
```

### Install Terraform on Amazon Linux 2
```
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
sudo yum install terraform
terraform version
```

### Download github repo to create eks cluster using terraform scripts (you can modify/add variables as per your requirements)
```
git clone https://github.com/hashicorp/learn-terraform-provision-eks-cluster/
cd learn-terraform-provision-eks-cluster
terraform init
terraform plan
terraform apply --auto-approve
aws eks --region <your-aws-region> update-kubeconfig --name <output.cluster_name>
```

### Install ArgoCD on your eks cluster.
```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v2.13.1/manifests/install.yaml
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

### Get ArgoCD admin user password to login from UI
```
kubectl get secrets argocd-initial-admin-secret -n argocd -o yaml
```
### To decode encrypted password - replace below password with actual password
```
echo password | base64 --decode
```

### Create ArgoCD applications using below yaml files or you can create them directly from UI.
```
cd k8s-manifests/argocd-apps
kubectl apply -f db.yaml -n argocd
kubectl apply -f app.yaml -n argocd
```

## Monitoring and Observability

## Install Helm
```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

### Install Prometheus and Grafana on your eks cluster.
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
kubectl create namespace monitoring
helm install prometheus prometheus-community/prometheus --n monitoring
helm install grafana grafana/grafana -n monitoring
```

### Expose Prometheus and Grafana services
```
kubectl expose svc/prometheus-server --type NodePort --target-port 9090 --name prometheus-server-ext -n monitoring
kubectl expose svc/grafana --type NodePort --target-port 3000 --name grafana-ext -n monitoring
kubectl port-forward svc/prometheus-server-ext 9090:80 -n monitoring
kubectl port-forward svc/grafana-ext 3000:80 -n monitoring
```

### Get Grafana admin user password to login from UI
```
kubectl get secrets grafana -n monitoring -o yaml
```
### Create Prometheus Datasource in Grafana by adding prometheus server url and now you're ready to create dashboards.

## To destroy resources in one go.
```
terraform destroy --auto-approve
```