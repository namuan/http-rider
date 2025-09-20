from faker import Generator
from faker.providers.address.en_US import Provider as AP
from faker.providers.company.en_US import Provider as CP
from faker.providers.date_time.en_US import Provider as DTProvider
from faker.providers.internet.en_US import Provider as IP
from faker.providers.lorem.en_US import Provider as LoremProvider
from faker.providers.misc.en_US import Provider as MP
from faker.providers.person.en_US import Provider as PP
from faker.providers.python.en_US import Provider as PythonProvider

g = Generator()
g.add_provider(PP)
g.add_provider(MP)
g.add_provider(IP)
g.add_provider(AP)
g.add_provider(CP)
g.add_provider(PythonProvider)
g.add_provider(LoremProvider)
g.add_provider(DTProvider)


class CustomFaker:
    last_name = g.last_name
    first_name = g.first_name

    country = g.country
    building_number = g.building_number
    street_name = g.street_name
    street_address = g.street_address
    address = g.address
    secondary_address = g.secondary_address
    city = g.city
    zipcode = g.postcode
    state = g.state

    prefix_male = g.prefix_male
    first_name_male = g.first_name_male
    last_name_male = g.last_name_male
    name_male = g.name_male
    suffix_male = g.suffix_male

    prefix_female = g.prefix_female
    first_name_female = g.first_name_female
    last_name_female = g.last_name_female
    name_female = g.name_female
    suffix_female = g.suffix_female
    uuid4 = g.uuid4

    def domain_word(self):
        return g.domain_word()


fake = CustomFaker()
