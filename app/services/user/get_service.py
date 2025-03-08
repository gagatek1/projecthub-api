from app.core.cognito import Cognito


def get_users(cognito: Cognito):
    return cognito.get_users().get("Users")
