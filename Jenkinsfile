pipeline {
  agent any
  stages {
      stage('Clone-code') {
        steps {
          git branch: 'main', url: 'https://github.com/rasathelamedude/DevOps-project-two-tier-flask-app.git'
        }
      }
      stage('Build Docker Image') {
        steps {
            sh 'docker build -t flask-app:latest .'
        }
      }
      stage('Deploy with Docker Compose') {
        steps {
            // Stop any running containers
            sh 'docker compose down || true'

            // Start the new containers
            sh 'docker compose up -d'
        }
      }
  }
}