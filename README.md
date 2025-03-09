# ProjectHub API

ProjectHub API is a FastAPI-based application designed to manage projects and tasks. It leverages AWS Cognito for authentication and DynamoDB for data storage.

## Table of Contents

- Installation
- Configuration
- Usage
- API Endpoints

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/gagatek1/projecthub-api.git
    cd projecthub-api
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. Create a `.env` file in the root directory and add the following environment variables:

    ```env
    AWS_ACCESS_KEY_ID=your_aws_access_key_id
    AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
    REGION_NAME=your_aws_region
    AWS_COGNITO_APP_CLIENT_ID=your_cognito_app_client_id
    AWS_COGNITO_APP_CLIENT_SECRET=your_cognito_app_client_secret
    AWS_COGNITO_USER_POOL_ID=your_cognito_user_pool_id
    ```

2. Ensure that your AWS credentials and region are correctly set up.

## Usage

1. Run the application:

    ```sh
    uvicorn main:app --reload
    ```

2. The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### Authentication

- **POST /auth/signup**: Sign up a new user.
- **POST /auth/verify**: Verify a user's account.
- **POST /auth/signin**: Sign in a user.
- **POST /auth/token**: Generate a new token.
- **POST /auth/change**: Change a user's password.
- **POST /auth/forgot**: Initiate forgot password process.
- **POST /auth/confirm**: Confirm forgot password.
- **POST /auth/logout**: Log out a user.

### Projects

- **POST /projects/create**: Create a new project.
- **GET /projects/**: Get all projects.
- **GET /projects/{project_id}**: Get a specific project.
- **PUT /projects/update**: Update a project.
- **DELETE /projects/delete/{project_id}**: Delete a project.

### Tasks

- **POST /tasks/create**: Create a new task.
- **GET /tasks/**: Get all tasks.
- **GET /tasks/{task_id}**: Get a specific task.
- **PUT /tasks/update**: Update a task.
- **DELETE /tasks/delete/{task_id}**: Delete a task.

### Users

- **GET /users/**: Get all users.
- **GET /users/{user_id}**: Get a specific user.
- **POST /users/email**: Update a user's email.
