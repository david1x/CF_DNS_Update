properties([pipelineTriggers([cron('H/30 * * * *')])])
pipeline {
    agent { label 'deepin' }

    environment {
        API_TOKEN = credentials('API_TOKEN')
        ZONE_ID = credentials('ZONE_ID')
        DOMAIN = credentials('DOMAIN')
        RECORDS = credentials('RECORDS')
        DB_HOST = credentials("DB_HOST")
        DB_USER = credentials("DB_USER")
        DB_PASS = credentials("DB_PASS")
        DB_NAME = credentials("DB_NAME")
        DB_PORT = credentials("DB_PORT")
    }

    stages {
        
        stage('Create Virtual Environment') {
            steps {
                script {
                        // Install pip if not already installed
                        def pipInstalled = sh(script: 'command -v pip', returnStatus: true) == 0
                        if (!pipInstalled) {
                            sh 'sudo apt-get update && sudo apt-get install -y python3-pip'
                        }
                        sh 'env | pwd'
                        // Create a virtual environment in the TorrentHeadless directory
                        sh 'python3 -m venv venv'
                        
                        sh 'env | pwd'
                        // Activate the virtual environment
                        sh './venv/bin/activate'

                        sh 'env | pwd'
                        // Install requirements.txt within the virtual environment
                        sh 'sudo ./venv/bin/pip3 install -r requirements.txt'
                        sh 'env | pwd'                    
                }
            }
        }

        stage('Run') {
            steps {
                    script {
                        // Use double quotes to interpolate variables
                        sh 'env | pwd'
                        sh "./venv/bin/python3 main.py"
                    }
            }
        }

        stage('Cleanup') {
            steps {
                deleteDir()
            }
        }
    }

}