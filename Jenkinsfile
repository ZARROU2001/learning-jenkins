pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = credentials('dockerhub-credentials')
    }

    stages {
        stage('Prepare Environment') {
            steps {
                sh 'docker system prune -f' // Optional: Clean up Docker environment
                sh "echo ${env.DOCKER_CREDENTIALS_PSW} | docker login -u ${env.DOCKER_CREDENTIALS_USR} --password-stdin"
            }
        }

        stage('Build and Push Microservices') {
            steps {
                script {
                    def microservices = ['auth-service', 'user-service', 'gold-price-service', 'notification-service', 'blockchain-service']

                    microservices.each { service ->
                        dir(service) {
                            echo "Processing ${service}..."

                            // Multi-stage build for optimized Docker image
                            sh "docker build -f Dockerfile -t ${env.DOCKER_CREDENTIALS_USR}/${service}:latest ."

                            // Push Docker image to Docker Hub
                            sh "docker push ${env.DOCKER_CREDENTIALS_USR}/${service}:latest"
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'All microservices have been successfully built and pushed to Docker Hub.'
        }
        failure {
            echo 'An error occurred during the build or push process.'
        }
    }
}
