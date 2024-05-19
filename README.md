# log_search

Steps to setup the repository:

1. Install python 3.9 and pip.
2. Clone this repository, and make it as the pwd on terminal.
3. We are using dropbox as the remote storage where our folders and files will be store. So, add dropbox access token in file dropbox_connector.py in variable DROPBOX_ACCESS_TOKEN.
4. We are expecting that folders of log will be present under folder `/logs`.
5. Run `pip install pipenv`
6. Run `pipenv install`
7. Run `pipenv shell`
8. Run `pipenv run python main.py`

Curl to search for a keyword in logs for a time period: `curl --location --request GET 'http://127.0.0.1:5000/search/logs?searchKeyword=https&from=2024-05-01&to=2024-05-10'`
