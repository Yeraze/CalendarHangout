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

Now, that list of prereqs may seem daunting to the Python-uninitiated, but it's not bad.  Just do this:

```bash
easy_install pip
pip install py_applescript
pip install dateutils
pip install --upgrade google-api-python-client

```

If you're a [Homebrew](http://brew.sh) User, then you'll optionally also need to do:
```bash
pip install pyobjc
```
_That one takes a while_.

If any of those complain about permission denied, then just prefix the command with `sudo` and it should work.

First Run
---------
Before  your first run (which you'll need to do manually from the commandline)

1. Create a `~/.hangoutFix` directory
2. Place your shiny new `client_secrets.json` file in it.
3. Change the "CalendarID" at the Top of `hangoutFix.py` to your calendar.
4. Now run it.. It will redirect you to your browser to enable access.
5. Once you've granted access, it should take off and update.

You can safely Ctrl-C it if you don't want it to do the total run right now.  Keep in mind, that you can't
break while it's running the applescript, so you'll have to kill it between updates.

Using launchctl
---------------
This script won't work inside of cron.. Don't ask me, blame apple.

Because of that, if you really want to automate it, you'll need to do so via launchctl.

So, edit the `com.yeraze.hangoutFix.plist` file here to reflect the directory of where
you placed the newly corrected hangoutFix.py script.  Then:

* launchctl load com.yeraze.hangoutFix.plist
* launchctl start com.yeraze.hangoutFix

That should start off the job.  After that one completes, it should start another every 24 hours!

*Note* If you get a strange error like:
```
Could not open job overrides database at: /private/var/db/launchd.db/com.apple.launchd/overrides.plist: 13: Permission denied
launch_msg(): Socket is not connected
```
Then this means you're in tmux, aren't you?  Either exit tmux and try it again, or read up on `reattach-to-user-namespace`.
