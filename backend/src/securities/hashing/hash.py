from passlib.context import CryptContext
from src.config.manager import settings


class HashGenerator:
    def __init__(self):
        # Set up a single hashing context
        self._hash_ctx: CryptContext = CryptContext(schemes=[settings.HASHING_ALGORITHM_LAYER_1], deprecated="auto")

    def generate_password_hash(self, password: str) -> str:
        """
        Hashes the user's password using the configured algorithm (e.g., bcrypt, Argon2).
        """
        return self._hash_ctx.hash(password)

    def is_password_verified(self, password: str, hashed_password: str) -> bool:
        """
        Verifies the user's password against the stored hash.
        """
        return self._hash_ctx.verify(password, hashed_password)


def get_hash_generator() -> HashGenerator:
    return HashGenerator()


hash_generator: HashGenerator = get_hash_generator()
