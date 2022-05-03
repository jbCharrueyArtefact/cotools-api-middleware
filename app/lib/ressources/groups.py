def list_groups(client, users=None):
    if users:
        return {user: client.list_groups(user) for user in users}
    else:
        return client.list_groups()


def get_details_groups(groups, client):
    return {group: client.get_details_group(group) for group in groups}


def get_groups_from_users(users, client):
    return {user: client.list_groups(user) for user in users}
