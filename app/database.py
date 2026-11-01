from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///./blog.db'

engine = create_async_engine(url=
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

AsyncSessionLocal = async_sessionmaker( 
    engine,                             # engine The async engine (from create_async_engine(...)) that holds the database connection details. Every session the factory creates uses this engine
    class_= AsyncSession,               # 
    expire_on_commit= False             # By default, after db.commit() SQLAlchemy marks all loaded objects as “expired”, so accessing an attribute triggers a new database load. In async code that implicit reload fails (usually with a MissingGreenlet error), because lazy loading can’t happen outside an await. Setting it to False keeps the object’s data available after commit.
)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
