pipeline {
    agent any
    

    environment {
        DOCKER_CREDS = credentials('dockerhub-creds')
        BEST_ACC = credentials('best-accuracy')
    }

    stages {

        stage('Checkout') {
            steps {
                git credentialsId: 'git-creds',
                    url: 'https://github.com/2022BCS0185-MaheswarReddy/Mlops-Lab2.git'
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                . venv/bin/activate
                python train.py
                '''
            }
        }

        stage('Read Accuracy') {
            steps {
                script {
                    ACCURACY = sh(
                        script: "jq '.r2' artifacts/metrics.json",
                        returnStdout: true
                    ).trim()
                    echo "Current Accuracy: ${ACCURACY}"
                }
            }
        }

        stage('Compare Accuracy') {
            steps {
                script {
                    echo "Best Accuracy: ${BEST_ACC}"
                    if (ACCURACY.toFloat() <= BEST_ACC.toFloat()) {
                        echo "Model did NOT improve "
                        currentBuild.result = 'SUCCESS'
                        env.SKIP_DOCKER = "true"
                    } else {
                        echo "Model Improved "
                    }
                }
            }
        }

        stage('Build Docker Image') {
            when {
                expression { env.SKIP_DOCKER != "true" }
            }
            steps {
                sh '''
                docker build -t mahesh2022bcs0185/lab6:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Push Docker Image') {
            when {
                expression { env.SKIP_DOCKER != "true" }
            }
            steps {
                sh '''
                echo $DOCKER_CREDS_PSW | docker login -u $DOCKER_CREDS_USR --password-stdin
                docker push mahesh2022bcs0185/lab6:${BUILD_NUMBER}
                docker tag mahesh2022bcs0185/lab6:${BUILD_NUMBER} mahesh2022bcs0185/lab6:latest
                docker push mahesh2022bcs0185/lab6:latest
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'artifacts/**'
        }
    }
}
