#
# Copyright (c) 2011 Brad Taylor <brad@getcoded.net>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import re

from datetime import datetime

from scoutmaster import settings
from scoutmaster.quotes.models import Quote
from scoutmaster.core.plugin import ListenerPlugin

class QuotePlugin(ListenerPlugin):
    def __init__(self):
        pass

    def recieve_message(self, campfire, room, message):
        body = message['body']
        if not body:
            return

        # I'll only respond to messages directed at me
        if not body.startswith(settings.CAMPFIRE_BOT_NAME):
            return

        m = re.match('%s: quote$' % settings.CAMPFIRE_BOT_NAME, body)
        if m:
            self.speak_random_quote(campfire, room)

        m = re.match('%s: quote (?P<user>\w+) "?(?P<quote>.*)"?$' % settings.CAMPFIRE_BOT_NAME,
                     body)
        if m:
            # TODO: replace datetime.now() with overridden save inside of Quote
            Quote.objects.create(user=m.group('user'),
                                 quote=m.group('quote'),
                                 date=datetime.now())

    # TODO: This should go into Quote's manager
    def speak_random_quote(self, campfire, room, user=None):
        quotes = Quote.objects.order_by('?')
        if quotes.count() == 0:
            room.speak('Outta quotes!  Say something funny!')
            return

        room.speak(unicode(quotes[0]))
