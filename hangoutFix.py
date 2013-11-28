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
import re

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
        for i, an_event in zip(xrange(len(feed.entry)), feed.entry):
            VC = "";
            print '\t%s. %s' % (i, an_event.title.text,)
            for fc in an_event.extension_elements:
                if (("%s" % fc).find("ns0:videoConference") > 0):
                    VC = findUrl.search("%s" % fc);
                    print '\t\tVideoConference: %s' % (VC.group(0)).split()[1]
                
            for a_when in an_event.when:
                print '\t\tStart time: %s' % (a_when.start,)
                print '\t\tEnd time:   %s' % (a_when.end,)

    def Run(self):

        self._DateRangeQuery()


def main():
    user = raw_input("Username:")
    pw = raw_input("Password:")

    sample = HangoutFix(user, pw)
    sample.Run()

if __name__ == '__main__':
    main()
