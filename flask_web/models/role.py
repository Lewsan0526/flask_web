# -*- coding: utf-8 -*-

from ..ext import db


class Permission(object):
    FOLLOW = 1  # 0x01
    COMMENT = 2  # 0x02
    WRITE = 4  # 0x04
    MODERATE = 8  # 0x08
    ADMIN = 16  # 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    ROLES = {
        'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
        'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                      Permission.WRITE, Permission.MODERATE],
        'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE,
                          Permission.ADMIN],
    }

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if not self.permissions:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        default_role = "User"
        for name, roles in Role.ROLES.items():
            role = Role.query.filter_by(name=name).first()
            if not role:
                role = Role(name=name)
            role.reset_permissions()
            for perm in roles:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def reset_permissions(self):
        self.permissions = 0

    def __repr__(self):
        return '<Role %r>' % self.name
