from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # General configuration
    project_name: str
    environment: str = "development"
    debug: bool = False

    # Embrapa base URL
    base_url: str

    # JWT configuration
    secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int
    database_url: str

    model_config = SettingsConfigDict(env_file=".env")

    # URL builders for each dataset
    @property
    def production_url(self) -> str:
        return f"{self.base_url}?opcao=opt_02"

    @property
    def processing_url(self) -> str:
        return f"{self.base_url}?opcao=opt_03"

    @property
    def commercialization_url(self) -> str:
        return f"{self.base_url}?opcao=opt_04"

    @property
    def importation_url(self) -> str:
        return f"{self.base_url}?opcao=opt_05"

    @property
    def exportation_url(self) -> str:
        return f"{self.base_url}?opcao=opt_06"

settings = Settings()