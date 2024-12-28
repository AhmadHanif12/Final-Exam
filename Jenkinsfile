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
                        python -m pip install virtualenv
                        python -m virtualenv venv
                        call venv\\Scripts\\activate.bat
                        python -m pip install -r requirements.txt
                        python -m pip install pytest pytest-flask
                    '''
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    bat '''
                        call venv\\Scripts\\activate.bat
                        pytest test_encryption.py -v
                    '''
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    bat '''
                        call venv\\Scripts\\activate.bat
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