from datetime import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.util import uuid_from_time
from src.config.manager import settings


# Define the base Cassandra model
class BaseCassandraModel(Model):
    __abstract__ = True  # Indicating this model will not be used directly
    __keyspace__ = settings.CASSANDRA_KEYSPACE
    __connection__ = "default"


# Message Model
class Message(BaseCassandraModel):
    # Define primary key with clustering order
    chatroom_id = columns.UUID(primary_key=True, partition_key=True)  # Partition by chatroom ID
    message_id = columns.UUID(
        primary_key=True, default=lambda: uuid_from_time(datetime.now())
    )  # Clustering key for message
    message_text = columns.Text(required=True)
    user_id = columns.UUID(required=True)
    created_at = columns.DateTime(default=datetime.now)  # No clustering_order here

    __table_name__ = "messages"

    # Set the primary key with clustering order
    __primary_key__ = (chatroom_id, message_id, created_at)

    class Meta:
        # Specify clustering order here
        clustering_order = {"created_at": "DESC"}


# User Model
class User(BaseCassandraModel):
    user_id = columns.UUID(primary_key=True, default=lambda: uuid_from_time(datetime.now()))  # Partition by user ID
    username = columns.Text(required=True, index=True)  # Keep username as a text field
    email = columns.Text(required=True, index=True)
    hashed_password = columns.Text(required=True)

    __table_name__ = "users"  # Explicitly define table name

    __options__ = {
        "compaction": {"class": "LeveledCompactionStrategy"},  # Recommended for read-heavy apps
    }


# Chatroom Model
class Chatroom(BaseCassandraModel):
    chatroom_id = columns.UUID(
        primary_key=True, default=lambda: uuid_from_time(datetime.now())
    )  # Partition by chatroom ID
    chatroom_name = columns.Text(index=True)  # Index chatroom_name for efficient name-based searches
    users = columns.Set(columns.UUID)  # Use a Set of UUIDs for users in the chatroom
    created_at = columns.DateTime(default=datetime.now)

    __table_name__ = "chatrooms"
