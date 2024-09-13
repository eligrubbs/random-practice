from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAIL_FROM_ADDR: str
    EMAIL_TO_ADDR: str

    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAIL_FROM_ADDR)

settings = Settings()
