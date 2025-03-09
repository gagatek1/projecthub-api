from app.core.cognito import Cognito


def get_users(cognito: Cognito):
    return cognito.shows_users().get("Users")


def get_user(id: str, cognito: Cognito):
    return cognito.show_user(id)
