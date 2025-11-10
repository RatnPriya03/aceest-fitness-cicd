pipeline {
    // Agent is set to 'any' to use the default Jenkins executor.
    agent any 

    // Define environment variables
    environment {
        // --- Custom Variables ---
        DOCKER_HUB_ID = 'RatnPriya03' 
        IMAGE_NAME = 'aceest-fitness'
        // FIX: Using GString interpolation (double quotes) for dynamic variable creation
        IMAGE_TAG = "1.0.${new Date().format('yyyyMMdd.HHmmss')}"
        
        // --- Jenkins Credentials/Tools IDs ---
        DOCKER_CREDENTIAL_ID = 'docker-hub-cred-id' 
        
        // --- SonarQube Configuration ---
        SONAR_PROJECT_KEY = 'aceest-fitness'
        SONAR_TOOL_NAME = 'SonarScanner' 
        SONAR_SERVER_NAME = 'SonarQube' 
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Run Unit Tests (Pytest) in Docker') {
            steps {
                echo 'Building temporary image to run tests...'
                // Build a temporary image based on your Dockerfile/app for testing
                sh "docker build -t ${IMAGE_NAME}_test:${IMAGE_TAG} ."
                
                echo 'Running Pytest inside a temporary Docker container...'
                // Run the pytest tests inside the built image
                sh "docker run --rm ${IMAGE_NAME}_test:${IMAGE_TAG} /bin/sh -c 'pip install pytest && pytest'"
            }
        }

        stage('SonarQube Scan') {
            steps {
                echo 'Starting SonarQube analysis...'
                withSonarQubeEnv(SONAR_SERVER_NAME) { 
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
                    echo 'Building final Docker image...'
                    
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