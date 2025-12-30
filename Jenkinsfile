pipeline {
    agent any

    parameters {
        file(name: 'UPLOAD_FILE', description: 'Select file to upload')
    }

    stages {

        stage('Checkout Repository') {
            steps {
                checkout scm
            }
        }

        stage('Convert Excel to XML') {
            steps {
                bat """
                python excel_to_xml_advance.py "%WORKSPACE%\\%UPLOAD_FILE%"
                """
            }
        }
    }

    post {
        success {
            script {
                def today = new Date().format('yyyy-MM-dd')
                archiveArtifacts artifacts: "**/*_${today}.xml", fingerprint: true
            }
        }

        always {
            echo 'Build completed!'
        }
    }
}
