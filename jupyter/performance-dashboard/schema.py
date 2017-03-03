# coding: utf-8

# Initially created with sqlacodegen --outfile schema.py url

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Float, ForeignKey, Integer, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


t_bench_run = Table(
    'bench_run', metadata,
    Column('RunId', Integer, nullable=False, unique=True, server_default=text("nextval('bench_run_id_seq'::regclass)")),
    Column('HostId', ForeignKey('machine.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    Column('RevisionId', ForeignKey('revision.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    Column('BenchStartDate', DateTime)
)


class Benchmark(Base):
    __tablename__ = 'benchmark'

    benchmark_name = Column(Text, primary_key=True, nullable=False)
    id = Column(Integer, nullable=False, unique=True, server_default=text("nextval('benchmark_id_seq'::regclass)"))
    parameter1 = Column(Text, primary_key=True, nullable=False)
    parameter2 = Column(Text, primary_key=True, nullable=False)
    component = Column(Text, primary_key=True, nullable=False)


class Benchstep(Base):
    __tablename__ = 'benchstep'

    benchmark_id = Column(ForeignKey('benchmark.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    benchstep_name = Column(Text, primary_key=True, nullable=False)
    id = Column(Integer, nullable=False, unique=True, server_default=text("nextval('benchstep_id_seq'::regclass)"))
    measure_type = Column(Text, primary_key=True, nullable=False, server_default=text("'Time'::text"))
    threshold = Column(BigInteger)
    step_parameter1 = Column(Text, primary_key=True, nullable=False)

    benchmark = relationship('Benchmark')


t_benchstep_result = Table(
    'benchstep_result', metadata,
    Column('benchstep_id', ForeignKey('benchstep.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    Column('value', Float(53), nullable=False),
    Column('id', Integer, nullable=False, unique=True, server_default=text("nextval('benchstep_result_id_seq'::regclass)")),
    Column('benchstep_result_date', DateTime),
    Column('bench_run_id', ForeignKey('bench_run.RunId', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
)


class Machine(Base):
    __tablename__ = 'machine'

    name = Column(Text, nullable=False, unique=True)
    id = Column(Integer, primary_key=True, server_default=text("nextval('machine_id_seq'::regclass)"))


class Revision(Base):
    __tablename__ = 'revision'

    version_id = Column(ForeignKey('version.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    revision = Column(BigInteger, primary_key=True, nullable=False)
    id = Column(Integer, nullable=False, unique=True, server_default=text("nextval('revision_id_seq'::regclass)"))

    version = relationship('Version')


t_rs = Table(
    'rs', metadata,
    Column('hostnameid', Integer),
    Column('hostname', Text),
    Column('revid', Integer),
    Column('rev', BigInteger),
    Column('benchmarkid', Integer),
    Column('benchmarkname', Text),
    Column('component', Text),
    Column('parameter1', Text),
    Column('parameter2', Text),
    Column('benchstepid', Integer),
    Column('benchstepname', Text),
    Column('version', Text),
    Column('value', Float(53)),
    Column('target', Float(53)),
    Column('resultdate', DateTime),
    Column('step_parameter1', Text)
)


class Threshold(Base):
    __tablename__ = 'threshold'

    benchstep_id = Column(BigInteger, primary_key=True)
    value75 = Column(Float(53), nullable=False)
    value100 = Column(Float(53), nullable=False)
    lessthan = Column(Boolean, nullable=False, server_default=text("true"))


class Threshold2(Base):
    __tablename__ = 'threshold2'

    benchname = Column(Text, primary_key=True, nullable=False)
    bench_parameter1 = Column(Text, primary_key=True, nullable=False, server_default=text("'*'::text"))
    bench_parameter2 = Column(Text, primary_key=True, nullable=False, server_default=text("'*'::text"))
    benchstepname = Column(Text, primary_key=True, nullable=False)
    benchstep_parameter1 = Column(Text, primary_key=True, nullable=False, server_default=text("'*'::text"))
    value75 = Column(Float(53))
    value100 = Column(Float(53))
    lessthan = Column(Boolean, nullable=False, server_default=text("true"))


class Version(Base):
    __tablename__ = 'version'

    version = Column(Text, nullable=False, unique=True)
    id = Column(Integer, primary_key=True, unique=True, server_default=text("nextval('version_id_seq'::regclass)"))
