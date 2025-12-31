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
                sh '''

                 set -e

        echo "Uploaded file parameter: $UPLOAD_FILE"
        echo "Workspace: $WORKSPACE"

        # ALWAYS copy uploaded file to a known name
        cp "$UPLOAD_FILE" input.xlsx
        
                VENV_PY="/opt/jenkins-venv/bin/python"

                if [ ! -x "$VENV_PY" ]; then
                    echo "ERROR: Virtualenv python not found at $VENV_PY"
                    exit 1
                fi

                echo "Using virtualenv python:"
                $VENV_PY --version

                $VENV_PY excel_to_xml.py $UPLOAD_FILE
                '''
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
