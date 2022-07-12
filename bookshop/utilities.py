def user_is_active(data_self_request):
    data = {}
    user_active = data_self_request.user.is_active

    if user_active:
        data['username'] = data_self_request.user.username
        data['user_is_active'] = user_active
    else:
        data['user_is_active'] = user_active

    return data