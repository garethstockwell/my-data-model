// tests.groovy

pipeline {
    agent { label 'default' }

    stages {
        stage('setup') {
            steps {
                sh '''
                    python3 --version
                    python3 -m venv venv
                '''
            }
        }
        stage('upgrade-pip') {
            steps {
                sh '''
                    source venv/bin/activate
                    which python
                    which pip
                    pip install --constraint=.jenkins/constraints.txt pip
                    pip --version
                '''
            }
        }
    }
}
