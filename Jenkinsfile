pipeline {
    agent any

    parameters {
        file(name: 'UPLOAD_FILE', description: 'Select file to upload')
    }

    stages {


        stage('Store File') {
            steps {
                sh '''
                    echo "Storing uploaded file..."

                    mkdir -p "$WORKSPACE/uploads"

                    if [ -f "$WORKSPACE/$UPLOAD_FILE" ]; then
                        mv "$WORKSPACE/$UPLOAD_FILE" "$WORKSPACE/uploads/"
                        echo "File moved to $WORKSPACE/uploads/"
                    else
                        echo "Uploaded file not found for moving!"
                        exit 1
                    fi
                '''
            }
        }

        stage('Convert Excel to XML') {
            steps {
                sh '''
                    echo "Workspace: $WORKSPACE"
                    echo "Uploaded file name: $UPLOAD_FILE"

                    UPLOAD_PATH="$WORKSPACE/$UPLOAD_FILE"

                    if [ ! -f "$UPLOAD_PATH" ]; then
                        echo "ERROR: Uploaded file not found at $UPLOAD_PATH"
                        exit 1
                    fi

                    /opt/jenkins-venv/bin/python excel_to_xml.py "$UPLOAD_PATH"
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
    }
}
