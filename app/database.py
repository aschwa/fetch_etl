from psycopg2 import connect
from config import settings


def write_login(user_login):
    """Connects to postgresql and writes a single UserLogin object
    to the database.

    Args:
        user_login (_type_): _description_
    """
    # Establish psql connection
    psql_creds = {
        "dbname": settings.POSTGRES_DB,
        "user": settings.POSTGRES_USER,
        "password": settings.POSTGRES_PASSWORD,
        "host": settings.POSTGRES_HOST,
        "port": settings.DATABASE_PORT,
    }
    psql_conn = connect(**psql_creds)
    psql_conn.autocommit = True
    cursor = psql_conn.cursor()

    # Insert single row into database
    cursor.execute(
        """INSERT INTO user_logins (user_id, device_type, masked_ip,\
        masked_device_id, locale, app_version, create_date)\
                  VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (
            user_login.user_id,
            user_login.device_type,
            user_login.masked_ip,
            user_login.masked_device_id,
            user_login.locale,
            user_login.app_version,
            user_login.create_date,
        ),
    )
    psql_conn.close()
