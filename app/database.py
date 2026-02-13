from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///data/confusion.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class LabeledSample(Base):
    __tablename__ = "samples"
    id = Column(Integer, primary_key=True)
    backspace_rate = Column(Float)
    typing_speed = Column(Float)
    pause_count = Column(Integer)
    scroll_changes = Column(Integer)
    window_switches = Column(Integer)
    label = Column(String)  # fluent | thinking | confused | idle

Base.metadata.create_all(engine)
