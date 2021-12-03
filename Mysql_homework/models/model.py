from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from static.tests_config import TestsConfig

Base = declarative_base()


class RequestsCount(Base):
    __tablename__ = TestsConfig.TABLES_NAMES[0]
    __table_args__ = {'mysql_charset': 'utf8'}

    count = Column(Integer, primary_key=True)


class MethodsCount(Base):
    __tablename__ = TestsConfig.TABLES_NAMES[1]
    __table_args__ = {'mysql_charset': 'utf8'}

    method = Column(String(10), primary_key=True)
    count = Column(Integer, nullable=False)


class PopularRequests(Base):
    __tablename__ = TestsConfig.TABLES_NAMES[2]
    __table_args__ = {'mysql_charset': 'utf8'}

    url = Column(String(100), primary_key=True)
    count = Column(Integer, nullable=False)


class Biggest4XXRequests(Base):
    __tablename__ = TestsConfig.TABLES_NAMES[3]
    __table_args__ = {'mysql_charset': 'utf8'}

    row_id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(250), nullable=False, primary_key=True)
    status = Column(String(3), nullable=False, primary_key=True)
    size = Column(String(10), nullable=False, primary_key=True)
    ip = Column(String(15), nullable=False, primary_key=True)


class Popular5XXRequestsIP(Base):
    __tablename__ = TestsConfig.TABLES_NAMES[4]
    __table_args__ = {'mysql_charset': 'utf8'}

    ip = Column(String(15), primary_key=True)
    count = Column(Integer, nullable=False)
