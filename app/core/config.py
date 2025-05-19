from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Informações do Projeto
    project_name: str
    environment: str = "development"
    debug: bool = False

    # Configurações da Embrapa
    base_url: str

    # JWT
    jwt_secret: str
    jwt_algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
