# Mini-app for test task

To start the project, run the `docker-compose up` command in the root folder of the project.

### Project description
When you start the project, the currencies available via API are automatically loaded. All currencies have default value False on activity and monitoring.\
When you add a currency to the list of active currencies, the rates for that currency start to be collected into the database. When you add it to the list of currencies for monitoring, the currency will be displayed by endpoints and in csv locally.\
The exchange rate is downloaded and updated every 5 minutes — `crontab(minute='*/5')`.

### List of endpoints
1. http://127.0.0.1:8000/api/last_rates/ — get a list of currencies with the current exchange rate ;
2. http://127.0.0.1:8000/api/get_currency_list_to_add/ — get a list of currencies that can be added for tracking ;
3. http://127.0.0.1:8000/api/add-currency-to-active/ — add a new currency to track ;
4. http://127.0.0.1:8000/api/currency-rate-at-time/ — get exchange rate history for a specific currency for a specific period of time ;
5. http://127.0.0.1:8000/api/switch-monitoring-currency/ — switching on/off a currency from monitoring ;
6. http://127.0.0.1:8000/swagger/ — swagger schema .

### Management command
`python manage.py export_to_csv` — create locally a csv file with a list of currencies and current exchange rate.

Thank you for the test assignment.