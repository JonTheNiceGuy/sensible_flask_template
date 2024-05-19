from . import Base
from flask_security import UserMixin, RoleMixin, AsaList, hash_password
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                    String, ForeignKey

class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(MutableList.as_mutable(AsaList()), nullable=True)

class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(
        Integer,
        primary_key=True
    )
    email = Column(
        String(255),
        unique=True
    )
    password = Column(
        String(255),
        nullable=False
    )
    active = Column(Boolean())
    fs_uniquifier = Column(
        String(64),
        unique=True,
        nullable=False
    )
    roles = relationship(
        'Role',
        secondary='roles_users',
        backref=backref(
            'users',
            lazy='dynamic'
        )
    )

def initial_user_setup():
    from app import app, db_session
    app.security.datastore.find_or_create_role(
        name="user", permissions={"user-read", "user-write"}
    )
    app.security.datastore.find_or_create_role(
        name="admin", permissions={"user-read", "user-write", "admin"}
    )
    db_session.commit()
    first_user = db_session.query(User).first()
    if not first_user:
        import os
        app.security.datastore.create_user(
            email=os.environ.get('FIRST_ADMIN_USERNAME', 'admin@example.org'),
            password=hash_password(os.environ.get('FIRST_ADMIN_PASSWORD', 'Default-Password-Yes1')),
            roles=["admin"]
        )
        db_session.commit()
