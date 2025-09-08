from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from apps.contacts.models import Contact
from apps.organizations.models import Organization
from apps.contacts.schemas import ContactSchema, ContactCreateSchema, ContactUpdateSchema
from ninja.security import SessionAuth

api = Router(auth=SessionAuth())

@api.get("/", response=List[ContactSchema])
def list_contacts(request):
    return Contact.objects.filter(user=request.auth)

@api.post("/", response={201: ContactSchema})
def create_contact(request, payload: ContactCreateSchema):
    org_id = payload.organization_id
    organization = get_object_or_404(Organization, id=org_id)
    data = payload.dict()
    data.pop('organization_id')
    contact = Contact.objects.create(**data, organization=organization, user=request.auth)
    return contact

@api.get("/{contact_id}", response=ContactSchema)
def get_contact(request, contact_id: int):
    contact = get_object_or_404(Contact, id=contact_id, user=request.auth)
    return contact

@api.put("/{contact_id}", response=ContactSchema)
def update_contact(request, contact_id: int, payload: ContactUpdateSchema):
    contact = get_object_or_404(Contact, id=contact_id, user=request.auth)
    org_id = payload.organization_id
    organization = get_object_or_404(Organization, id=org_id)
    data = payload.dict()
    data.pop('organization_id')
    for attr, value in data.items():
        setattr(contact, attr, value)
    contact.organization = organization
    contact.save()
    return contact

@api.delete("/{contact_id}", response={204: None})
def delete_contact(request, contact_id: int):
    contact = get_object_or_404(Contact, id=contact_id, user=request.auth)
    contact.delete()
    return 204, None
