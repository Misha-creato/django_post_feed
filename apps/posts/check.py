

def post_data(data) -> bool:
    keys = (
        'title',
    )

    for key in keys:
        if data.get(key):
            return True
    return False
