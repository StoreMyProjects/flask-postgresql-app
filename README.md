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

## To destroy resources in one go.
```
terraform destroy --auto-approve
```