import re

from django.db.models import EmailField
from django.db.models.loading import get_models
from django.conf import settings

#TODO: create class Introspect in order to make this code reusable

field_replacers = {
    'AutoField': '"SKIP"',
    'ForeignKey': '"SKIP"',
    'ManyToManyField': '"SKIP"',
    'OneToOneField': '"SKIP"',
    'SlugField': '"SKIP"', # we probably don't want to change slugs
    'DateField': '"date"',
    'DateTimeField': '"datetime"',
    'BooleanField': '"bool"',
    'NullBooleanField': '"bool"',
    'IntegerField': '"integer"',
    'SmallIntegerField': '"small_integer"',
    'PositiveIntegerField': '"positive_integer"',
    'PositiveSmallIntegerField': '"positive_small_integer"',
    'DecimalField': '"decimal"',
    'UUIDField': '"SKIP"', # we probably don't want to change uuids
    'FileField': '"SKIP"', # we probably don't want to change file fields
    'UpdateUserField': '"SKIP"', # we probably don't want to change last_modified_user
}

# NB - order matters. 'address' is more generic so should be at the end.
charfield_replacers = [
    (r'(\b|_)full_name\d*', '"name"'),
    (r'(\b|_)first_name\d*', '"first_name"'),
    (r'(\b|_)last_name\d*', '"last_name"'),
    (r'(\b|_)user_name\d*', '"username"'),
    (r'(\b|_)username\d*', '"username"'),
    (r'(\b|_)name\d*', '"name"'),
    (r'(\b|_)email\d*', '"email"'),
    (r'(\b|_)town\d*', '"city"'),
    (r'(\b|_)city\d*', '"city"'),
    (r'(\b|_)post_code\d*', '"postcode"'),
    (r'(\b|_)postcode\d*', '"postcode"'),
    (r'(\b|_)zip\d*', '"zip_code"'),
    (r'(\b|_)zipcode\d*', '"zip_code"'),
    (r'(\b|_)zip_code\d*', '"zip_code"'),
    (r'(\b|_)telephone\d*', '"phone_number"'),
    (r'(\b|_)phone\d*', '"phone_number"'),
    (r'(\b|_)mobile\d*', '"phone_number"'),
    (r'(\b|_)tel\d*\b', '"phone_number"'),
    (r'(\b|_)state\d*\b', '"state"'),
    (r'(\b|_)address\d*', '"address"'),
]


integerfield_replacers = [
    (r'(\b|_)version\d*', '"SKIP"'),  # skip django-reversion specific fields by default
]


def get_replacer_for_field(field):
    # Some obvious ones:
    if isinstance(field, EmailField):
        return '"email"'

    # Use choices, if available and not skipped in settings
    choices = getattr(field, 'choices', None)
    if choices is not None and len(choices) > 0:
        if getattr(settings, 'ANONYMIZER_SKIP_CHOICES', False):
            return '"SKIP"'
        return '"choice"'

    field_type = field.get_internal_type()
    if field_type == "CharField" or field_type == "TextField":
        # Guess by the name

        # First, go for complete match
        for pattern, result in charfield_replacers:
            if re.match(pattern + "$", field.attname):
                return result

        # Then, go for a partial match.
        for pattern, result in charfield_replacers:
            if re.search(pattern, field.attname):
                return result

        # Nothing matched.
        if field_type == "TextField":
            return '"lorem"'

        # Just try some random chars
        return '"varchar"'

    # IntegerFields
    if field_type.endswith('IntegerField'):
        for pattern, result in integerfield_replacers:
            if re.match(pattern + "$", field.attname):
                return result

    try:
        r = field_replacers[field_type]
    except KeyError:
        print('Cannot guess ', field_type)
        r = "UNKNOWN_FIELD"

    return r

attribute_template = "        ('%(attname)s', %(replacer)s),"
class_template = """
class %(modelname)sAnonymizer(Anonymizer):

    model = %(modelname)s

    attributes = [
%(attributes)s
    ]
"""

def create_anonymizer(model):
    attributes = []
    fields = model._meta.fields
    # For the faker.name/username/email magic to work as expected and produce
    # consistent sets of names/email addreses, they must be accessed in the same
    # order. This will usually not be a problem, but if duplicate names are
    # produced and the field is unique=True, the logic in DjangoFaker for
    # getting new values from the 'source' means that the order will become out
    # of sync. To avoid this, we put fields with 'unique=True' at the beginning
    # of the list. Usually this will only be the username.
    sort_key = lambda f: not getattr(f, 'unique', False)
    fields.sort(key=sort_key)

    for f in fields:
        replacer = get_replacer_for_field(f)
        attributes.append(attribute_template % {'attname': f.attname,
                                                'replacer': replacer })
    return class_template % {'modelname':model.__name__,
                             'attributes': "\n".join(attributes) }


def create_anonymizers_module(app):
    model_names = []
    imports = []
    output = []
    output.append("")
    imports.append("from anonymizer import Anonymizer")
    for model in get_models(app):
        model_names.append(model.__name__)
        output.append(create_anonymizer(model))

    imports.insert(0, "from %s import %s" % (app.__name__, ", ".join(model_names)))

    return "\n".join(imports) + "\n".join(output)
