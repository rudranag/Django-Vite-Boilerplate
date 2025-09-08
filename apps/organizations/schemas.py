from ninja import ModelSchema
from apps.organizations.models import Organization

class OrganizationSchema(ModelSchema):
    class Config:
        model = Organization
        model_fields = ['id', 'name']

class OrganizationCreateSchema(ModelSchema):
    class Config:
        model = Organization
        model_fields = ['name']
