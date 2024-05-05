pipeline {
    agent any

    stages {
        stage('Prepare Environment') {
            steps {
                script {
                    // Загрузка переменных окружения из файла .env
                    def envVars = readProperties file: '/opt/env/.env.getcontact'

                    // Импорт переменных окружения в среду Jenkins job
                    envVars.each {
                        env."${it.key}" = "${it.value}"
                    }
                }
            }
        }
        stage('Creating images tag') {
            steps {
                script {
                    // Создание уникального имени для нового образа
                    def timestamp = new Date().getTime()
                }
            }
        }
        stage('Get Old Image Tag (getcontact-flask)') {
            steps {
                script {
                    // Получаем тег старого образа pinteresthub
                    env.OLD_IMAGE_TAG = sh(script: "docker images getcontact-flask --format '{{.Tag}}' | head -n 1", returnStdout: true).trim()
                }
            }
        }
        stage('Build New Image (getcontact-flask)') {
            steps {
                script {
                    // Создание уникального имени для нового образа
                    env.NEW_IMAGE_NAME = "getcontact-flask:${timestamp}"

                    echo "# Собираем новый Docker образ"
                    dir('./PyQt5-flask_desktop_app') {
                        sh "docker build -t ${env.NEW_IMAGE_NAME} ."
                    }
                }
            }
        }
        stage('Cleanup Old Container and Image (getcontact-flask)') {
            steps {
                echo "# Принудительно останавливаем и удаляем старый контейнер, если он существует"
                sh "docker rm -f getcontact-flask || true"

                echo "# Удаляем старый Docker образ, если он существует"
                sh "docker rmi getcontact-flask:${env.OLD_IMAGE_TAG} || true"
            }
        }
        stage('Get Old Image Tag (getcontact-tg)') {
            steps {
                script {
                    // Получаем тег старого образа pinteresthub
                    env.OLD_IMAGE_TAG = sh(script: "docker images getcontact-tg --format '{{.Tag}}' | head -n 1", returnStdout: true).trim()
                }
            }
        }
        stage('Build New Image (getcontact-tg)') {
            steps {
                script {
                    // Создание уникального имени для нового образа
                    env.NEW_IMAGE_NAME = "getcontact-tg:${timestamp}"

                    echo "# Собираем новый Docker образ"
                    sh "docker build -t ${env.NEW_IMAGE_NAME} ."
                }
            }
        }
        stage('Cleanup Old Container and Image (getcontact-tg)') {
            steps {
                echo "# Принудительно останавливаем и удаляем старый контейнер, если он существует"
                sh "docker rm -f getcontact-tg || true"

                echo "# Удаляем старый Docker образ, если он существует"
                sh "docker rmi getcontact-tg:${env.OLD_IMAGE_TAG} || true"
            }
        }
        stage('Run Docker Compose') {
            steps {
                script {
                    echo "# Запускаем Docker Compose"
                    sh "docker-compose up -d"
                }
            }
        }
    }
}
