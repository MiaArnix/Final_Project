from pathlib import Path
import json
import sys
import os
import django
import shutil
from django.contrib.auth import get_user_model


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
sys.path.append(PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
AuthUser = get_user_model()

from identity.models import *  # noqa

users_file = Path(PROJECT_ROOT) / "data" / "users.json"
metadata_file = Path(PROJECT_ROOT) / "data" / "metadata.json"
identities_file = Path(PROJECT_ROOT) / "data" / "identities.json"

with users_file.open() as file:
    user_data = json.load(file)
    auth_users = user_data.get("users")

AuthUser.objects.all().delete()

for user in auth_users:
    if not AuthUser.objects.filter(username=user["username"]).exists():
        AuthUser.objects.create_user(
            username=user["username"],
            email=user["email"],
            password=user["password"]
        )

AuthUser.objects.create_superuser(
    username="admin",
    email="admin@localhost",
    password="admin"
)


with metadata_file.open() as file:
    metadata_data = json.load(file)
    genders = metadata_data.get("genders")
    name_contexts = metadata_data.get("name_contexts")
    relationship_types = metadata_data.get("relationship_types")
    identity_name_accesses = metadata_data.get("identity_name_accesses")

Gender.objects.all().delete()
NameContext.objects.all().delete()
RelationshipType.objects.all().delete()
IdentityNameAccess.objects.all().delete()

for gender in genders:
    if not Gender.objects.filter(name=gender["name"]).exists():
        Gender.objects.create(name=gender["name"])

for name_context in name_contexts:
    if not NameContext.objects.filter(name=name_context["name"]).exists():
        NameContext.objects.create(name=name_context["name"])

for relationship_type in relationship_types:
    if not RelationshipType.objects.filter(name=relationship_type["name"]).exists():
        RelationshipType.objects.create(name=relationship_type["name"])
        
for identity_name_access in identity_name_accesses:
    relationship_type = RelationshipType.objects.get(name=identity_name_access["relationship_type"])
    name_context = NameContext.objects.get(name=identity_name_access["name_context"])
    if not IdentityNameAccess.objects.filter(relationship_type=relationship_type, name_context=name_context).exists():
        IdentityNameAccess.objects.create(
            relationship_type=relationship_type,
            name_context=name_context
        )

with identities_file.open() as file:
    identity_data = json.load(file)
    identities = identity_data.get("identities")

Identity.objects.all().delete()

for identity in identities:
    owner = AuthUser.objects.get(username=identity["owner"])
    names = identity["names"]
    relationships = identity["relationships"]
    identity_instance = Identity.objects.create(
        owner=owner,
        is_public=identity["is_public"],
        gender=Gender.objects.get(name=identity["gender"])
    )

    for name in names:
        name_context = NameContext.objects.get(name=name["name_context"])
        if not IdentityName.objects.filter(identity=identity_instance, name_context=name_context).exists():
            IdentityName.objects.create(
                identity=identity_instance,
                name_context=name_context,
                name_value=name["name_value"],
                is_default=name["is_default"]
            )
            
    for relationship in relationships:
        consumer = AuthUser.objects.get(username=relationship["consumer"])
        relationship_type = RelationshipType.objects.get(name=relationship["relationship_type"])
        if not IdentityRelationship.objects.filter(identity=identity_instance, consumer=consumer).exists():
            IdentityRelationship.objects.create(
                identity=identity_instance,
                consumer=consumer,
                relationship_type=relationship_type
            )

print("Sample data load completed.")