

def profile_data(data):
    keys = (
        'username',
    )

    for key in keys:
        if data.get(key, 'valid'):
            return True
        return False
