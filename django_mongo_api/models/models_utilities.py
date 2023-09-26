from mongoengine import Document, StringField, BooleanField, DateTimeField, EmbeddedDocument


class AbstractStixObject(Document):
    meta = {
        'allow_inheritance': True,
        'abstract': True,
        'collation': {
            'locale': 'en_US',
            'strength': 2
        }
    }

    id = StringField(primary_key=True, required=True, index=True, index_background=False)
    spec_version = StringField(required=False, default='2.1')
    expired = BooleanField(default=False)

class AbstractStixRelationalObject(AbstractStixObject):
    """
    STIX 2.1 Relational Object
    """
    meta = {
        'allow_inheritance': True,
        'abstract': True
    }

    created = DateTimeField(required=True)
    modified = DateTimeField(required=False, default=None)

class AbstractStixDomainObject(AbstractStixObject):
    """
    STIX 2.1 Domain Object
    """
    meta = {
        'allow_inheritance': True,
        'abstract': True,

    }

    created = DateTimeField(required=True)
    modified = DateTimeField(required=False, null=True)



class EmbeddedStixObject(EmbeddedDocument):
    meta = {'allow_inheritance': True, 'abstract': True, 'collection': 'stix'}

    id = StringField(primary_key=True, required=True, index=True, index_background=False)
    spec_version = StringField(required=True, default='2.1')


class EmbeddedStixDomainObject(EmbeddedStixObject):
    meta = {
        'allow_inheritance': True,
    }

    created = DateTimeField(required=True)
    modified = DateTimeField(required=True)


class EmbeddedStixCyberObject(EmbeddedStixObject):
    meta = {
        'allow_inheritance': True,
    }