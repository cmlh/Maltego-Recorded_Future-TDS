import json, urllib, urllib2

class APIUtil:
    _url = 'https://api.recordedfuture.com/query/?'
    _headers = {"Accept-encoding": "gzip"}
    _token = ""

    def _local_error(self, q, e):
        return "Exception occurred during query:\nquery was '{0}'\nException: {1}".format(q, e)
    def _remote_error(self, q, res):
        return "Server failure:\nQuery was '{0}'\nHTTP Status: {1}\tMessage: {2}".format(q, res.get('code','NONE'), res.get('error', 'NONE'))

    def __init__(self):
        pass

    def query(self, q):
        """Perform a standard query."""
        q["token"] = self._token
        url_q = urllib.urlencode({"q":json.dumps(q)})

        try:
            data = urllib2.urlopen(urllib2.Request(self._url+url_q, None)).read()
        except Exception as e:
            raise Exception(self._local_error(q, e))

        res = json.loads(data)
        if res.get('status', '') == 'FAILURE':
            raise Exception(self._remote_error(q, res))
        return res

    def paged_query(self, q, field=None, unique=False):
        """
        Generator for paged query results.
        :field supports dot-notation for getting specific fields. Example 'instances.document.id'
        :unique requires that the items are hashable (i.e. you need field).
        """
        seen = set()
        while True:
            res = self.query(q)
            for item in self._dot_index(field, res):
                if unique:
                    if item in seen:
                        continue
                    seen.add(item)
                yield item

            if 'next_page_start' not in res:
                break
            if 'instance' in q:
                q['instance']['page_start'] = res['next_page_start']
            elif 'entity' in q:
                # Cheat for broken entity paging.
                if len(res.get('entities', [])) == 0:
                        break

                q['entity']['page_start'] = res['next_page_start']
            else:
                raise Exception("Unable to page query. Unknown query type.")

    def _dot_index(self, index, data):
        d = data
        if index:
            for i in index.split('.'):
                d = map(lambda x : x[i], d) if type(d) == type([]) else d[i]
        return d if type(d) == type([]) else [d]

