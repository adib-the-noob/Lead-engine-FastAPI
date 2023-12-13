class BaseConfig:
    DATABASE_URL = "postgresql://postgres:postgres@db:5432/leadengine-dev-db"
    SECRET_KEY = "c19a0d857803863a4039cdb12d61d017e8b0e533282b9780991a2f2852e35e8b"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS = 30

config = BaseConfig()
