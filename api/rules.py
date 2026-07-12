import rules
from identity.models import IdentityRelationship

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


# identity rules
# it is allowed to read identity if the identity is public OR the user is superuser OR identity owner OR has a relationship with the identity
rules.add_perm('identity.read_identity', is_public |  rules.is_superuser | is_identity_owner | has_relationship)

# it is allowed to write identity if the user is superuser OR identity owner
rules.add_perm('identity.write_identity', rules.is_superuser | is_identity_owner)

# it is allowed to delete identity if the user is superuser OR identity owner
rules.add_perm('identity.delete_identity', rules.is_superuser | is_identity_owner)

# identity relationship rules
# it is allowed to read or write identity relationship if the user is superuser OR identity owner
rules.add_perm('identity.access_identity_relationship', rules.is_superuser | is_identity_owner)

# identity name rules
# it is allowed to read or write identity name if the user is superuser OR identity owner
rules.add_perm('identity.access_identity_name', rules.is_superuser | is_identity_owner)

# metadata rules
# it is allowed to write metadata if the user is superuser
rules.add_perm('identity.write_metadata', rules.is_superuser)

