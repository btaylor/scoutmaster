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

from django.template.loader import render_to_string

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

        m = re.match('%s: quote( (?P<user>\w+))?$' % settings.CAMPFIRE_BOT_NAME, body)
        if m:
            user = m.group('user')
            quote = Quote.objects.get_random_quote(user=user)
            if quote:
                room.speak(render_to_string('quotes/quote.txt', {'quote': quote}))
            else:
                room.speak(render_to_string('quotes/no_quotes.txt'))

        m = re.match('%s: quote (?P<user>\w+) "?(?P<quote>.*)"?$' % settings.CAMPFIRE_BOT_NAME,
                     body)
        if m:
            Quote.objects.create(user=m.group('user'),
                                 quote=m.group('quote'))
