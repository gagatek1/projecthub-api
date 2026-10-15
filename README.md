# ProjectHub API

ProjectHub API is a FastAPI application for managing projects and tasks. It uses AWS Cognito for authentication and a single DynamoDB table for storage. This guide covers running it locally with uvicorn.

## Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [AWS setup](#aws-setup)
4. [Configuration](#configuration)
5. [Running locally](#running-locally)
6. [Trying the API](#trying-the-api)
7. [Development](#development)
8. [API endpoints](#api-endpoints)
9. [Project layout](#project-layout)
10. [Troubleshooting](#troubleshooting)

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.11 or newer. uv installs Python 3.14 (from `.python-version`) automatically.
- [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), configured with credentials allowed to manage Cognito and DynamoDB (only needed for the one-time AWS setup below).
- An AWS account.

## Installation

```sh
git clone https://github.com/gagatek1/projecthub-api.git
cd projecthub-api
uv sync
```

`uv sync` creates `.venv/` and installs runtime and development dependencies exactly as pinned in `uv.lock`.

## AWS setup

You need a Cognito user pool with an app client, and one DynamoDB table. The commands below create both; replace `eu-central-1` with your region.

### Cognito user pool

```sh
export AWS_REGION=eu-central-1

POOL_ID=$(aws cognito-idp create-user-pool \
  --pool-name projecthub \
  --username-attributes email \
  --auto-verified-attributes email \
  --query UserPool.Id --output text)

aws cognito-idp create-user-pool-client \
  --user-pool-id "$POOL_ID" \
  --client-name projecthub-api \
  --generate-secret \
  --explicit-auth-flows ALLOW_USER_PASSWORD_AUTH ALLOW_REFRESH_TOKEN_AUTH \
  --query 'UserPoolClient.[ClientId,ClientSecret]' --output text

echo "$POOL_ID"
```

Note the pool id, client id and client secret for the configuration step. The client secret is optional: if you create the client without `--generate-secret`, leave `AWS_COGNITO_APP_CLIENT_SECRET` empty.

### DynamoDB table

All projects and tasks live in one table with a string partition key `pk` and sort key `sk`:

```sh
aws dynamodb create-table \
  --table-name projecthub \
  --attribute-definitions AttributeName=pk,AttributeType=S AttributeName=sk,AttributeType=S \
  --key-schema AttributeName=pk,KeyType=HASH AttributeName=sk,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST

aws dynamodb wait table-exists --table-name projecthub
```

Item keys:

| Item    | `pk`                   | `sk`           |
|---------|------------------------|----------------|
| Project | `project`              | `project#<id>` |
| Task    | `project#<project_id>` | `task#<id>`    |

Data from the old `projects`/`tasks` tables (versions up to 0.6) is not migrated automatically.

## Configuration

Copy the example file and fill in the values from the AWS setup:

```sh
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `APP_STAGE` | no (`dev`) | `dev`, `test`, `staging` or `prod`. OpenAPI docs are disabled in `prod`. |
| `REGION_NAME` | yes | AWS region of Cognito and DynamoDB, e.g. `eu-central-1`. |
| `DYNAMODB_TABLE` | no (`projecthub`) | Name of the table created above. |
| `DYNAMODB_HOST` | no | Endpoint override, only for DynamoDB Local (e.g. `http://localhost:8000`). |
| `AWS_COGNITO_APP_CLIENT_ID` | yes | App client id. |
| `AWS_COGNITO_APP_CLIENT_SECRET` | no | App client secret; empty for clients without a secret. |
| `AWS_COGNITO_USER_POOL_ID` | yes | User pool id. |

The app does not read AWS credentials from these variables. boto3 uses the standard AWS chain: `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` (they can also go into `.env`) or `AWS_PROFILE`. Settings are validated at startup, so a missing or malformed value fails immediately with a clear error.

## Running locally

```sh
uv run --env-file .env uvicorn app.entrypoints.api.api_gateway_handler:app --reload
```

`--env-file .env` exports the file into the process environment so that boto3 also sees AWS credentials stored there.

- API: http://127.0.0.1:8000/api/v1
- Health check: http://127.0.0.1:8000/api/v1/health
- Swagger UI: http://127.0.0.1:8000/api-docs (not available when `APP_STAGE=prod`)

## Trying the API

```sh
API=http://127.0.0.1:8000/api/v1

# 1. Sign up; Cognito emails a confirmation code
curl -s -X POST $API/auth/signup -H 'Content-Type: application/json' \
  -d '{"email": "you@example.com", "password": "Passw0rd!x"}'

# 2. Confirm the account with the code from the email
curl -s -X POST $API/auth/verify -H 'Content-Type: application/json' \
  -d '{"email": "you@example.com", "confirmation_code": "123456"}'

# 3. Sign in and keep the access token
TOKEN=$(curl -s -X POST $API/auth/signin -H 'Content-Type: application/json' \
  -d '{"email": "you@example.com", "password": "Passw0rd!x"}' \
  | python3 -c 'import json, sys; print(json.load(sys.stdin)["AccessToken"])')

# 4. Create a project and a task in it
PROJECT_ID=$(curl -s -X POST $API/projects -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"name": "Apollo", "description": "Moon landing", "max_users": 3}' \
  | python3 -c 'import json, sys; print(json.load(sys.stdin)["id"])')

curl -s -X POST $API/projects/$PROJECT_ID/tasks -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"name": "Build rocket", "description": ""}'

# 5. List your projects and the project's tasks
curl -s "$API/projects?limit=20" -H "Authorization: Bearer $TOKEN"
curl -s "$API/projects/$PROJECT_ID/tasks" -H "Authorization: Bearer $TOKEN"
```

Lists return `{"items": [...], "next_cursor": "..."}`. When `next_cursor` is not `null`, pass it back as `?cursor=` to get the next page.

## Development

All commands run inside the project's virtual environment through `uv run`.

| Task | Command |
|---|---|
| Install / update dependencies | `uv sync` |
| Add a runtime dependency | `uv add <package>` |
| Add a development dependency | `uv add --dev <package>` |
| Format code | `uv run ruff format .` |
| Lint (auto-fix safe issues with `--fix`) | `uv run ruff check .` |
| Type check | `uv run ty check --error-on-warning` |
| Check layer contracts | `uv run lint-imports` |
| Run all tests | `uv run pytest` |
| Run one test file | `uv run pytest tests/domain/project/command_handlers/test_create_project.py -x` |
| Coverage report | `uv run pytest --cov --cov-report=term-missing` |

Before pushing, run the same checks as CI:

```sh
uv run ruff format --check . && uv run ruff check . && uv run ty check --error-on-warning && uv run lint-imports && uv run pytest
```

Tests need no AWS account: DynamoDB and Cognito are simulated with [moto](https://docs.getmoto.org/), entities are created with FactoryBoy factories (`tests/fixtures/factories.py`), and authentication is mocked with the `tokens` fixture.

## API endpoints

All paths are prefixed with `/api/v1`. Every endpoint except the public auth flows requires `Authorization: Bearer <AccessToken>`.

| Status | Meaning |
|---|---|
| 400 | Invalid code, password policy or cursor |
| 401 | Missing, invalid or revoked token; wrong credentials |
| 403 | Not the owner or assignee; account not confirmed |
| 404 | Resource (or assigned user) not found |
| 409 | Email already registered; project still has tasks |
| 422 | Request validation failed (the response lists fields, never the submitted values) |
| 429 | Too many attempts |
| 502 | Identity provider failure |

### Authentication

- **POST /auth/signup**: sign up (public)
- **POST /auth/verify**: confirm the account with a code (public)
- **POST /auth/signin**: get tokens (public)
- **POST /auth/token**: new access token from a refresh token; `user_id` is the Cognito username (public)
- **POST /auth/forgot**: send a password reset code; the answer is the same whether or not the account exists (public)
- **POST /auth/confirm**: reset the password with a code (public)
- **POST /auth/change**: change the password (`old_password`, `new_password`)
- **POST /auth/logout**: global sign-out, revokes all tokens (204)

### Projects

Only the owner can see, update or delete a project. A project with tasks cannot be deleted (409).

- **POST /projects**: create a project
- **GET /projects?limit=&cursor=**: list your projects (id, name)
- **GET /projects/{project_id}**: get a project
- **PUT /projects/{project_id}**: update a project
- **DELETE /projects/{project_id}**: delete a project

### Tasks

Tasks belong to a project. Only the project owner can create them. The owner sees all tasks of the project, other users only tasks assigned to them; only the assigned user can update or delete one. `assigned_user` must be an existing Cognito user.

- **POST /projects/{project_id}/tasks**: create a task (assigned to you by default)
- **GET /projects/{project_id}/tasks?limit=&cursor=**: list tasks of the project (id, name)
- **GET /projects/{project_id}/tasks/{task_id}**: get a task
- **PUT /projects/{project_id}/tasks/{task_id}**: update a task
- **DELETE /projects/{project_id}/tasks/{task_id}**: delete a task

### Users

- **GET /users?limit=&cursor=**: list users (id, sub, status, enabled; at most 60 per page)
- **GET /users/{sub}**: get a user by `sub`
- **PUT /users/me/email**: change your email (Cognito sends a verification code)

## Project layout

```
app/
  settings.py                    typed configuration (pydantic-settings)
  domain/<context>/              identity, project, task
    commands/ command_handlers/  one write use case per file
    entity.py                    PynamoDB entity: attributes and keys only (entities/ when several)
    repository.py                writes (conditional create/update/delete)
    query_service.py             XQueryService class: reads (query_services/ when several entities)
    schemas.py                   XRequest / XResponse pydantic models
    exceptions.py                business errors
  entrypoints/api/
    api_gateway_handler.py       FastAPI app, ROUTERS, error mapping, security headers
    v1/<resource>/<action>.py    one endpoint per file; __init__.py lists `routers`
  shared/
    auth/authorize.py            `with authorize_user(request.headers) as user:`
    clients/ entities/           Cognito client, DynamoDB base entity
    errors.py pagination.py types.py
tests/                           mirrors app/ (one test file and class per module); fixtures/ holds factories and mocks
```

Dependencies point one way only: entrypoints → domain → shared. `lint-imports` enforces this.

## Troubleshooting

- **`ValidationError` for `CognitoSettings` or `DynamoDBSettings` at startup**: a required variable is missing or malformed in `.env` (see [Configuration](#configuration)).
- **`NoCredentialsError` or `UnrecognizedClientException`**: boto3 found no valid AWS credentials. Set `AWS_PROFILE`, or put the keys in `.env` and start with `uv run --env-file .env ...`.
- **`ResourceNotFoundException` from DynamoDB**: the table does not exist in `REGION_NAME`, or `DYNAMODB_TABLE` has a different name.
- **Sign-in returns 502**: the app client does not allow `USER_PASSWORD_AUTH`, or the pool requires an extra step (MFA, new password) that this API does not support.
- **Every call returns 401**: the access token expired (1 hour by default). Get a new one from `POST /auth/token` or sign in again.
