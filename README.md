# KYC Verification App

A web-based Know Your Customer (KYC) verification system using React (Frontend) and FastAPI (Backend). It integrates with Setu APIs for PAN and bank account verification.

Running on - http://3.111.32.152:3000/

For Running locally - docker compose -f 'docker-compose.yml' up -d --build 

Features

✅ PAN Verification via Setu API
✅ Bank Account Verification
✅ User-Friendly Interface
✅ Analytics Dashboard

## Tech Stack

Frontend: React
Backend: FastAPI (Python)
Database: MongoDB
Deployment: AWS (EC2, S3, RDS, Docker, Terraform)

## Setup & Installation

1. Clone the Repository
git clone git@github.com:GauravDange30/kyc-app.git
cd kyc-app
2. Frontend Setup (React)
cd frontend
npm install
Create a .env file in frontend

REACT_APP_CLIENTID_API_KEY=your_client_id
REACT_APP_CLIENTSECRET_API_KEY=your_client_secret
REACT_APP_PRODINSTANCE_API_KEY=your_product_instance_id
REACT_APP_PRODINSTANCE_API_KEY_BANK=your_bank_product_instance_id
Start the frontend:

npm start
3. Backend Setup (FastAPI)
cd backend
pip install -r requirements.txt
Create a .env file in backend

MONGO_URI=mongodb+srv://your_mongodb_url
SETU_API_KEY=your_setu_api_key
Start the backend:

uvicorn main:app --reload
API Endpoints

## Method	Endpoint	Description
POST	/kyc_verification/api/verify/pan	Verify PAN card

POST	/kyc_verification/api/verify/bank/reverse	Verify Bank Account

## Deployment on AWS

Create EC2 Instance (Ubuntu)
Install Docker & Docker Compose
sudo apt update && sudo apt install -y docker.io docker-compose
Clone Repository & Setup
git clone git@github.com:GauravDange30/kyc-app.git
cd kyc-app
Build & Run with Docker
docker-compose up --build -d
Expose API via Nginx or AWS Load Balancer
CI/CD Pipeline (GitHub Actions + AWS)

Trigger: Push to main branch
Build: Install dependencies & run tests
Deploy: SSH into AWS & restart services

## Future Improvements

✅ Role-based access control (RBAC)
✅ Webhooks for real-time verification updates
✅ Kubernetes for scaling

## Contributors
👤 Gaurav Dange

Feel free to contribute! PRs are welcome. 🚀
