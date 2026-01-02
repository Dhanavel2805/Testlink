pipeline {
    agent any

    parameters {
        file(name: 'UPLOAD_FILE', description: 'Select file to upload')
    }

    stages {

       // stage('Checkout Repository') {
         //   steps {
           //     checkout scm
            //}
       // }

       stage('Convert Excel to XML') {
    steps {
        sh '''
        echo "Workspace: $WORKSPACE"
        echo "Uploaded file name: $UPLOAD_FILE"

        UPLOAD_DIR="$WORKSPACE@tmp/fileParameters"
        UPLOAD_PATH="$UPLOAD_DIR/$UPLOAD_FILE"

        if [ ! -f "$UPLOAD_PATH" ]; then
          echo "ERROR: Uploaded file not found at $UPLOAD_PATH"
          exit 1
        fi

        echo "File found: $UPLOAD_PATH"

        # Optional: copy to workspace
        cp "$UPLOAD_PATH" "$WORKSPACE/$UPLOAD_FILE"

        # Run your script
        python3 excel_to_xml_old.py "$WORKSPACE/$UPLOAD_FILE"
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
