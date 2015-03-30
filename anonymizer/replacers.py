# Pre-built replacers.

varchar = lambda anon, obj, field, val: anon.faker.varchar(field=field)
varchar.__doc__ = """
Returns random data for a varchar field.
"""

ssn = lambda anon, obj, field, val: anon.faker.simple_pattern('###-###-###-###', field=field)
ssn.__doc__ = """
Returns bothified data for a ssn.
"""

bool = lambda anon, obj, field, val: anon.faker.bool(field=field)
bool.__doc__ = """
Returns a random boolean value (True/False)
"""

integer = lambda anon, obj, field, val: anon.faker.integer(field=field)
integer.__doc__ = """
Returns a random integer (for a Django IntegerField)
"""

positive_integer = lambda anon, obj, field, val: anon.faker.positive_integer(field=field)
positive_integer.__doc__ = """
Returns a random positive integer (for a Django PositiveIntegerField)
"""

small_integer = lambda anon, obj, field, val: anon.faker.small_integer(field=field)
small_integer.__doc__ = """
Returns a random small integer (for a Django SmallIntegerField)
"""

positive_small_integer = lambda anon, obj, field, val: anon.faker.positive_small_integer(field=field)
positive_small_integer.__doc__ = """
Returns a positive small random integer (for a Django PositiveSmallIntegerField)
"""

datetime = lambda anon, obj, field, val: anon.faker.datetime(field=field)
datetime.__doc__ = """
Returns a random datetime
"""

date = lambda anon, obj, field, val: anon.faker.date(field=field)
date.__doc__ = """
Returns a random date
"""

decimal = lambda anon, obj, field, val: anon.faker.decimal(field=field)
decimal.__doc__ = """
Returns a random decimal
"""

postcode = lambda anon, obj, field, val: anon.faker.postcode(field=field)
postcode.__doc__ = """
Generates a random postcode (not necessarily valid, but it will look like one).
"""

country = lambda anon, obj, field, val: anon.faker.country(field=field)
country.__doc__ = """
Returns a randomly selected country
"""

username = lambda anon, obj, field, val: anon.faker.username(field=field)
username.__doc__ = """
Generates a random username
"""

first_name = lambda anon, obj, field, val: anon.faker.first_name(field=field)
first_name.__doc__ = """
Returns a random first name
"""

last_name = lambda anon, obj, field, val: anon.faker.last_name(field=field)
last_name.__doc__ = """
Returns a random second name
"""

name = lambda anon, obj, field, val: anon.faker.name(field=field)
name.__doc__ = """
Generates a random full name (using first name and last name)
"""

email = lambda anon, obj, field, val: anon.faker.email(field=field)
email.__doc__ = """
Generates a random email address.
"""

similar_email = lambda anon, obj, field, val: val if 'betterworks.com' in val else '@'.join([anon.faker.username(field=field), val.split('@')[-1]])
similar_email.__doc__ = """
Generate a random email address using the same domain.
"""

full_address = lambda anon, obj, field, val: anon.faker.address(field=field)
full_address.__doc__ = """
Generates a random full address, using newline characters between the lines.
Resembles a US address
"""
phone_number = lambda anon, obj, field, val: anon.faker.phone_number(field=field)
phone_number.__doc__ = """
Generates a random US-style phone number
"""

street_address = lambda anon, obj, field, val: anon.faker.street_address(field=field)
street_address.__doc__ = """
Generates a random street address - the first line of a full address
"""

city = lambda anon, obj, field, val: anon.faker.city(field=field)
city.__doc__ = """
Generates a random city name. Resembles the name of US/UK city.
"""

state = lambda anon, obj, field, val: anon.faker.state(field=field)
state.__doc__ = """
Returns a randomly selected US state code
"""

zip_code = lambda anon, obj, field, val: anon.faker.zip_code(field=field)
zip_code.__doc__ = """
Returns a randomly generated US zip code (not necessarily valid, but will look like one).
"""

company = lambda anon, obj, field, val: anon.faker.company(field=field)
company.__doc__ = """
Generates a random company name
"""

lorem = lambda anon, obj, field, val: anon.faker.sentence(field=field)
lorem.__doc__ = """
Generates a paragraph of lorem ipsum text
"""

similar_datetime = lambda anon, obj, field, val: anon.faker.datetime(field=field, val=val)
similar_datetime.__doc__ = """
Returns a datetime that is within plus/minus two years of the original datetime
"""

similar_date = lambda anon, obj, field, val: anon.faker.date(field=field, val=val)
similar_date.__doc__ = """
Returns a date that is within plus/minus two years of the original date
"""

similar_lorem = lambda anon, obj, field, val: anon.faker.lorem(field=field, val=val)
similar_lorem.__doc__ = """
Generates lorem ipsum text with the same length and same pattern of linebreaks
as the original. If the original often takes a standard form (e.g. a single word
'yes' or 'no'), this could easily fail to hide the original data.
"""

choice = lambda anon, obj, field, val: anon.faker.choice(field=field)
choice.__doc__ = """
Randomly chooses one of the choices set on the field.
"""
