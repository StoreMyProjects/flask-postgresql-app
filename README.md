# flask-postgesql-app
This deploys flask app and postgres db on kubernetes cluster using docker images.

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

### Clone this repo and navigate to flask-postgres-app/k8s-manifests and execute below commands
```
kubectl create namespace flaskpro
kubectl apply -f db-secrets.yaml -n flaskpro
kubectl apply -f db-configmap.yaml -n flaskpro
kubectl apply -f db-deployment.yaml -n flaskpro
kubectl apply -f db-service.yaml -n flaskpro

kubectl get svc -n flaskpro
```
#### Copy cluster-ip of postgres svc and edit app-deployment.yaml and replace DB_HOST value with it.
```
kubectl apply -f app-deployment.yaml -n flaskpro
kubectl apply -f app-service.yaml -n flaskpro

kubectl get svc -n flaskpro
```

### Copy external-ip of app svc paste it on browser window with it's service port - external-ip:port

#### Some basic kubernetes commands used for debugging pods
```
kubectl get pods -n namespace
kubectl logs pod_name -n namespace
kubectl exec -it pod_name -n namespace -- /bin/bash
```
