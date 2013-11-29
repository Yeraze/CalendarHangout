#!/usr/bin/python
#
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__author__ = 'randall.hand@gmail.com (Randall Hand)'


try:
    from xml.etree import ElementTree
except ImportError:
    from elementtree import ElementTree
import gdata.calendar.data
import gdata.calendar.client
import gdata.acl.data
import atom
import getopt
import sys
import string
import time
import datetime
import re
import ConfigParser
import os

class HangoutFix:

    def __init__(self, email, password):

        self.cal_client = gdata.calendar.client.CalendarClient(
            source='Google-Calendar_Python_Sample-1.0')
        self.cal_client.ClientLogin(email, password, self.cal_client.source)

    def _DateRangeQuery(self, start_date='2013-11-24', end_date='2013-11-30'):
        findUrl = re.compile(r"link href=\"(\S+)\"")
        print 'Date range query for events on Primary Calendar: %s to %s' % (
            start_date, end_date,)
        query = gdata.calendar.client.CalendarEventQuery(
            start_min=start_date, start_max=end_date)
        feed = self.cal_client.GetCalendarEventFeed(q=query)

        batchJob = gdata.calendar.data.CalendarEventFeed()
        batchSize = 0

        for i, an_event in zip(xrange(len(feed.entry)), feed.entry):
            VC = "";
            print '\t%s. %s' % (i, an_event.title.text,)
            for fc in an_event.extension_elements:
                if (("%s" % fc).find("ns0:videoConference") > 0):
                    VC = findUrl.search("%s" % fc);
                    VC = VC.group(0).split()[1]
                    url = VC.split('\"')[1]
                    if((an_event.content.text) and ((an_event.content.text).find(url) > 0)):
                        print '\t\t Already updated'
                    else:
                        print '\t\t Adding url %s' % url

                        print '\t\t Updating content...'
                        an_event.content.text = "%s<p />-- %s" % (an_event.content.text,url)
                           # Create a WebContent object
                        
                        web_content = gdata.calendar.data.WebContent(url=url)

                        # Create a WebContentLink object that contains the WebContent object
                        title = 'Google Hangout'
                        href = url
                        type = 'text/html'
                        web_content_link = gdata.calendar.data.WebContentLink(title=title, href=href,
                            link_type=type, web_content=web_content)

                        # Create an event that contains this web content
                        an_event.link.append(web_content_link) 

                        an_event.batch_id = gdata.data.BatchId(text='update-request')
                        batchJob.AddUpdate(entry=an_event)
                        batchSize = batchSize +1
                else :
                    print '\t\t No hangout found...'
        if(batchSize > 0):
            print "Sending batch update request ( %i updates )..." % batchSize
            response_feed = self.cal_client.ExecuteBatch(batchJob,
                gdata.calendar.client.DEFAULT_BATCH_URL)

          # iterate the response feed to get the operation status
            for entry in response_feed.entry:
                if (entry.batch_status.code != 200):
                    print "Error on update: %s - %s" % (entry.batch_status.code, entry.batch_status.reason)



    def Run(self):
        today = datetime.date.today().isoformat()
        enddate = (datetime.date.today() + datetime.timedelta(days=7)).isoformat();
        self._DateRangeQuery(start_date = today, end_date = enddate)


def main():
    config = ConfigParser.RawConfigParser()
    cfgFile = os.path.expanduser('~/.hangoutfix')
    config.read(cfgFile)
    try:
        user = config.get('hangoutfix', 'user')
        pw = config.get('hangoutfix', 'pw')
    except:
        print 'Seems you haven\'t created the %s file yet.' % cfgFile
        print ' I will create you a template. Please fill it in.'
        config = ConfigParser.RawConfigParser()

        config.add_section('hangoutfix')
        config.set('hangoutfix', 'user', 'GMAIL_HERE')
        config.set('hangoutfix', 'pw', 'PASSWORD_HERE')

        # Writing our configuration file to 'example.cfg'
        with open(cfgFile, 'wb') as configfile:
            config.write(configfile)
    else:

        sample = HangoutFix(user, pw)
        sample.Run()

if __name__ == '__main__':
    main()
