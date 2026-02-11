# Two-Tier Flask Application with CI/CD Pipeline

![Python](https://img.shields.io/badge/python-3.9-blue)
![Flask](https://img.shields.io/badge/flask-3.0-green)
![Docker](https://img.shields.io/badge/docker-compose-blue)
![AWS](https://img.shields.io/badge/AWS-EC2-orange)
![Jenkins](https://img.shields.io/badge/CI%2FCD-Jenkins-red)
![MySQL](https://img.shields.io/badge/database-MySQL-blue)

## Overview

A production-ready two-tier web application built with Flask and MySQL, demonstrating a complete CI/CD pipeline using Jenkins, Docker, and AWS EC2. This project showcases automated deployment workflows, containerization best practices, and cloud infrastructure management.

## Architecture

```
┌─────────────┐      ┌──────────────────┐        ┌─────────────────────┐
│  Developer  │─────▶│  GitHub Repository│─────▶│   Jenkins Server    │
│ (Git Push)  │      │  (Source Control) │       │   (AWS EC2)         │
└─────────────┘      └──────────────────┘        │                     │
                                                 │ 1. Clone Repository │
                                                 │ 2. Build Docker     │
                                                 │ 3. Deploy Containers│
                                                 └──────────┬──────────┘
                                                            │
                                                            ▼
                                                  ┌─────────────────────┐
                                                  │  Application Server │
                                                  │    (Same EC2)       │
                                                  │                     │
                                                  │  ┌───────────────┐  │
                                                  │  │ Flask Container│ │
                                                  │  └───────┬───────┘  │
                                                  │          │          │
                                                  │          ▼          │
                                                  │  ┌───────────────┐  │
                                                  │  │ MySQL Container│ │
                                                  │  └───────────────┘  │
                                                  └─────────────────────┘
```

## Features

- **Full CI/CD Pipeline** - Automated build and deployment on every git push
- **Containerized Deployment** - Both Flask and MySQL run in isolated Docker containers
- **Automated Database Setup** - MySQL initializes with proper schema on first run
- **Health Checks** - Both services include health monitoring
- **Persistent Data** - MySQL data persists across container restarts using Docker volumes
- **Custom Networking** - Containers communicate on isolated Docker network
- **Message Board Functionality** - Users can submit and view messages stored in the database

## Technologies Used

### Backend & Database

- **Python 3.9** - Application runtime
- **Flask 3.0** - Web framework
- **MySQL** - Relational database
- **Flask-MySQLdb** - Database connector

### DevOps & Infrastructure

- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Jenkins** - CI/CD automation
- **AWS EC2** - Cloud hosting (Amazon Linux 2023)
- **Git/GitHub** - Version control

## Project Structure

```
├── app.py                  # Flask application
├── templates/
│   └── index.html         # Frontend template
├── requirements.txt       # Python dependencies
├── Dockerfile            # Flask container definition
├── docker-compose.yml    # Multi-container orchestration
├── Jenkinsfile          # CI/CD pipeline definition
└── README.md            # Project documentation
```

## Local Setup

### Running Locally with Docker Compose

1. **Clone the repository**

   ```bash
   git clone https://github.com/rasathelamedude/DevOps-project-two-tier-flask-app.git
   cd DevOps-project-two-tier-flask-app
   ```

2. **Build and run with Docker Compose**

   ```bash
   docker compose up -d
   ```

3. **Access the application**

   ```
   http://localhost:8000
   ```

4. **Stop the application**
   ```bash
   docker compose down
   ```

## AWS Deployment Guide

### Step 1: Launch EC2 Instance

1. Launch an **Amazon Linux 2023** EC2 instance (t2.small or larger recommended)
2. Configure Security Group with the following inbound rules:
   - SSH (Port 22) - Your IP
   - HTTP (Port 80) - Anywhere
   - Custom TCP (Port 8000) - Anywhere (Flask app)
   - Custom TCP (Port 8080) - Anywhere (Jenkins)

### Step 2: Install Dependencies on EC2

SSH into your instance and run:

```bash
# Update system
sudo yum update -y

# Install Git
sudo yum install git -y

# Install Docker
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user
newgrp docker

# Install Docker Compose
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# Verify installations
docker --version
docker compose version
```

### Step 3: Install Jenkins

```bash
# Install Java
sudo yum install java-17-amazon-corretto -y

# Add Jenkins repository
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key

# Install Jenkins
sudo yum install jenkins -y

# Start Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Grant Jenkins Docker permissions
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins

# Get initial admin password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

### Step 4: Configure Jenkins

1. Access Jenkins at `http://<your-ec2-public-ip>:8080`
2. Enter the initial admin password
3. Install suggested plugins
4. Create admin user

### Step 5: Create Jenkins Pipeline

1. Create new **Pipeline** job in Jenkins
2. Configure:
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: Your GitHub repo URL
   - **Script Path**: Jenkinsfile
3. Save and click **Build Now**

### Step 6: Increase /tmp Size (Important!)

Jenkins requires sufficient temporary workspace:

```bash
# Increase tmpfs to 2GB
sudo mount -o remount,size=2G /tmp

# Make it permanent
echo "tmpfs /tmp tmpfs defaults,size=2G 0 0" | sudo tee -a /etc/fstab
```

### Step 7: Access Your Application

After successful pipeline execution:

```
http://<your-ec2-public-ip>:8000
```

## CI/CD Pipeline

The Jenkins pipeline automates three key stages:

### Stage 1: Clone Code

- Pulls the latest code from the GitHub repository
- Triggered automatically on git push (can be configured with webhooks)

### Stage 2: Build Docker Image

- Builds the Flask application Docker image
- Tags it as `flask-app:latest`
- Leverages Docker layer caching for faster builds

### Stage 3: Deploy with Docker Compose

- Stops any existing containers
- Starts fresh containers using the newly built image
- MySQL container initializes with persistent volume
- Flask container connects to MySQL on custom network

**Pipeline Flow:**

```
Git Push → Jenkins Detects Change → Clone Repo → Build Image → Deploy Containers → App Live
```

## Screenshots

You just need to replace the screenshot bullet list with Markdown image references that point to your local ./screenshots/ folder.

Here’s the updated Markdown format:

## Screenshots

### Jenkins pipeline success

![Jenkins pipeline success](./screenshots/pipeline-succeeding.png)

### Application running

![Application running](./screenshots/flask-app-pipeline-result.png)

### Docker containers status

![Docker containers status](./screenshots/pipeline-running-docker-build.png)

### EC2 instance setup & dependencies installation

![EC2 instance setup](./screenshots/installing-dependencies-in-ec2.png)

## Challenges & Learnings

### Challenge 1: EC2 Instance Froze During Build

**Problem:** The t2.micro instance (1GB RAM) ran out of memory during Docker builds, causing the instance to freeze.

**Solution:**

- Upgraded to t2.small (2GB RAM)
- Added 2GB swap space as backup
- Learned about resource requirements for CI/CD workloads

### Challenge 2: Jenkins Stuck on "Waiting for executor"

**Problem:** Pipeline wouldn't start, showing "Waiting for next available executor"

**Solution:**

- `/tmp` directory was only 459MB, below Jenkins's 1GB threshold
- Increased tmpfs size to 2GB
- Learned about Jenkins disk space monitoring requirements

### Challenge 3: Docker Compose Buildx Version Conflict

**Problem:** `compose build requires buildx 0.17.0 or later` error

**Solution:**

- Modified `docker-compose.yml` to use pre-built image instead of rebuilding
- Implemented better CI/CD practice: build once, deploy many times
- Separated build and deploy concerns

## Key Takeaways

- **Infrastructure as Code**: Jenkinsfile and docker-compose.yml enable reproducible deployments
- **Containerization Benefits**: Isolated environments, consistent deployments, easy scaling
- **CI/CD Value**: Automated pipelines reduce manual errors and deployment time
- **Resource Management**: Cloud resources need proper sizing for workload requirements
- **Troubleshooting Skills**: Developed systematic debugging approach for DevOps issues

## Future Improvements

- [ ] Implement HTTPS with SSL/TLS certificates (Let's Encrypt)
- [ ] Add automated testing stage in CI/CD pipeline (pytest)
- [ ] Migrate to Kubernetes for container orchestration
- [ ] Implement Infrastructure as Code with Terraform
- [ ] Use AWS RDS instead of containerized MySQL for production
- [ ] Add monitoring and logging (Prometheus + Grafana)
- [ ] Implement GitHub webhooks for automatic Jenkins triggers
- [ ] Add environment variables management with AWS Secrets Manager
- [ ] Set up blue-green deployment strategy
- [ ] Implement automated backup strategy for database

## Security Notes

**For Production Deployments:**

- Never hardcode credentials (use AWS Secrets Manager or environment files)
- Restrict Security Group rules to specific IPs
- Implement IAM roles for EC2 instances
- Enable HTTPS/SSL for all traffic
- Regular security updates and patching
- Use private subnets for databases

**Current Implementation:**
This project uses hardcoded credentials for educational purposes. The focus is on demonstrating DevOps workflows and CI/CD concepts.

## License

MIT License - Feel free to use this project for learning and portfolio purposes.

## Author

**Rasyar Mustafa**

- GitHub: [@rasathelamedude](https://github.com/rasathelamedude)
- LinkedIn: [@rasyar](https://www.linkedin.com/in/rasyar-safin-1b105b2b9/)

---

If you found this project helpful, please consider giving it a star!

## Acknowledgments

- Inspired by real-world DevOps practices
- Built as a learning project to demonstrate CI/CD capabilities
- Thanks to the open-source community for excellent documentation
