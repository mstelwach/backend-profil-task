from main import *


class Persons:

    @staticmethod
    def set_session_database():
        db = create_engine('sqlite:///persons.db')
        session = sessionmaker(bind=db)
        return session()

    @staticmethod
    def sorted_query(qs, quantity):
        return sorted(qs.items(), key=lambda kv: kv[1], reverse=True)[:int(quantity)]

    @staticmethod
    def get_char_points(password):
        char_points = [('[a-z]', 1), ('[A-Z]', 2), ('[0-9]', 1), ("""[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]""", 3)]
        total = 0
        for char, points in char_points:
            if re.compile(char).search(password):
                total += points
        return total

    def get_percent_gender(self):
        """
        Getting percentage of women and men.
        :return: List of percentage.
        """
        session = self.set_session_database()
        female_length = len(session.query(Person).filter_by(gender='female').all())
        male_length = len(session.query(Person).filter_by(gender='male').all())
        person_length = len(session.query(Person).all())
        female_percentage = 100 * float(female_length) / float(person_length)
        male_percentage = 100 * float(male_length) / float(person_length)
        print('Female: {}%, Male: {}%'.format(female_percentage, male_percentage))
        return [('Female', female_percentage), ('Male', male_percentage)]

    def average_age(self, gender=None):
        """
        Showing average age depending on gender / or not.
        :param gender: string format, optional(male, female)
        :return: Average age - float format.
        """
        session = self.set_session_database()
        sum_age = 0

        persons = session.query(Dob).all()
        if gender == 'male':
            persons = session.query(Dob).join(Person).filter_by(gender='male').all()
        if gender == 'female':
            persons = session.query(Dob).join(Person).filter_by(gender='female').all()

        for person in persons:
            sum_age += person.age

        avg = sum_age / len(persons)
        print('The average age is: {}'.format(round(avg, 2)))
        return round(avg, 2)

    def most_common_cities(self, quantity):
        """
        Showing a most common N cities, N=quantity.
        :param quantity: integer format, e.g. -> 5
        :return: List with N tuples in format: (city, number of appearances).
        """
        session = self.set_session_database()
        cities = {}
        locations = session.query(Location).all()
        for location in locations:
            if location.city not in cities:
                cities[location.city] = 1
            else:
                cities[location.city] += 1
        return self.sorted_query(cities, quantity)

    def most_common_passwords(self, quantity):
        """
        Getting a most common N passwords, N=quantity.
        :param quantity: integer format, e.g. -> 5
        :return: List with N tuples in format: (password, number of appearances).
        """
        session = self.set_session_database()
        passwords = {}
        logins = session.query(Login).all()
        for login in logins:
            if login.password not in passwords:
                passwords[login.password] = 1
            else:
                passwords[login.password] += 1
        return self.sorted_query(passwords, quantity)

    def person_range_date_birth(self, start_date, end_date):
        """
        Showing all users who were born in the date range given as a parameter.
        :param start_date: string date format, optional(YYYY-MM-DD)
        :param end_date: string date format, optional(YYYY-MM-DD)
        :return: List with e-mail person.
        """
        session = self.set_session_database()
        persons = session.query(Person).join(Dob).filter(Dob.date >= start_date, Dob.date <= end_date).all()
        return [person.email for person in persons]

    def most_secure_password(self):
        """
        Getting a most secure password.
        :return: List with most secure password and points.
        """
        session = self.set_session_database()
        most_points_password = 0
        most_secure_password = None
        logins = session.query(Login).all()
        for login in logins:
            points_password = 0
            password = login.password
            if len(password) >= 8:
                points_password += 5
            points_password += self.get_char_points(password)
            if points_password >= most_points_password:
                most_points_password = points_password
                most_secure_password = password
        print('Most secure password: {} - {} points.'.format(most_secure_password, most_points_password))
        return [most_secure_password, most_points_password]


if __name__ == '__main__':
    p = Persons()
    method = sys.argv[1].lstrip('-')
    args = sys.argv[2:]
    print(getattr(p, method)(*args))
