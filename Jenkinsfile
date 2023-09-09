def img
pipeline {
    agent any
    
    environment {
        registry = 'amrendra01/flask-app'
        registryCredential = 'docker-hub-login'
        dockerImg = ''
        }
    
    stages {
        stage('Clean workspace'){
            steps{
                cleanWs disableDeferredWipeout: true, deleteDirs: true
            }
        }
        stage('Build Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/amrendra01/tourX.git']]])
            }
        }
        stage('Build Image') {
            steps {
                script {
                    img = registry + ":$BUILD_ID"
                    // img = registry
                    dockerImg = docker.build("${img}")
                }
            }
        }
        stage('Publish Build') {
            steps {
                script {
                    docker.withRegistry('', registryCredential) {
                        dockerImg.push()
                    }
                }
            }
        }
        stage('Update deployment file') {
            steps {
                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'GITHUB_TOKEN')]) {
                    sh '''
                    pwd
                    sed "s/img_tag/$BUILD_ID/g" deployment-service.yaml-tmpl > deployment-service.yaml
                    cat deployment-service.yaml
                    
                    git config --global user.name amrendrasngh
                    git config --global user.email singhamrendra1999@gmail.com
                    
                    git add deployment-service.yaml
                    git commit -m "Update deployment version"
                    git push https://${GITHUB_TOKEN}@github.com/amrendrasngh/tourX HEAD:main
                    '''
                 }
            }
        }
        stage('Deploy to Kubernetes cluster') {
            steps {
                kubernetesDeploy configs: 'deployment-service.yaml', kubeConfig: [path: ''], kubeconfigId: 'eks-kube', secretName: '', ssh: [sshCredentialsId: '*', sshServer: ''], textCredentials: [certificateAuthorityData: '', clientCertificateData: '', clientKeyData: '', serverUrl: 'https://']
            }
        }
    }
}
