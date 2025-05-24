from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Configurações gerais
    project_name: str
    environment: str = "development"
    debug: bool = False

    # URL base da Embrapa
    base_url: str

    # Configurações de JWT
    jwt_secret: str
    jwt_algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")

    # Propriedades para construir URLs específicas
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