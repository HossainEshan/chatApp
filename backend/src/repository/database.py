from typing import Optional

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, NoHostAvailable, Session
from cassandra.cqlengine import connection
from src.config.manager import settings


class CassandraDatabase:
    def __init__(self):
        """Initialize the Cassandra database connection attributes."""
        self.cluster: Optional[Cluster] = None
        self.session: Optional[Session] = None

    def connect(self):
        """Initiate Cassandra connection using settings."""
        auth_provider = PlainTextAuthProvider(
            username=settings.CASSANDRA_USERNAME, password=settings.CASSANDRA_PASSWORD
        )
        try:
            self.cluster = Cluster(
                contact_points=[settings.CASSANDRA_HOST], port=settings.CASSANDRA_PORT, auth_provider=auth_provider
            )
            self.session = self.cluster.connect(keyspace="chatapp")
            connection.register_connection(
                name="default", session=self.session, default=True
            )  # Name of the connection

        except NoHostAvailable as e:
            print(f"Error connecting to Cassandra: {e}")
            raise

    def shutdown(self):
        """Shutdown the Cassandra connection."""
        if self.cluster:
            try:
                self.cluster.shutdown()
            except Exception as e:
                print(f"Error shutting down Cassandra connection: {e}")


# Singleton instance of CassandraDatabase
database: CassandraDatabase = CassandraDatabase()
