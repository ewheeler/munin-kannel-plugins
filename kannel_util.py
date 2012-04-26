import urllib2
from xml.etree.ElementTree import XML
import os

def get_status(url = os.environ['STATUS_URL']):
    response = urllib2.urlopen(url)
    try:
        xml = XML(response.read())
    finally:
        response.close()

    result = {}

    el = xml.find('sms')
    result_d = result['sms'] = {}
    result_d['received'] = {'total': int(el.findtext('received/total')),
     'queued': int(el.findtext('received/queued'))}
    result_d['sent'] = {'total': int(el.findtext('sent/total')),
     'queued': int(el.findtext('sent/queued'))}
    result_d['storesize'] = int(el.findtext('storesize'))

    el = xml.find('dlr')
    result_d = result['dlr'] = {}
    result_d['received'] = {'total': int(el.findtext('received/total'))}
    result_d['sent'] = {'total': int(el.findtext('sent/total'))}

    result_d['queued'] = int(el.findtext('queued'))

    els = xml.find('smscs').findall('smsc')
    result_d = result['smscs'] = []
    for el in els:
        result_d.append({
            'id': el.findtext('id'),
            'admin_id': el.findtext('admin-id'),
            'received': {
                'sms': int(el.findtext('sms/received')),
                'dlr': int(el.findtext('dlr/received'))
            },
            'sent': {
                'sms': int(el.findtext('sms/sent')),
                'dlr': int(el.findtext('dlr/sent'))
            },
            'failed' : int(el.findtext('failed')),
            'queued' : int(el.findtext('queued')),
            'status' : el.findtext('status').split(' ', 2)[0]
        })

    return result