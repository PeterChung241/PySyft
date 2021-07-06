# syft absolute
from syft.core.node.common.node_table import Base
from syft.core.node.common.node_table.utils import seed_db

# grid absolute
from app.core.config import settings
from app.db.session import SessionLocal, engine
from syft import Domain, Network

if settings.NODE_TYPE.lower() == "domain":
    node = Domain("Domain", db_engine=engine)
elif settings.NODE_TYPE.loser() == "network":
    node = Network("Network", db_engine=engine)
else:
    raise Exception(
        "Don't know NODE_TYPE "
        + str(settings.NODE_TYPE)
        + ". Please set "
        + "NODE_TYPE to either 'Domain' or 'Network'."
    )

node.loud_print()
Base.metadata.create_all(engine)

if len(node.setup):  # Check if setup was defined previously
    node.name = node.setup.node_name


if not len(node.roles):  # Check if roles were registered previously
    seed_db(SessionLocal())
