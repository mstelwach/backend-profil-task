import pytest
from script import Persons


class TestPersons:
    def setup_class(self):
        self.p = Persons()

    def test_get_percent_gender(self):
        assert self.p.get_percent_gender() == [('Female', 49.8), ('Male', 50.2)]

    def test_average_age(self):
        assert self.p.average_age() == 49.11

    def test_average_age_male(self):
        assert self.p.average_age('male') == 48.71

    def test_average_age_female(self):
        assert self.p.average_age('female') == 49.51

    def test_most_common_cities(self):
        result = [('Gisborne', 7), ('Lower Hutt', 5), ('Napier', 5), ('Queanbeyan', 5), ('Van', 5)]
        assert self.p.most_common_cities(5) == result

    def test_most_common_passwords(self):
        result = [('surf', 3), ('achtung', 3), ('thrasher', 2), ('jethro', 2), ('review', 2)]
        assert self.p.most_common_passwords(5) == result

    def test_person_range_date_birth(self):
        result = ['malene.stenseth@example.com', 'selene.dufour@example.com']
        assert self.p.person_range_date_birth('1977-03-12', '1977-04-04') == result

    def test_most_secure_password(self):
        assert self.p.most_secure_password() == ['films+pic+galeries', 9]
