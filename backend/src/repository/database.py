import loguru
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, Session
from cassandra.cqlengine import connection
from src.config.manager import settings


class CassandraDatabase:
    def __init__(self):
        """Initialize the Cassandra database connection attributes."""
        self.cluster: Cluster | None = None
        self.session: Session | None = None

    def connect(self) -> None:
        """Initiate Cassandra connection using environment settings."""
        auth_provider = PlainTextAuthProvider(
            username=settings.CASSANDRA_USERNAME, password=settings.CASSANDRA_PASSWORD
        )
        try:
            self.cluster = Cluster(
                contact_points=[settings.CASSANDRA_HOST], port=settings.CASSANDRA_PORT, auth_provider=auth_provider
            )
            self.session = self.cluster.connect(keyspace="chatapp")
            connection.register_connection(name="default", session=self.session, default=True)  # Register connection

            loguru.logger.info("Successfully initialized connection to Cassandra")

        except Exception as e:
            loguru.logger.info(
                f"Could not connect using environment credentials, will attempt default credentials: \n {e}"
            )
            self._connect_default()

    def _connect_default(self) -> None:
        """Connect to Cassandra using default credentials and set up keyspace and user."""
        auth_provider = PlainTextAuthProvider(username="cassandra", password="cassandra")
        try:
            self.cluster = Cluster(
                contact_points=[settings.CASSANDRA_HOST], port=settings.CASSANDRA_PORT, auth_provider=auth_provider
            )
            self.session = self.cluster.connect()
            loguru.logger.info("Successfully connected using default new credentials")

            # Create keyspace and user if necessary
            self.session.execute(
                "CREATE KEYSPACE IF NOT EXISTS chatapp WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};"
            )
            loguru.logger.info("Successfully created new keyspace")
            self.session.set_keyspace("chatapp")
            self.session.execute(
                f"CREATE USER IF NOT EXISTS '{settings.CASSANDRA_USERNAME}' WITH PASSWORD '{settings.CASSANDRA_PASSWORD}' SUPERUSER;"
            )
            loguru.logger.info("Successfully created new superuser using environment credentials")

            loguru.logger.info("Will try to reconnect using new superuser")
            self.connect()

        except Exception as e:
            loguru.logger.error(f"Failed to connect with default credentials: \n {e}")
            # Optionally: clear the session/cluster state on failure
            self.cluster = None
            self.session = None
            raise

    def shutdown(self) -> None:
        """Shutdown the Cassandra connection."""
        if self.cluster:
            try:
                self.cluster.shutdown()
            except Exception as e:
                print(f"Error shutting down Cassandra connection: {e}")


# Singleton instance of CassandraDatabase
database: CassandraDatabase = CassandraDatabase()
