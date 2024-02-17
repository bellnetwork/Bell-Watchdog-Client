def get_service_name(service: str) -> str:
    """Returns the service name for a given access details string."""
    parts = service.split("/")
    if len(parts) == 2:
        return parts[1]
    else:
        return service