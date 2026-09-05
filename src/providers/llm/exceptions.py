"""Public, provider-neutral exception contract for expression adapters."""

class ProviderError(Exception):
    """An expected provider operation failed."""

class ProviderConfigError(ProviderError):
    """Provider configuration is missing or invalid."""

class ProviderUnsupportedError(ProviderError):
    """The adapter does not implement the requested operation."""

class ProviderTransportError(ProviderError):
    """A remote endpoint could not complete the request."""
