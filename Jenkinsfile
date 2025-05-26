pipeline {
    agent any

    environment {
        AWS_REGION       = 'ap-south-1'
        AWS_ACCOUNT_ID   = '343218198881'
        ECR_REPOSITORY   = 'testwebsite'
        ECR_REGISTRY     = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        IMAGE_TAG        = "${env.BUILD_ID}"
        IMAGE_URI        = "${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}"
        CREDENTIALS_ID   = 'aws-ecr-cred'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/Spike741/chatbot.git'
            }
        }

        stage('Configure AWS Credentials') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: "${env.CREDENTIALS_ID}",
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    script {
                        bat "aws configure set aws_access_key_id %AWS_ACCESS_KEY_ID%"
                        bat "aws configure set aws_secret_access_key %AWS_SECRET_ACCESS_KEY%"
                        bat "aws configure set default.region ${env.AWS_REGION}"
                        bat 'aws sts get-caller-identity'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${env.IMAGE_URI}")
                }
            }
        }

        stage('Login to ECR and Push Image') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: "${env.CREDENTIALS_ID}",
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    script {
                        bat "aws ecr get-login-password --region ${env.AWS_REGION} | docker login --username AWS --password-stdin ${env.ECR_REGISTRY}"
                        docker.image("${env.IMAGE_URI}").push()
                    }
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully! Docker image pushed to ECR and deployed to EC2.'
        }
        failure {
            echo '❌ Pipeline failed! Check the logs for errors.'
        }
    }
}
