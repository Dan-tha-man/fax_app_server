from typing import Dict, Any

from fastapi.testclient import TestClient

from src import crud
from src.core.config import settings
from src.tests.utils.room import create_random_room
from src.tests.utils.user import create_random_user

def test_create_event(
    client: TestClient,
    db: Any
) -> None:
    new_room = create_random_room(db)
    new_user = create_random_user(db)

    response = client.post(
        f"{settings.API_PREFIX_STR}/room/{new_room.UUID}/{new_user.username()}"
    )

    assert 200 <= response.status_code < 300

    event_uuid = str(response.content, 'utf-8').strip('"')
    assert event_uuid != None
    
    new_event = crud.event.get_by_uuid(db, new_room.UUID, event_uuid)
    assert new_event != None
    assert new_event.UUID == event_uuid
    assert new_event.event_creator == new_user.username()

    crud.event.remove(db, primary_key=new_event.primary_key())
    crud.user.remove(db, primary_key=new_user.primary_key())