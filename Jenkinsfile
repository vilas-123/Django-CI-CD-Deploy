pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        IMAGE_NAME = 'vilas12/ticket-booking-app'
    }

    stages {

        stage('Clone') {
            steps {
                echo 'Cloning from GitHub...'
                git branch: 'main',
                    url: 'https://github.com/vilas-123/Django-CI-CD-Deploy.git'
            }
        }

        stage('Install and Test') {
            steps {
                echo 'Running Django tests...'
                sh '''
                    python3 -m pip install -r requirements.txt --break-system-packages
                    python3 manage.py test
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
            }
        }

        stage('Push to DockerHub') {
            steps {
                echo 'Pushing to DockerHub...'
                sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying on EC2...'
                sh '''
                    docker stop ticket-app || true
                    docker rm ticket-app || true
                    docker run -d \
                        --name ticket-app \
                        -p 8000:8000 \
                        vilas12:latest
                '''
            }
        }
    }

    post {
        success {
            echo 'Ticket booking app is live!'
        }
        failure {
            echo 'Pipeline failed! Check logs above.'
        }
    }
}