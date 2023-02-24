import secrets

# Generate a random secret key
secret_key = secrets.token_urlsafe(32)
print(secret_key)