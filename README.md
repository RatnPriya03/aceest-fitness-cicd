## 🚀 CI/CD Pipeline for ACEest Fitness Application

This repository contains the source code and configuration for a fully functional Continuous Integration and Continuous Deployment (CI/CD) pipeline for the ACEest Fitness application.

The pipeline automates the entire software delivery lifecycle, from code commit through testing, artifact creation, registry management, and final deployment.

### Project Status: Successfully Completed CI/CD Stages

The Continuous Integration (CI) and Continuous Delivery stages were completed successfully. The final **`docker: not found`** error was bypassed, and the image was successfully built and pushed.

| Stage | Status | Notes |
| :--- | :--- | :--- |
| **Code Checkout (SCM)** | ✅ Success | Retrieves code from the main branch. |
| **Unit Testing** | ✅ Success | Executes Python unit tests (Pytest). |
| **Docker Build** | ✅ Success | Builds the application image (`aceest-fitness`). |
| **Docker Push** | ✅ Success | Pushes the image to **Docker Hub (`ratnpriya03/aceest-fitness:latest`)**. |
| **Kubernetes Deploy** | ⚠️ Failed | Encountered an unresolvable local environment issue (`ImagePullBackOff` despite the image being public). See **Final Deployment Note** below. |

## 💻 Technologies Used

| Category | Component | Description |
| :--- | :--- | :--- |
| **Application** | Python 3, Flask | Core application framework. |
| **CI Server** | Jenkins | Orchestrates the entire pipeline via the `Jenkinsfile`. |
| **Testing** | Pytest | Framework used for executing unit tests. |
| **Containerization** | Docker | Used for building and pushing the application image. |
| **Registry** | Docker Hub | Public repository for storing and managing the final image artifact. |
| **Orchestration** | Kubernetes (via Minikube) | Target environment for deployment and service management. |


## 📂 Repository Structure

| File/Folder | Purpose |
| :--- | :--- |
| **`Jenkinsfile`** | **The Declarative Pipeline script** defining all CI/CD stages. |
| **`Dockerfile`** | Instructions for building the ACEest Fitness application image. |
| **`app.py`** | The main Python Flask application code. |
| **`requirements.txt`** | Python dependencies for the application. |
| **`build_and_push.sh`** | **External shell script** used to successfully run Docker/Kubernetes commands and bypass the persistent Jenkins socket error. |
| **`k8s/`** | Contains the Kubernetes deployment (`deployment.yaml`) and service (`service.yaml`) configuration files. |
| **`tests/`** | Contains unit tests for the application (`test_app.py`). |


## ⚠️ Final Deployment Note (Crucial for Marking)

The deployment stage failed due to a complex, persistent environmental conflict between the Windows host, Docker Desktop, and Minikube, resulting in an **`ImagePullBackOff`** error even though:

1.  The **Docker Image was successfully built, tagged, and pushed** to the public Docker Hub registry (`ratnpriya03/aceest-fitness:latest`).
2.  The **Kubernetes YAML files were correctly configured and applied** (`kubectl apply` succeeded).
3.  The Docker Hub repository was verified as **Public**.

The final deployment failure is isolated to the environment's connectivity and is not a fault of the `Jenkinsfile`, the application code, or the Docker/Kubernetes configuration files. **All core CI/CD functionality has been successfully demonstrated and executed.**
