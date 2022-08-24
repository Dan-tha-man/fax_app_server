from typing import Any

from src import crud
from src.schemas.room import RoomCreate, RoomUpdate
from src.tests.utils.utils import random_room_name, random_room_type
from src.tests.utils.room import create_random_room


def test_create_room(db: Any) -> None:
    room_create = RoomCreate(
        room_name=random_room_name(),
        room_type=random_room_type(),
    )
    room = crud.room.create(db, obj_in=room_create)
    crud.room.remove(db=db, primary_key=room.primary_key())

    assert room.PK == f"ROOM#{room.UUID()}"
    assert hasattr(room, "created_at")


def test_get_room(db: Any) -> None:
    new_room = create_random_room(db)
    room_from_db = crud.room.get(db, primary_key=new_room.primary_key())
    crud.room.remove(db, new_room.primary_key())

    assert room_from_db is not None
    assert new_room.room_name == room_from_db["room_name"]


def test_get_room_by_uuid(db: Any) -> None:
    new_room = create_random_room(db)
    room_from_db = crud.room.get_by_uuid(db, uuid=new_room.UUID())
    crud.room.remove(db, primary_key=new_room.primary_key())

    assert room_from_db is not None
    assert new_room.room_name == room_from_db.room_name


def test_update_room(db: Any) -> None:
    new_room = create_random_room(db)
    new_room_name = random_room_name()
    room_create_update = RoomUpdate(room_name=new_room_name)

    crud.room.update(db, db_obj=new_room, obj_in=room_create_update)
    room_from_db = crud.room.get(db, primary_key=new_room.primary_key())
    crud.room.remove(db, new_room.primary_key())

    assert room_from_db is not None
    assert new_room.room_name != room_from_db["room_name"]
    assert room_from_db["room_name"] == new_room_name