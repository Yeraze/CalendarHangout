# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command-line skeleton application for Calendar API.
Usage:
  $ python sample.py

You can also get help on all the command-line flags the program understands
by running:

  $ python sample.py --help

"""

import argparse
import httplib2
import os
import sys
import datetime
import tempfile
import applescript
import time

from dateutil.parser import *
from dateutil.tz import *

from apiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools

CalendarID = "FILL IN HERE"

# Parser for command-line arguments.
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[tools.argparser])


# CLIENT_SECRETS is name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret. You can see the Client ID
# and Client secret on the APIs page in the Cloud Console:
# <https://cloud.google.com/console#/project/157180257281/apiui>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# Set up a Flow object to be used for authentication.
# Add one or more of the following scopes. PLEASE ONLY ADD THE SCOPES YOU
# NEED. For more information on using scopes please see
# <https://developers.google.com/+/best-practices>.
FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
                                      scope=[
                                      'https://www.googleapis.com/auth/calendar',
                                      'https://www.googleapis.com/auth/calendar.readonly',
                                      ],
                                      message=tools.message_if_missing(CLIENT_SECRETS))


def main(argv):
    # Parse the command-line flags.
    flags = parser.parse_args(argv[1:])

    # If the credentials don't exist or are invalid run through the native client
    # flow. The Storage object will ensure that if successful the good
    # credentials will get written back to the file.
    storage = file.Storage('sample.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(FLOW, storage, flags)

    # Create an httplib2.Http object to handle our HTTP requests and authorize it
    # with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)

    # Construct the service object for the interacting with the Calendar API.
    service = discovery.build('calendar', 'v3', http=http)



    try:
        today = "%sZ" % (datetime.datetime.utcnow().isoformat())
        enddate = "%sZ" % (datetime.datetime.utcnow() +
                   datetime.timedelta(days=14)).isoformat()
        print("Retrieving events from %s to %s" % (today, enddate))
        events = service.events().list(calendarId=CalendarID, 
                orderBy = "startTime",
                timeMin = today, timeMax = enddate,
                showHiddenInvitations= True,
                singleEvents = True).execute()
        print("Found %i events" % (len(events['items'])))
 
        processedUIDs = []
        print('launching calendar...')
        calScript = applescript.AppleScript(r'''
                        on run
                            tell application "Calendar"
                                activate
                                repeat until application "Calendar" is running
                                    delay 1
                                end repeat
                            end tell
                        end run
                        ''')
        calScript.run();

        for event in events['items']:
            if event.has_key('hangoutLink'):
                if (event['start'].has_key("dateTime")):
                    startTime = parse(event['start']['dateTime'])
                else:
                    startTime = parse(event['start']['date'])
                # sDate = startTime.strftime("%A, %B %d, %Y %I:%M:%S %p")
                uid = event['iCalUID'];
                sDate = startTime.strftime("%A, %B %d, %Y  %I:%M:%S %p")
                print( "-> %s (%s) " % (event['summary'], sDate))
                if (event['iCalUID'] not in processedUIDs):
                    sDate = startTime.strftime("%B %d %Y")
                    processedUIDs.append(uid)
                    aScript = applescript.AppleScript(r'''
                        on run 
                            tell application "Calendar"
                                set thecount to 0
                                repeat with myCal in calendars
                                    set theEvents to (events of myCal whose uid = "%s")
                                    set thecount to (thecount + (count of theEvents))
                                    repeat with theEvent in theEvents
                                        set (url of theEvent) to "%s"
                                    end repeat
                                end repeat
                                return thecount as text
                            end tell
                        end run''' % (uid, event['hangoutLink']))
                    tstart = time.time()
                    processed = aScript.run()
                    tend = time.time()
                    print("  Processed %s items in %i seconds" % (processed, tend-tstart))
                else:
                    print("  Skipping, already captured")


    except client.AccessTokenRefreshError:
        print ("The credentials have been revoked or expired, please re-run"
               "the application to re-authorize")


# For more information on the Calendar API you can visit:
#
#   https://developers.google.com/google-apps/calendar/firstapp
#
# For more information on the Calendar API Python library surface you
# can visit:
#
#   https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/
#
# For information on the Python Client Library visit:
#
#   https://developers.google.com/api-client-library/python/start/get_started
if __name__ == '__main__':
    main(sys.argv)
