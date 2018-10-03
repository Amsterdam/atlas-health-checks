#!groovy

def tryStep(String message, Closure block, Closure tearDown = null) {
    try {
        block();
    }
    catch (Throwable t) {
        slackSend message: "${env.JOB_NAME}: ${message} failure ${env.BUILD_URL}", channel: '#ci-channel-app', color: 'danger'

        throw t;
    }
    finally {
        if (tearDown) {
            tearDown();
        }
    }
}


node {
    stage("Checkout") {
        checkout scm
    }

    stage("Build docker") {
        tryStep "build", {
            def api = docker.build("build.datapunt.amsterdam.nl:5000/datapunt/build.datapunt.amsterdam.nl:5000/datapunt/atlas-health-checks:${env.BUILD_NUMBER}", ".")
            api.push()
        }
    }

    stage("Test") {
        tryStep "Test", {
            def image = docker.image("build.datapunt.amsterdam.nl:5000/datapunt/build.datapunt.amsterdam.nl:5000/datapunt/atlas-health-checks:${env.BUILD_NUMBER}")
            image.pull()
            image.run()
        }
    }
}

String BRANCH = "${env.BRANCH_NAME}"

if (BRANCH == "master") {
    node {
        stage('Push image') {
            tryStep "image tagging", {
                def api = docker.image("build.datapunt.amsterdam.nl:5000/datapunt/atlas-health-checks:${env.BUILD_NUMBER}")
                api.pull()
                api.push("latest")
            }
        }
    }
}
