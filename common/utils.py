# -*- coding:utf-8 -*-

from django.core import serializers
#import simplejson as json
from types import NoneType
from django.db.models.manager import Manager
from django.db.models import Model
import datetime

import logging
log = logging.getLogger('django')


def DateTimeNowToSql():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')


def GetObjectOrNone(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def get_class( kls ):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


def ru_month(num):
    MONTHS = {
        1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь',
        7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь',
        12: 'Декабрь'
    }
    return MONTHS[num]


class JsonResponseContext(object):
    def __init__(self, request, *args, **kwargs):
        self.get = request.GET
        self.names = kwargs['names']
        self.values = {}
        self.errors = []
        self.result = True
        self.json = {}
        self.qs = False
        self.data = False
        self.check()

    def check(self):
        for n in self.names:
            if n in self.get and self.get[n] != '':
                self.values[n] = self.get[n]
            else:
                self.errors.append("Request parameter \'%s\' not found!" % n)
        if len(self.errors) > 0:
            self.result = False
        return self.result

    def to_json(self):
        if self.qs:
            self.json['data'] = json.loads(serializers.serialize('json', self.qs, indent=4))
        if len(self.errors) > 0:
            self.json['result'] = 0
            self.json['errors'] = self.errors
        else:
            self.json['result'] = 1
            self.json['values'] = self.values
        return json.dumps(self.json, indent=2)



def GetInstanceValues(instance, go_into={}, exclude=(), extra=()):
    SIMPLE_TYPES = (int, long, str, list, dict, tuple, bool, float, bool,
                    unicode, NoneType)
    if not isinstance(instance, Model):
        raise TypeError("Argument is not a Model")

    value = { 'pk': instance.pk, }

    # check for simple string instead of tuples
    # and dicts; this is shorthand syntax
    if isinstance(go_into, str):
        go_into = {go_into: {}}

    if isinstance(exclude, str):
        exclude = (exclude,)

    if isinstance(extra, str):
        extra = (extra,)

    # process the extra properties/function/whatever
    for field in extra:
        property = getattr(instance, field)

        if callable(property):
            property = property()

        if isinstance(property, SIMPLE_TYPES):
            value[field] = property
        else:
            value[field] = repr(property)

    field_list = instance._meta.get_all_field_names()
    for field in field_list:
        try:
            property = getattr(instance, field)
        except:
            continue

        if field in exclude or field[0] == '_':
            # if it's in the exclude tuple, ignore it
            # if it's a "private" field, ignore it
            # if it's an instance of manager (this means a more complicated
            # relationship), ignore it
            continue
        elif isinstance(property, Manager):
            value[field] = repr(property.reverse())
        elif go_into.has_key(field):
            # if it's in the go_into dict, make a recursive call for that field
            try:
                field_go_into = go_into[field].get('go_into', {})
            except AttributeError:
                field_go_into = {}

            try:
                field_exclude = go_into[field].get('exclude', ())
            except AttributeError:
                field_exclude = ()

            try:
                field_extra = go_into[field].get('extra', ())
            except AttributeError:
                field_extra = ()

            value[field] = GetInstanceValues(property,
                                      field_go_into,
                                      field_exclude,
                                      field_extra)
        else:
            if isinstance(property, Model):
                # if it's a model, we need it's PK #
                value[field] = property.pk
            elif isinstance(property, (datetime.date,
                                       datetime.time,
                                       datetime.datetime)):
                # if it's a date/time, we need it #
                # in iso format for serialization #
                value[field] = property.isoformat()
            else:
                # else, we just put the value #
                if callable(property):
                    property = property()

                if isinstance(property, SIMPLE_TYPES):
                    value[field] = property
                else:
                    value[field] = repr(property)

    return value


def get_values_originsl(instance, go_into={}, exclude=(), extra=()):
    """
    Transforms a django model instance into an object that can be used for
    serialization. Also transforms datetimes into timestamps.

    @param instance(django.db.models.Model) - the model in question
    @param go_into(dict) - relations with other models that need expanding
    @param exclude(tuple) - fields that will be ignored
    @param extra(tuple) - additional functions/properties which are not fields

    Usage:
    get_values(MyModel.objects.get(pk=187),
               {'user': {'go_into': ('clan',),
                         'exclude': ('crest_blob',),
                         'extra': ('get_crest_path',)}},
               ('image'))

    """

    SIMPLE_TYPES = (int, long, str, list, dict, tuple, bool, float, bool,
                    unicode, NoneType)

    if not isinstance(instance, Model):
        raise TypeError("Argument is not a Model")

    value = {
        'pk': instance.pk,
        }

    # check for simple string instead of tuples
    # and dicts; this is shorthand syntax
    if isinstance(go_into, str):
        go_into = {go_into: {}}

    if isinstance(exclude, str):
        exclude = (exclude,)

    if isinstance(extra, str):
        extra = (extra,)

    # process the extra properties/function/whatever
    for field in extra:
        property = getattr(instance, field)

        if callable(property):
            property = property()

        if isinstance(property, SIMPLE_TYPES):
            value[field] = property
        else:
            value[field] = repr(property)

    field_options = instance._meta.get_all_field_names()
    for field in field_options:
        try:
            property = getattr(instance, field)
        except:
            continue

        if field in exclude or field[0] == '_' or isinstance(property, Manager):
            # if it's in the exclude tuple, ignore it
            # if it's a "private" field, ignore it
            # if it's an instance of manager (this means a more complicated
            # relationship), ignore it
            continue
        elif go_into.has_key(field):
            # if it's in the go_into dict, make a recursive call for that field
            try:
                field_go_into = go_into[field].get('go_into', {})
            except AttributeError:
                field_go_into = {}

            try:
                field_exclude = go_into[field].get('exclude', ())
            except AttributeError:
                field_exclude = ()

            try:
                field_extra = go_into[field].get('extra', ())
            except AttributeError:
                field_extra = ()

            value[field] = get_values(property,
                                      field_go_into,
                                      field_exclude,
                                      field_extra)
        else:
            if isinstance(property, Model):
                # if it's a model, we need it's PK #
                value[field] = property.pk
            elif isinstance(property, (datetime.date,
                                       datetime.time,
                                       datetime.datetime)):
                # if it's a date/time, we need it #
                # in iso format for serialization #
                value[field] = property.isoformat()
            else:
                # else, we just put the value #
                if callable(property):
                    property = property()

                if isinstance(property, SIMPLE_TYPES):
                    value[field] = property
                else:
                    value[field] = repr(property)

    return value

from django.core.exceptions import ObjectDoesNotExist


def model_todict(obj, exclude=['AutoField', 'OneToOneField']):
    #exclude=['AutoField', 'ForeignKey', 'OneToOneField']
    log.info("model_to_dict")
    tree = {}
    for field_name in obj._meta.get_all_field_names():
        print "Fieldname: %s" % field_name
        try:
            field = getattr(obj, field_name)
        except (ObjectDoesNotExist, AttributeError):
            print "Except error:"
            continue
        if field.__class__.__name__ in ['RelatedManager', 'ManyRelatedManager']:
            print "Field CN: %s in 'RelatedManager', 'ManyRelatedManager'" % field.__class__.__name__
            if field.model.__name__ in exclude:
                print "Field is in Exclude"
                continue
            if field.__class__.__name__ == 'ManyRelatedManager':
                print "Field .__class__.__name__ %s == ManyRelatedManager" % field.__class__.__name__
                exclude.append(obj.__class__.__name__)
            subtree = []
            for related_obj in getattr(obj, field_name).all():
                value = model_todict(related_obj, exclude=exclude)
                if value:
                    subtree.append(value)
                    print "Append value to suubtree: %s" % value
            if subtree:
                tree[field_name] = subtree
            continue
        field = obj._meta.get_field_by_name(field_name)[0]
        print "field: %s" % field
        if field.__class__.__name__ in exclude:
            print "Field %s __class__.__name__ %s is in Exclude" % (field, field.__class__.__name__)
            continue

        if field.__class__.__name__ == 'RelatedObject':
            print "Field.__name__.__name__ %s == RelatedObject" % field.__class__.__name__
            exclude.append(field.model.__name__)
            tree[field_name] = model_to_dict(getattr(obj, field_name), \
                exclude=exclude)
            continue

        value = getattr(obj, field_name)
        if not isinstance(value, str):
            value = repr(value)
        #value.decode('utf-8')
        print "Value: %s" % value
        if value:
            tree[field_name] = value
    print "Tree: %s" % tree
    return tree

