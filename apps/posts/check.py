

def post_data(data) -> bool:
    keys = (
        'title',
    )

    for key in keys:
        if data.get(key):
            return True
    return False


def post_author(request, post) -> bool:
    if request.user == post.user:
        return True
    return False
