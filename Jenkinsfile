pipeline {
    // Executes on the main Jenkins agent for SCM checkout, then hands off to Docker agents
    agent any 

    // Define environment variables
    environment {
        // --- Custom Variables ---
        DOCKER_HUB_ID = 'RatnPriya03' 
        IMAGE_NAME = 'aceest-fitness'
        // FIX: Use GString interpolation (double quotes) for dynamic variable creation
        IMAGE_TAG = "1.0.${new Date().format('yyyyMMdd.HHmmss')}"
        
        // --- Jenkins Credentials/Tools IDs ---
        // MUST match the IDs you created in Jenkins -> Manage Credentials
        DOCKER_CREDENTIAL_ID = 'docker-hub-cred-id' 
        
        // --- SonarQube Configuration ---
        SONAR_PROJECT_KEY = 'aceest-fitness'
        SONAR_TOOL_NAME = 'SonarScanner' 
        SONAR_SERVER_NAME = 'SonarQube' 
    }

    stages {
        stage('Checkout Code') {
            steps {
                // SCM checkout happens automatically at the start, but we can explicitly call it here too.
                checkout scm
            }
        }

        stage('Run Unit Tests (Pytest)') {
            // FIX: Use a stage-specific Docker agent to ensure Python/pip is available
            agent {
                docker {
                    image 'python:3.9-slim' 
                }
            }
            steps {
                echo 'Installing Python dependencies...'
                sh 'pip install -r requirements.txt' 
                echo 'Running Pytest...'
                sh 'pytest' 
            }
        }

        stage('SonarQube Scan') {
            // Use the same Python agent environment for a clean scan
            agent {
                docker {
                    image 'python:3.9-slim' 
                }
            }
            steps {
                echo 'Starting SonarQube analysis...'
                withSonarQubeEnv(SONAR_SERVER_NAME) { 
                    // Point to the SonarScanner tool installed globally in Jenkins
                    tool name: SONAR_TOOL_NAME, type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                    
                    // Execute the scan
                    sh "sonar-scanner \
                        -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://localhost:9000"
                }
            }
        }
        
        stage('Quality Gate Check') {
            steps {
                echo 'Waiting for SonarQube Quality Gate result...'
                timeout(time: 5, unit: 'MINUTES') { 
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    echo 'Building and tagging Docker image...'
                    
                    // Use the Docker Hub credential 
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIAL_ID}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USER')]) {
                        
                        // 1. Build and Tag
                        sh "docker build -t ${DOCKER_HUB_ID}/${IMAGE_NAME}:${IMAGE_TAG} ."
                        sh "docker tag ${DOCKER_HUB_ID}/${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_HUB_ID}/${IMAGE_NAME}:latest"
                        
                        // 2. Log in and Push
                        echo 'Pushing image to Docker Hub...'
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
                echo 'Applying Kubernetes deployment (Rolling Update)...'
                
                // Use 'sed' to inject the newly built image tag into the k8s YAML file
                sh 'sed -i "s|LATEST_TAG_TO_BE_REPLACED|${DOCKER_HUB_ID}/${IMAGE_NAME}:${IMAGE_TAG}|g" k8s/deployment.yaml'
                
                // Apply the deployment and service files
                sh 'kubectl apply -f k8s/service.yaml'
                sh 'kubectl apply -f k8s/deployment.yaml'
                
                // Reset the YAML file to the placeholder for the next run (Good practice)
                sh 'sed -i "s|${DOCKER_HUB_ID}/${IMAGE_NAME}:${IMAGE_TAG}|LATEST_TAG_TO_BE_REPLACED|g" k8s/deployment.yaml'
                
                echo "Application deployed to Kubernetes with tag ${IMAGE_TAG}"
            }
        }
    }
}