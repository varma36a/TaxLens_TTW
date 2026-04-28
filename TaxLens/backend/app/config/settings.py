from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_deployment: str = ""
    azure_foundry_project_id: str = ""
    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "taxlens"
    mongodb_server_selection_timeout_ms: int = 2000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def is_azure_openai_configured(self) -> bool:
        return all(
            [
                self.azure_openai_endpoint,
                self.azure_openai_api_key,
                self.azure_openai_deployment,
            ]
        )

settings = Settings()
