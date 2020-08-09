# backend-task-profil-software

Loading data from persons.json file or using API into the database.

### Scripts 'main.py'

If you want to fill database, use the script:
 1. Open the terminal and then enter the following command:
 2. Go to the directory with the downloaded :iles by typing:
 - If you want to use file 'persons.json':
```
$ python main.py -insert_to_db 'persons.json'
```

- If you want to use API - https://randomuser.me/:
```
$ python main.py -insert_to_db
```

### Scripts 'movies.py'

Use the script:
 1. Open the terminal and then enter the following command:
 2. Go to the directory with the downloaded files by typing:
 
- Getting percentage of women and men
  
  Example input:
  ```
  $ python script.py -get_percent_gender
  ```
  
- Showing average age depending on gender / or not.
 
  Example input:
   ```
  $ python script.py -average_age male
   ```
   
- Showing a most common N cities, N=quantity
 
  Example input:
   ```
  $ python script.py -most_common_cities 5
   ```
   
- Getting a most common N passwords, N=quantity
 
  Exampe input:
  
  ```
  $ python script.py -most_common_passwords 5
  ```
 
- Showing all users who were born in the date range given as a parameter, date format - YYYY-MM-DD
 
  Exampe input:
  
  ```
  $ python script.py -person_range_date_birth '1977-03-12' '1978-02-04'
  ```

- Getting a most secure password
 
  Exampe input:
  
  ```
  $ python script.py -most_secure_password
  ```
  
### UNIT TESTS
```
$ python -m pytest -v
```