from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from apps.organizations.models import Organization
from apps.organizations.schemas import OrganizationSchema, OrganizationCreateSchema
from ninja.security import SessionAuth

api = Router(auth=SessionAuth())

@api.get("/", response=List[OrganizationSchema])
def list_organizations(request):
    return Organization.objects.all()

@api.post("/", response={201: OrganizationSchema})
def create_organization(request, payload: OrganizationCreateSchema):
    return Organization.objects.create(**payload.dict())

@api.get("/{organization_id}", response=OrganizationSchema)
def get_organization(request, organization_id: int):
    return get_object_or_404(Organization, id=organization_id)

@api.put("/{organization_id}", response=OrganizationSchema)
def update_organization(request, organization_id: int, payload: OrganizationCreateSchema):
    organization = get_object_or_404(Organization, id=organization_id)
    for attr, value in payload.dict().items():
        setattr(organization, attr, value)
    organization.save()
    return organization

@api.delete("/{organization_id}", response={204: None})
def delete_organization(request, organization_id: int):
    organization = get_object_or_404(Organization, id=organization_id)
    organization.delete()
    return 204, None
