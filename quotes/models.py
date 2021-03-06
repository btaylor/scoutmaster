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

from datetime import datetime

from django.db import models

from scoutmaster.quotes.managers import QuoteManager

class Quote(models.Model):
    date = models.DateTimeField(editable=False)
    user = models.CharField(max_length=128)
    quote = models.TextField()
    objects = QuoteManager()

    def __unicode__(self):
        return '"%s" -- %s' % (self.quote, self.user)

    def save(self, *args, **kwargs):
        if not self.id and not self.date:
            self.date = datetime.now()
        super(Quote, self).save(*args, **kwargs)
