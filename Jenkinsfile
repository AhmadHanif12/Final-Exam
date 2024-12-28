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
                    bat """
                        python -m venv ${VENV}
                        .\\${VENV}\\Scripts\\activate.bat
                        pip install -r requirements.txt
                        pip install pytest pytest-flask
                    """
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    bat """
                        .\\${VENV}\\Scripts\\activate.bat
                        pytest test_encryption.py -v
                    """
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    bat """
                        .\\${VENV}\\Scripts\\activate.bat
                        python app.py
                    """
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