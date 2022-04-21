import uuid


def is_valid_uuid(uuid_to_test, version=4):
    try:
        return uuid.UUID(str(uuid_to_test)).version == version
    except ValueError:
        return False
