from generic_organization_service.models import ConnectionAttribute, UserConnection, Organization
from django.core.exceptions import ObjectDoesNotExist


def list_user_connections(organization: Organization):
    return UserConnection.objects.filter(organization=organization)


def add_user_connection(connection_id, organization: Organization) -> UserConnection:
    user_connection = get_user_connection(connection_id=connection_id, organization=organization)
    if not user_connection:
        user_connection = UserConnection.objects.create(connection_id=connection_id, organization=organization)

    return user_connection


def add_connection_attribute(name, value, user_connection: UserConnection) -> ConnectionAttribute:
    connection_attribute = get_connection_attribute(name, value, user_connection)
    if not connection_attribute:
        connection_attribute = ConnectionAttribute.objects.create(
            name=name,
            value=value,
            user_connection=user_connection)
    return connection_attribute


def get_connection_attribute(name, value, user_connection: UserConnection) -> ConnectionAttribute:
    connection_attribute = None
    try:
        filters = dict()
        filters['name'] = name
        filters['value'] = value
        filters['user_connection'] = user_connection

        connection_attribute = ConnectionAttribute.objects.filter(**filters)

        if connection_attribute:
            connection_attribute = connection_attribute[0]
    except ObjectDoesNotExist:
        connection_attribute = None
    return connection_attribute

def get_user_connection(connection_id=None, organization: Organization = None) -> UserConnection:
    user_connection = None
    try:
        filters = dict()
        if connection_id:
            filters['connection_id'] = connection_id
        if organization:
            filters['organization'] = organization

        connections = UserConnection.objects.filter(**filters)

        if connections:
            user_connection = connections[0]
    except ObjectDoesNotExist:
        user_connection = None
    return user_connection