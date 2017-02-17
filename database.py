from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
# from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import Session, relationship, backref,\
                                joinedload_all
from sqlalchemy.orm.collections import attribute_mapped_collection
Base = declarative_base()

class Network(Base):
    __tablename__ = 'network'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey(id))
    # name = Column(String(250), nullable=False)

    children = relationship("Network",

                        # cascade deletions
                        cascade="all, delete-orphan",

                        # many to one + adjacency list - remote_side
                        # is required to reference the 'remote'
                        # column in the join condition.
                        backref=backref("parent", remote_side=id),

                        # children will be represented as a dictionary
                        # on the "name" attribute.
                        collection_class=attribute_mapped_collection('name'),
                    )

    # def __init__(self, parent=None):
    #     self.parent = parent

    def __repr__(self):

        return '%d (%s)' %(self.id, str(self.parent_id))

class Run(Base):
    __tablename__ = 'run'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    levelsCompleted = Column(Integer)
    score = Column(Float)
    accuracy = Column(Float)
    network_id = Column(Integer, ForeignKey('network.id'))
    network = relationship(Network)

    def __repr__(self):

        return "%d: %s, %d levels, %.2lf points, %s accuracy" % (self.id, self.network, self.levelsCompleted, self.score, str(self.accuracy))

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///history.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

def makeSession():
    from sqlalchemy.orm import sessionmaker

    DBSession = sessionmaker(bind=engine)
    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call
    # session.commit(). If you're not happy about the changes, you can
    # revert all of them back to the last commit by calling
    # session.rollback()
    session = DBSession()

    return session



if __name__ == "__main__":
    from sqlalchemy.orm import sessionmaker

    DBSession = sessionmaker(bind=engine)
    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call
    # session.commit(). If you're not happy about the changes, you can
    # revert all of them back to the last commit by calling
    # session.rollback()
    session = DBSession()

    for u in session.query(Run).order_by(Run.score.desc())[:10]:
        print u

    print
    print

    for u in session.query(Network).join(Run).order_by(Run.score.desc())[:20]:
        print u
