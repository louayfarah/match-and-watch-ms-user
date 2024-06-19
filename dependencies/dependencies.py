import core
import core.databases
import core.databases.postgres
import core.databases.postgres.postgres


def get_db():
    db = core.databases.postgres.postgres.session_local()
    try:
        yield db
    finally:
        db.close()
