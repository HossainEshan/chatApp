from src.securities.hashing.hash import hash_generator


class PasswordGenerator:
    def generate_hashed_password(self, new_password: str) -> str:
        return hash_generator.generate_password_hash(password=new_password)

    def is_password_authenticated(self, password: str, hashed_password: str) -> bool:
        return hash_generator.is_password_verified(password=password, hashed_password=hashed_password)


def get_pwd_generator() -> PasswordGenerator:
    return PasswordGenerator()


pwd_generator: PasswordGenerator = get_pwd_generator()
