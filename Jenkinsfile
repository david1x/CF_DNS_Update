def time
properties([pipelineTriggers([cron('H/10 * * * *')])])
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
        stage('Check Public IP') {
            steps {
                script {
                    // Get current public IP
                    def currentIp = sh(script: "curl -s https://api.ipify.org", returnStdout: true).trim()
                    echo "Current public IP: ${currentIp}"

                    // Query PostgreSQL to get the previous IP
                    def previousIp = sh(script: """
                        PGPASSWORD=${DB_PASS} psql -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USER} -d ${DB_NAME} -t -c \
                        "SELECT previous_ip FROM public_ip LIMIT 1;"
                    """, returnStdout: true).trim()
                    echo "Previous public IP: ${previousIp}"

                    // Compare the IPs
                    if (currentIp == previousIp) {
                        echo "Public IP has not changed. Skipping remaining stages."
                        exit_now = true
                        currentBuild.result = 'SUCCESS'

                    } else {
                        echo "Public IP has changed from ${previousIp} to ${currentIp}."
                        echo "Proceeding with the rest of the pipeline."
                    }
                }
            }
        }
        stage('Create Virtual Environment') {
            when {
                not { expression { exit_now } }
            }
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
                        sh '. venv/bin/activate'

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