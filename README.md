# TaskFlow – Docker, AWS & DevOps Capstone Project

## 1. Project Overview

TaskFlow is a full-stack Task Management Application developed and deployed as part of Capstone Project 2.

The project demonstrates real-world DevOps practices by containerizing a frontend, backend, and database using Docker and Docker Compose, and deploying the application on AWS EC2.

## 2. Application Architecture

The application consists of three main services:

- **Frontend:** HTML, CSS, JavaScript and Nginx
- **Backend:** Python, Flask and Gunicorn
- **Database:** PostgreSQL

### Architecture Flow

```text
          User Browser
               |
               v
        AWS EC2 Instance
               |
               v
         Nginx Frontend
          Port 8080
               |
               v
         Flask Backend
          Port 5000
               |
               v
        PostgreSQL Database
          Port 5432
               |
               v
        Persistent Docker Volume
```

The services communicate through a Docker Compose network.

## 3. Technology Stack

| Category | Technologies |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Web Server | Nginx |
| Backend | Python, Flask, Gunicorn |
| Database | PostgreSQL |
| Containerization | Docker |
| Orchestration | Docker Compose |
| Cloud Platform | AWS EC2 |
| Operating System | Ubuntu Linux |
| Version Control | Git and GitHub |

## 4. Project Structure

```text
TaskFlow-DevOps-CapstoneP2/
│
├── backend/
│   ├── app.py
│   └── Dockerfile
│
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── frontend application files
│
├── database/
│   ├── Dockerfile
│   └── init.sql
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## 5. Docker Implementation

Dockerfiles were created for all three application services.

Docker Compose manages:

- Frontend container
- Backend container
- PostgreSQL container
- Internal service networking
- Persistent database storage
- Database health checks
- Service startup dependencies

### Start Application Locally

```bash
docker compose up -d --build
```

### Check Containers

```bash
docker compose ps
```

### View Logs

```bash
docker compose logs
```

### Stop Services

```bash
docker compose down
```

The named PostgreSQL volume preserves database data across container restarts.

**Important:** Do not use `docker compose down -v` when you want to preserve database data.

## 6. Environment Configuration

Create an environment file using the example:

```bash
cp .env.example .env
```

Configure the following variables:

```env
POSTGRES_DB=taskflow_db
POSTGRES_USER=taskflow_user
POSTGRES_PASSWORD=YOUR_STRONG_PASSWORD

DB_HOST=db
DB_NAME=taskflow_db
DB_USER=taskflow_user
DB_PASSWORD=YOUR_STRONG_PASSWORD
DB_PORT=5432
```

The `.env` file contains private configuration and must not be committed to GitHub.

## 7. AWS EC2 Deployment

The application was deployed on an AWS EC2 Ubuntu instance.

Deployment steps:

1. Provision an EC2 instance.
2. Configure the security group.
3. Install Docker and Docker Compose.
4. Clone the GitHub repository.
5. Configure environment variables.
6. Build and start containers using Docker Compose.
7. Verify application access through the public IP.

### Deployment Commands

```bash
git clone https://github.com/Ridwan-36/TaskFlow-DevOps-CapstoneP2.git

cd TaskFlow-DevOps-CapstoneP2

docker compose up -d --build

docker compose ps
```

### Application URL

```text
http://<EC2-PUBLIC-IP>:8080
```

Replace `<EC2-PUBLIC-IP>` with the current public IPv4 address of the EC2 instance.

## 8. Security Configuration

The EC2 security group was configured with:

| Port | Protocol | Purpose |
|---|---|---|
| 22 | TCP | SSH administration |
| 8080 | TCP | Web application access |

SSH access was restricted to the administrator's public IP address.

PostgreSQL port 5432 and backend port 5000 were not exposed through public security group rules.

Private SSH keys and environment files are excluded from Git tracking.

## 9. Application Testing

The following functionality was verified:

- Add new tasks
- View existing tasks
- Update task status
- Delete tasks
- Backend API connectivity
- PostgreSQL database connectivity
- Frontend accessibility through Nginx

### API Testing

```bash
curl http://localhost:8080/api/tasks
```

### Frontend Health Check

```bash
curl -I http://localhost:8080/
```

The frontend returned HTTP 200 OK during deployment verification.

## 10. Database Persistence Testing

Database persistence was verified by restarting Docker containers.

```bash
docker compose restart
```

After the containers became healthy, the application API was tested again.

Previously stored tasks remained available after the restart, confirming that the named Docker volume preserved database data.

## 11. ## 11. Logging and Health Checks

Application logs can be inspected using:

```bash
docker compose logs --tail=50
```

Individual service logs:

```bash
docker compose logs backend
docker compose logs frontend
docker compose logs db
```

Docker Compose health checks and container logs were used to verify service status and troubleshoot deployment issues.

## 12. Deployment Status

**Project Status: Successfully Deployed and Tested on AWS EC2**

Verified milestones:

- Full-stack application containerization
- Docker Compose service deployment
- PostgreSQL health check
- AWS EC2 deployment
- Public application accessibility
- CRUD functionality testing
- Container restart testing
- Database persistence verification
- GitHub repository publication

## 13. GitHub Repository

Source Code:

https://github.com/Ridwan-36/TaskFlow-DevOps-CapstoneP2

## 14. Project Learning Outcomes

Through this project, practical experience was gained in:

- Linux server administration
- Docker image creation and container management
- Docker Compose networking and volumes
- Flask and PostgreSQL integration
- AWS EC2 provisioning and deployment
- Security group configuration
- Application troubleshooting
- Git and GitHub version control
- Database persistence and service health verification

---

**TaskFlow – A Real-World Docker and AWS DevOps Deployment Project.**
