from faker import Faker
from faker.providers import internet, person, misc, address

fake = Faker()
fake.add_provider(internet)
fake.add_provider(person)
fake.add_provider(misc)
fake.add_provider(address)
