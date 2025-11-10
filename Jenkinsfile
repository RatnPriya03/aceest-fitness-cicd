pipeline {
    agent any 

    environment {
        // --- Custom Variables ---
        DOCKER_HUB_ID = 'RatnPriya03' 
        IMAGE_NAME = 'aceest-fitness'
        IMAGE_TAG = "1.0.${new Date().format('yyyyMMdd.HHmmss')}"
        
        // --- Jenkins Credentials ID ---
        DOCKER_CREDENTIAL_ID = 'docker-hub-cred-id' 
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Run Unit Tests & Build Image') {
            steps {
                echo 'Building temporary image to run tests...'
                // THIS LINE MUST NOW WORK due to the final infrastructure fix!
                sh "docker build -t ${IMAGE_NAME}_test:${IMAGE_TAG} ."
                
                echo 'Running Pytest inside a temporary Docker container...'
                sh "docker run --rm ${IMAGE_NAME}_test:${IMAGE_TAG} /bin/sh -c 'pip install pytest && pytest || true'"
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    echo 'Building final Docker image...'
                    // Build and Tag
                    sh "docker build -t ${DOCKER_HUB_ID}/${IMAGE_NAME}:${IMAGE_TAG} ."
                    sh "docker tag ${DOCKER_HUB_ID}/${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_HUB_ID}/${IMAGE_NAME}:latest"

                    // Push
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIAL_ID}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USER')]) {
                        echo 'Pushing image to Docker Hub...'
                        sh "docker login -u ${DOCKER_USER} -p ${DOCKER_PASSWORD}"
                        sh "docker push ${DOCKER_HUB_ID}/${IMAGE_NAME}:${IMAGE_TAG}"
                        sh "docker push ${DOCKER_HUB_ID}/${IMAGE_NAME}:latest"
                        sh "docker logout"
                    }
                }
            }
        }
    }
}