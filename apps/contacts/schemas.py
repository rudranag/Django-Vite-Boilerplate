from ninja import Schema, ModelSchema
from apps.contacts.models import Contact
from apps.organizations.schemas import OrganizationSchema
from typing import Optional

class ContactSchema(ModelSchema):
    organization: OrganizationSchema

    class Config:
        model = Contact
        model_fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'organization']


class ContactCreateSchema(Schema):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    organization_id: int

class ContactUpdateSchema(ContactCreateSchema):
    pass
