"""Optional error and performance monitoring configuration."""

from config import settings


def configure_monitoring() -> None:
    if settings.SENTRY_DSN:
        import sentry_sdk

        sentry_sdk.init(dsn=settings.SENTRY_DSN, enable_tracing=True)

    if settings.NEW_RELIC_CONFIG_FILE:
        import newrelic.agent

        newrelic.agent.initialize(settings.NEW_RELIC_CONFIG_FILE)