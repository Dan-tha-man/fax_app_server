from typing import Any

from src import crud
from src.schemas.room import RoomCreate, RoomUpdate
from src.tests.utils.utils import random_room_name, random_room_type
from src.tests.utils.room import create_random_room


def test_create_room(db: Any) -> None:
    room_create = RoomCreate(
        name=random_room_name,
        room_type=random_room_type,
    )
    room = crud.room.create(db, obj_in=room_create)
    crud.room.remove(db, room.primary_key())

    assert room.PK == f"ROOM#{room.UUID()}"
    assert hasattr(room, "created_at")


def test_get_room(db: Any) -> None:
    room = create_random_room(db)
    room_from_db = crud.room.get(db, primary_key=room.primary_key())
    crud.user.remove(db, room.primary_key())

    assert room_from_db is not None
    assert room.name == room_from_db["name"]


def test_get_room_by_uuid(db: Any) -> None:
    room = create_random_room(db)
    room_from_db = crud.room.get_by_username(db, room=room.UUID())
    crud.user.remove(db, room.primary_key())

    assert room_from_db is not None
    assert room.name == room_from_db.name


def test_update_room(db: Any) -> None:
    room = create_random_room(db)
    new_room_name = random_room_name()
    room_create_update = RoomUpdate(name=new_room_name)

    crud.room.update(db, db_obj=room, obj_in=room_create_update)
    room_from_db = crud.room.get(db, primary_key=room.primary_key())
    crud.user.remove(db, room.primary_key())

    assert room_from_db is not None
    assert room.name == room_from_db["name"]