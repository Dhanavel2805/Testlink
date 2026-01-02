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
		
		 stage('Push XML to GitHub Repo') {
            when {
                expression { currentBuild.currentResult == 'SUCCESS' }
            }
            steps {
                withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
                    sh '''
                        set -e
                        TODAY=$(date +%Y-%m-%d)
                        XML_FILE=$(ls *_${TODAY}.xml | head -n 1)

                        if [ -z "$XML_FILE" ]; then
                            echo "ERROR: No XML file found for today"
                            exit 1
                        fi

                        echo "Pushing file: $XML_FILE"

                        git config user.name "jenkins-bot"
                        git config user.email "jenkins@local"

                        git clone https://$Dhanavel/******@github.com/Dhanavel2805/Testlink_XML_to_Excel.git target_repo
                        cp "$XML_FILE" target_repo/
                        cd target_repo

                        git add "$XML_FILE"
                        git commit -m "Add XML generated on $TODAY"
                        git push origin main
                    '''
                }
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
