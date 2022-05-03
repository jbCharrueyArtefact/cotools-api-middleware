from fastapi import Depends, HTTPException, Header

from app.dependencies import get_essential_contact_client


def is_allowed(
    project_id: str = None,
    mail: str = Header(None),
    client=Depends(get_essential_contact_client),
):
    if project_id and mail:
        if not client.is_owner(project_id, mail):
            raise HTTPException(
                403, "not allowed: you're not owner of this project"
            )
