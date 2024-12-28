pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.11'
        VENV = 'venv'
        GITHUB_REPO = 'https://github.com/AhmadHanif12/Final-Exam.git'
    }
    
    options {
        // This will check for new commits every time
        skipDefaultCheckout(true)
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                cleanWs()
                git branch: 'master',
                    url: "${env.GITHUB_REPO}"
            }
        }
        
        stage('Setup Python') {
            steps {
                script {
                    // Delete existing venv if it exists
                    bat 'if exist venv rmdir /s /q venv'
                    
                    // Create and activate new venv with error handling
                    bat '''
                        python -m pip install --upgrade pip
                        python -m virtualenv venv
                        pip install -r requirements.txt
                        pip install requests pytest pytest-flask urllib3
                    '''
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    bat '''
                    '''
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    bat '''
                        python app.py
                    '''
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline succeeded! Application is deployed.'
        }
        failure {
            echo 'Pipeline failed! Check the logs for details.'
        }
        always {
            cleanWs()
        }
    }
} 