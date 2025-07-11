pipeline {
    // Agent defines where the pipeline will run. 'any' means any available agent.
    // For more control, you could specify a Docker image for the agent itself:
    // agent { docker { image 'python:3.9-slim-buster' } }
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Ensure the correct branch and URL are used.
                // Using 'scm' automatically checks out the configured repository for the pipeline.
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image, tagging with BUILD_NUMBER and 'latest'
                    sh "docker build -t user-service-py:${env.BUILD_NUMBER} ."
                    sh "docker tag user-service-py:${env.BUILD_NUMBER} user-service-py:latest"
                    // If pushing to a registry (for later exercises):
                    // sh "docker push user-service-py:${env.BUILD_NUMBER}"
                    // sh "docker push user-service-py:latest"
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Run unit tests inside a temporary container derived from the built image.
                    // --rm ensures the container is removed after it exits.
                    sh "docker run --rm user-service-py:${env.BUILD_NUMBER} python -m unittest discover"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Stop and remove any existing container instance of this service.
                    // '|| true' prevents the pipeline from failing if the container doesn't exist.
                    sh "docker stop user-service-container || true"
                    sh "docker rm user-service-container || true"

                    // Run the new container in detached mode (-d)
                    // Map host port 5001 to container port 5001
                    sh "docker run -d -p 5001:5001 --name user-service-container user-service-py:${env.BUILD_NUMBER}"

                    echo "User Service deployed on port 5001"
                    echo "Access it at http://<Your-Jenkins-Host-IP>:5001 (or localhost if Jenkins is local)"
                }
            }
        }
    }

    post {
        always {
            // Clean up the Jenkins workspace after every build.
            cleanWs()
        }
        success {
            echo "Pipeline for User Service completed successfully!"
        }
        failure {
            echo "Pipeline for User Service failed. Check console output for errors."
        }
        // You can add 'unstable', 'aborted' blocks for more fine-grained post-build actions.
    }
}
