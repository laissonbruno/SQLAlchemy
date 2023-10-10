from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import Column, create_engine, Integer, String, ForeignKey, inspect, select, func


Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"
    # atributos
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    
    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"
    
    
class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
    
    user = relationship("User", back_populates="address")
    
    
    def __repr__(self):
        return f"Address(id={self.id}, email={self.email_address})"
    


# conexão com o banco de dados

engine = create_engine("sqlite://")

# criando as classes como tabelas no banco de dados
Base.metada.create_all(engine)

inspetor_engine = inspect(engine)


with Session(engine) as session:
    laisson = User(
        name='Laisson',
        fullname='Laisson Germano',
        address=[Address(email_address='laisson@email.com')]
    )


    bruno = User(
        name='Bruno',
        fullname='Bruno Germano',
        address=[Address(email_address='bruno@email.com')]
    )
    
    # enviando para o banco
    session.add_all([laisson, bruno])
    
    session.commit()
    

stmt = select(User).where(User.name.in_(['laisson']))
for user in session.scalars(stmt):
    print(user)
    
    
stmt_address = select(Address).where(Address.user_id.in_([2]))
for address in session.scalars(stmt_address):
    print(address)
    
stmt_order = select(User).order_by(User.fullname.desc())

for result in session.scalars(stmt_order):
    print(result)
    
stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)
for result in session.scalars(stmt_join):
    print(result)
    
connection = engine.connect()
results = connection.execute(stmt_join).fetchall()

for result in results:
    print(result)
    
stmt_count = select(func.count('*')).select_from(User)
for result in session.scalars(stmt_count):
    print(result)
