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

import scoutmaster

from pinder import streaming
from pinder.campfire import Campfire

from scoutmaster import settings
from scoutmaster.core.plugin import ListenerPlugin
from scoutmaster.quotes.plugin import QuotePlugin

class Bot:
    def __init__(self):
        self.client = Campfire(settings.CAMPFIRE_SUBDOMAIN,
                               settings.CAMPFIRE_API_KEY, ssl=True)
        self.rooms = []
        for r in settings.CAMPFIRE_ROOMS:
            print r
            room = self.client.find_room_by_name(r)
            if room:
                self.rooms.append(room)
            room.join()

        self.plugins = []
        for p in settings.INSTALLED_PLUGINS:
            klass = scoutmaster
            parts = p.split('.')
            for i in parts:
                klass = getattr(klass, i)
            if klass:
                self.plugins.append(klass())

    def listen(self):
        def callback(message):
            room = self.client.room(message['room_id'])
            for p in self.plugins:
                if isinstance(p, ListenerPlugin):
                    p.recieve_message(self.client, room, message)

        def errback(message):
            print message

        for r in self.rooms:
            r.listen(callback, errback)
