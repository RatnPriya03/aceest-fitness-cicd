pipeline {
    agent any 

    // Define environment variables
    // Define environment variables
    environment {
        // --- Custom Variables ---
        DOCKER_HUB_ID = 'RatnPriya03' 
        IMAGE_NAME = 'aceest-fitness'
        // FIX: Wrap the entire dynamic expression in double quotes
        IMAGE_TAG = "1.0.${new Date().format('yyyyMMdd.HHmmss')}"
        
        // --- Jenkins Credentials/Tools IDs ---
        DOCKER_CREDENTIAL_ID = 'docker-hub-cred-id' // ID of your Docker Hub Credential
        SONAR_PROJECT_KEY = 'aceest-fitness'
        SONAR_TOOL_NAME = 'SonarScanner' // Name from Global Tool Configuration
        SONAR_SERVER_NAME = 'SonarQube' // Name from Configure System
    }
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Run Unit Tests (Pytest)') {
            steps {
                sh 'pip install -r requirements.txt' 
                sh 'pytest' // Execute your Pytest suite
            }
        }

        stage('SonarQube Scan') {
            steps {
                // Run scan using the configured SonarQube server and tool
                withSonarQubeEnv(SONAR_SERVER_NAME) { 
                    tool name: SONAR_TOOL_NAME, type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                    sh "sonar-scanner -Dsonar.projectKey=${SONAR_PROJECT_KEY} -Dsonar.sources=. -Dsonar.host.url=http://localhost:9000"
                }
            }
        }
        
        stage('Quality Gate Check') {
            steps {
                // Wait for the Quality Gate result from SonarQube
                timeout(time: 5, unit: 'MINUTES') { 
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    // Use the Docker Hub credential 
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIAL_ID}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USER')]) {
                        // 1. Build the image
                        sh "docker build -t ${DOCKER_HUB_ID}/${IMAGE_NAME}:${IMAGE_TAG} ."
                        sh "docker tag ${DOCKER_HUB_ID}/${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_HUB_ID}/${IMAGE_NAME}:latest"
                        
                        // 2. Log in and Push
                        sh "docker login -u ${DOCKER_USER} -p ${DOCKER_PASSWORD}"
                        sh "docker push ${DOCKER_HUB_ID}/${IMAGE_NAME}:${IMAGE_TAG}"
                        sh "docker push ${DOCKER_HUB_ID}/${IMAGE_NAME}:latest"
                        sh "docker logout"
                    }
                }
            }
        }

        stage('Kubernetes Deployment (Rolling Update)') {
            steps {
                // Use 'envsubst' to replace the placeholder tag in the k8s YAML before applying.
                sh 'sed -i "s|LATEST_TAG_TO_BE_REPLACED|${DOCKER_HUB_ID}/${IMAGE_NAME}:${IMAGE_TAG}|g" k8s/deployment.yaml'
                
                // Apply the deployment and service files
                sh 'kubectl apply -f k8s/deployment.yaml'
                sh 'kubectl apply -f k8s/service.yaml'
                
                // Reset the YAML file to the placeholder for the next run
                sh 'sed -i "s|${DOCKER_HUB_ID}/${IMAGE_NAME}:${IMAGE_TAG}|LATEST_TAG_TO_BE_REPLACED|g" k8s/deployment.yaml'
                
                echo "Application deployed to Kubernetes with tag ${IMAGE_TAG}"
            }
        }
    }
}