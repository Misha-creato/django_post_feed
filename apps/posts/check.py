

def post_data(data) -> bool:
    if data.get('title'):
        return True
    return False
