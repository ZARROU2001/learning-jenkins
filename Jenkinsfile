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
                    def microservices = [
                        'auth_service',
                        'blockchain_interaction_service',
                        'gold-project-service',
                        'notification_service',
                        'user_microservice'
                    ] // Update this list with your actual service directory names

                    microservices.each { service ->
                        dir("backend/${service}") { // Adjust path to match your repository structure
                            echo "Processing ${service}..."

                            // Build the Docker image
                            sh "docker build -f Dockerfile -t ${env.DOCKER_CREDENTIALS_USR}/${service}:latest ."

                            // Push the Docker image to Docker Hub
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
