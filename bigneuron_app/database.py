from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from bigneuron_app.config import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI, 
						convert_unicode=True,
						isolation_level=config.DB_ISOLATION_LEVEL,
						pool_recycle=3600)
db = scoped_session(sessionmaker(autocommit=False,
								 autoflush=False,
								 bind=engine))
Base = declarative_base()
Base.query = db.query_property()

from bigneuron_app.jobs.models import Job, JobStatus
from bigneuron_app.job_items.models import JobItemStatus
from bigneuron_app.users.models import User

def init_db():
	Base.metadata.drop_all(bind=engine)
	Base.metadata.create_all(bind=engine)


