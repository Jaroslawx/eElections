# eElection System
## Description
This project aims to create an electronic voting (e-voting) system capable of conducting various types of elections, such as presidential, parliamentary, local council, and university dean elections, among others. The system manages candidate lists, voter eligibility, voting criteria (e.g., number of candidates that can be supported, voting period), and ensures the secrecy of votes at all levels, including within the database.

After voting, the system generates a report containing detailed information on the candidates' support results and voter turnout, as well as a graphical presentation of the results

## Technologies Used
- Python 3.11
- Django 5.0.6
- Chart.js

## Features
- Candidate Management: Allows the creation, deletion, and modification of candidate profiles for each election.
- Voter Management: Manages the list of eligible voters for each election, ensuring only authorized individuals can participate.
- Voting Mechanism: Implements a secure voting process adhering to election rules (e.g., number of votes per voter, voting period duration).
- Result Reporting: Generates comprehensive reports on candidate support and voter turnout post-election, ensuring transparency and accountability.

## Installation
1. Clone the repository:
```shell
git clone https://github.com/Jaroslawx/eElections
```
2. Navigate into the project directory:
```shell
cd eElection
```
3. Install dependencies:
```shell
pip install -r requirements.txt
```
4. Apply database migrations:
```shell
python manage.py migrate
```
5. Start the Django development server:
```shell
python manage.py runserver
```
6. Access the application at http://localhost:8000 in your web browser.

## Usage
1. Admin Interface:
- Access the Django admin panel at http://localhost:8000/admin.
- Use Django's authentication system to log in as a superuser.
- Manage candidates, voters, and election configurations.
2. Voter Experience:
- Voters access the voting interface during the specified voting period.
- Vote securely without revealing individual choices.
3. Result Viewing:
- Post-election, view comprehensive reports detailing candidate support and voter turnout, also in graphical form.

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/Jaroslawx/eElections/blob/master/LICENSE) file for details.
