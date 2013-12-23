CalendarHangout
===============

Python script to process Google Calendar and Add Hangout links to Description.


Prereqs
-------
Before running this, you need to get:
* Python
* The py-applescript python module
* The pyobjc python module (which you may already have)
* The dateutils module
* The GData Python Client v3 - Included
 * Or you can install it globally via `easy_install --upgrade google-api-python-client`
* client_secrets.json file
 * Easiest way to get that is via [this link](https://developers.google.com/api-client-library/python/start/installation)
 * simply select "Calendar API" and "Command Line" platform, and it will walk you through the steps from there.
 * Upon first launch of the application, you will be prompted to authenticate in your browser.
* Also, change the "CalendarID" at the Top of this script to your calendar.
