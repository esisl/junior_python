class AccountError(Exception):
    """Base exception for accounts module"""
    pass

class UserAlreadyExistsError(AccountError):
    pass

class InvalidCredentialsError(AccountError):
    pass

class TokenRevokedError(AccountError):
    pass

class ProfileDeletionError(AccountError):
    pass