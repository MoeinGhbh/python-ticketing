import pytest
import sqlite3

# from db_create import
from app import models, routers, db_create

# @pytest.fixture()
# def db():
#     conn = sqlite3.connect(':memory:')
#     ct = CreateTable()
#     ct.create_table(conn)
#     return conn


# def test_sqlite(db):
#     aptusr = AddUser(db,'test@test.com','testpassword',0,0,0)
#     res = aptusr.insert_user()
#     assert res == True
