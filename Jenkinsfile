def time
properties([pipelineTriggers([cron('H/10 * * * *')])])

pipeline {
    agent none  // Default to no agent to allow pre-checks before assigning an agent

    stages {
        stage('Check Node') {
            agent { label 'master' }  // Run on master to check agent status
            steps {
                script {
                    def nodeOnline = jenkins.model.Jenkins.instance.getNode('deepin')?.toComputer()?.isOnline()
                    if (!nodeOnline) {
                        echo 'Node "deepin" is offline. Aborting pipeline.'
                        currentBuild.result = 'ABORTED'
                        error('Node is offline, stopping execution.')
                    }
                }
            }
        }
    }

    agent { label 'deepin' }  // Assign job to node after confirming it's online

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
        TLG_ID = credentials("TLG_ID")
        BOT_TOKEN = credentials("BOT_TOKEN")
    }

    stages {
        stage('Check Public IP') {
            steps {
                script {
                    def currentIp = sh(script: "curl -s https://api.ipify.org", returnStdout: true).trim()
                    echo "Current public IP: ${currentIp}"

                    def previousIp = sh(script: """
                        PGPASSWORD=${DB_PASS} psql -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USER} -d ${DB_NAME} -t -c \
                        "SELECT previous_ip FROM public_ip LIMIT 1;"
                    """, returnStdout: true).trim()
                    echo "Previous public IP: ${previousIp}"

                    if (currentIp == previousIp) {
                        echo "Public IP has not changed. Skipping remaining stages."
                        currentBuild.result = 'SUCCESS'
                        error('Skipping pipeline execution.')
                    } else {
                        echo "Public IP has changed from ${previousIp} to ${currentIp}."
                    }
                }
            }
        }

        stage('Create Virtual Environment') {
            steps {
                script {
                    if (sh(script: 'command -v pip', returnStatus: true) != 0) {
                        sh 'sudo apt-get update && sudo apt-get install -y python3-pip'
                    }
                    sh 'python3 -m venv venv'
                    sh './venv/bin/pip3 install -r requirements.txt'
                }
            }
        }

        stage('Run') {
            steps {
                script {
                    sh './venv/bin/python3 main.py'
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
