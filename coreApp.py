from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, text

engine = create_engine('sqlite:///:memory')

metadata_obj = MetaData()

user = Table(
    'user',
    metadata_obj,
    Column('user_id', Integer, primary_key=True),
    Column('user_name', String(40), nullable=False),
    Column('email_address', String(60)),
    Column('nickname', String(50), nullable=False)
)

user_prefs = Table(
    'user_prefs',
    metadata_obj,
    Column('pref_id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('user.user_id'), nullable=False),
    Column('pref_value', String(100))
)


for table in metadata_obj.sorted_tables:
    print(table)
    
    
metadata_obj.create_all(engine)

metadata_db_obj = MetaData()
financial_info = Table(
    'financial_info',
    metadata_db_obj,
    Column('id', Integer, primary_key=True),
    Column('value', String(100), nullable=False)
)

print(financial_info.primary_key)
print(financial_info.constraints)


sql = text('select * from user')
result = engine.execute(sql)

for row in result:
    print(row)

sql_insert = text("insert into user values(2, 'laisson', 'email@email.com', 'la')")
engine.execute(sql_insert)