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
            def api = docker.build("docker-registry.data.amsterdam.nl/datapunt/atlas-health-checks:${env.BUILD_NUMBER}", ".")
            api.push()
        }
    }

    stage("Test") {
        tryStep "test", {
            withEnv([
                    'USERNAME_EMPLOYEE_PLUS=atlas.employee.plus@amsterdam.nl',
                    'API_ROOT=https://acc.api.data.amsterdam.nl'
            ]) {
                withCredentials([string(credentialsId: 'PASSWORD_EMPLOYEE_PLUS', variable: 'PASSWORD_EMPLOYEE_PLUS')]) {
                    if (!PASSWORD_EMPLOYEE_PLUS?.trim()) {
                        error("PASSWORD_EMPLOYEE_PLUS missing")
                    }
                    def image = docker.image("docker-registry.data.amsterdam.nl/datapunt/atlas-health-checks:${env.BUILD_NUMBER}")
                    image.pull()
                    image.inside { c ->
                        sh 'pytest'
                    }
                }
            }
        }
    }
}

String BRANCH = "${env.BRANCH_NAME}"

if (BRANCH == "master") {
    node {
        stage('Push image') {
            tryStep "tag & push image", {
                def api = docker.image("docker-registry.data.amsterdam.nl/datapunt/atlas-health-checks:${env.BUILD_NUMBER}")
                api.pull()
                api.push("latest")
            }
        }
    }
}
