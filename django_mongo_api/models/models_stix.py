import datetime

from mongoengine import StringField, ListField, DateTimeField, EmbeddedDocumentField, IntField, FloatField, \
    ReferenceField, EmailField, CASCADE

from django_mongo_api.models.models_utilities import AbstractStixDomainObject, AbstractStixObject, \
    EmbeddedStixCyberObject, EmbeddedStixDomainObject, AbstractStixRelationalObject


class OrganizationStix(AbstractStixDomainObject):
    meta = {'collection': 'OrganizationStix'}

    type = StringField(required=True, default='identity')
    name = StringField(required=True, null=False)
    description = StringField()
    roles = ListField(StringField(), default=[])
    identity_class = StringField(required=False, null=True)
    contact_information = StringField(required=False)
    sectors = ListField(StringField(), default=[])


class ThreatActorStix(AbstractStixDomainObject):
    meta = {'collection': 'ThreatActorStix'}

    type = StringField(required=True, default='threat-actor')
    name = StringField(required=True, null=False)
    description = StringField()
    threat_actor_types = ListField(StringField(), default=[])
    aliases = ListField(StringField(), default=[])
    first_seen = DateTimeField(allow_null=True)
    last_seen = DateTimeField(allow_null=True)
    roles = ListField(StringField(), default=[])
    goals = ListField(StringField(), default=[])
    sophistication = StringField(required=False)
    resource_level = StringField(required=False)
    primary_motivation = StringField(required=False)
    secondary_motivations = ListField(StringField(), default=[])
    personal_motivations= ListField(StringField(), default=[])


class StixObject(AbstractStixObject):
    meta = {
        'allow_inheritance': True,
        'collection': 'StixObjects'
    }

    type = StringField(required=True)
    stix = EmbeddedDocumentField('EmbeddedStixObject')
    added_on = DateTimeField(default=datetime.datetime.utcnow)


class OrganizationStixRelationship(AbstractStixRelationalObject):
    meta = {
        'collection': 'OrganizationStixRelationship',
    }

    type = StringField(required=False, default='relationship')
    relationship_type = StringField(required=True)
    description = StringField()
    source_ref = ReferenceField(OrganizationStix, null=False, reverse_delete_rule=CASCADE)
    target_ref = ReferenceField(StixObject, null=False, reverse_delete_rule=CASCADE)
    start_time = DateTimeField(required=False, default=datetime.datetime.utcnow)
    stop_time = DateTimeField(required=False)



class StixLocation(EmbeddedStixDomainObject):
    # meta = {'collection': 'StixLocation'}

    type = StringField(required=True, default='location')
    description = StringField(required=False, null=False, default=None)
    latitude = FloatField(required=False, min_value=-90, max_value=90)
    longitude = FloatField(required=False, min_value=-180, max_value=180)
    precision = FloatField(required=False)
    region = StringField(required=False, null=True)
    country = StringField(required=False, null=True)
    administrative_area = StringField(required=False)
    city = StringField(required=False)
    street_address = StringField(required=False)
    postal_code = StringField(required=False)


class StixAutonomousSystem(EmbeddedStixCyberObject):
    type = StringField(required=True, default='autonomous-system')
    number = IntField(required=True)
    rir = StringField(required=False)
    name = StringField()
    aliases = ListField(StringField())


class StixIpv4Addr(EmbeddedStixCyberObject):
    type = StringField(required=True, default='ipv4-addr')
    value = StringField(required=True)
    resolves_to_refs = ListField(ReferenceField(StixObject, null=False, default=[]))
    belongs_to_refs = ListField(ReferenceField(StixObject, null=False, default=[]))


class StixEmailAddr(EmbeddedStixCyberObject):
    type = StringField(required=True, default='email-addr')
    value = EmailField(required=True)
    displayName = StringField(required=False, null=True)