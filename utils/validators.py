def is_valid_query(query: str) -> bool:
    """Validate search query"""
    if not query:
        return False
    if len(query) < 2:
        return False
    if len(query) > 500:
        return False
    return True


def sanitize_query(query: str) -> str:
    """Sanitize search query"""
    return query.strip()
