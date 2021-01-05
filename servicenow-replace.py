from gi.repository import Gtk

from zim.plugins import PluginClass
from zim.gui.pageview import PageViewExtension

import re
import sys

VERBATIM = 'code'
VERBATIM_BLOCK = 'pre'

class InsertSymbolPlugin(PluginClass):

    plugin_info = {
        'name': _('ServiceNow Replace'), # T: plugin name
        'description': _('''\
Replace matching ServiceNow regex with a link.
'''), # T: plugin description
        'author': 'jorp',
    }

    def __init__(self):
        PluginClass.__init__(self)
        
class InsertSymbolPageViewExtension(PageViewExtension):

    def __init__(self, plugin, pageview):
        PageViewExtension.__init__(self, plugin, pageview)
        self.connectto(pageview.textview, 'end-of-word')
        
    '''Handler for the end-of-word signal from the textview'''
    def on_end_of_word(self, textview, start, end, word, char, editmode):
        # lazy check to save regex performance hit on every word
        if (not word.startswith(('INC', 'CHG', 'RITM', 'SCTASK'))) or len(word) < 10:
            return
        servicenow_items = {
            "INC" : "https://SERVICENOW_DOMAIN/incident.do?sysparm_query=number=",
            "CHG" : "https://SERVICENOW_DOMAIN/change_request.do?sysparm_query=number=",
            "RITM" : "https://SERVICENOW_DOMAIN/sc_req_item.do?sysparm_query=number=",
            "SCTASK" : "https://SERVICENOW_DOMAIN/sc_task.do?sysparm_query=number="
        }
        pattern = re.compile('(INC|RITM|SCTASK|CHG)[0-9]{7}$')
        
        if VERBATIM in editmode \
        or VERBATIM_BLOCK in editmode \
        or not (char.isspace() or char == ';'):
            return

        ticket = word
        if not pattern.match(ticket):
            return
        
        prefix = ''.join(filter(lambda x: not x.isdigit(), ticket))
        url = servicenow_items.get(prefix)
        string = f"[[{url}{ticket}|{ticket}]]"

        buffer = textview.get_buffer()
        mark = buffer.create_mark(None, end, left_gravity=False)

        buffer.delete(start, end)
        iter = buffer.get_iter_at_mark(mark)
        buffer.insert(iter, string)
        buffer.delete_mark(mark)

        # block other handlers
        textview.stop_emission('end-of-word')
