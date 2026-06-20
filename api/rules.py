import rules
from identity.models import IdentityRelationship, IdentityNameAccess

@rules.predicate
def is_identity_owner(user, identity):
    return identity.owner == user

@rules.predicate
def is_public(user, identity):
    return identity.is_public

@rules.predicate
def has_relationship(user, identity):
    return IdentityRelationship.objects.filter(
        identity=identity,
        consumer=user
    ).exists()

# it is allowed to read identity if the identity is public OR the user is superuser OR identity owner OR has a relationship with the identity
rules.add_rule('identity.read_identity', is_public |  rules.is_superuser | is_identity_owner | has_relationship)

# it is allowed to write identity if the user is superuser OR identity owner
rules.add_rule('identity.write_identity', rules.is_superuser | is_identity_owner)

# it is allowed to delete identity if the user is superuser OR identity owner
rules.add_rule('identity.delete_identity', rules.is_superuser | is_identity_owner)

# it is always allowed to read metadata 
rules.add_rule('identity.read_metadata', rules.always_allow)

# it is allowed to write metadata if the user is superuser
rules.add_rule('identity.write_metadata', rules.is_superuser)