import requests


class ApiClient:
    """EDSCC class for API calls"""

    def __init__(self, **options):
        self.data = []
        self.squadron = []
        self.valid_verb = []
        self.api_key = options.pop('api_key')
        self.url = options.pop('api_url')
        self.session = requests.Session()
        self.session.proxies = {'https': 'https://localhost:8888'}

    def auth(self):
        reply = self.post('auth')
        if reply['status_code'] == 200:
            self.squadron = reply;
            self.valid_verb = reply['valid_verb']
            return True

    def post(self, verb, **options):
        print('Connecting EDSCC API Server')
        print(f"Command: {verb} Options: {options}")
        uri = '{0}/api/{1}'.format(self.url, verb) if verb != "auth" else '{0}/{1}'.format(self.url, verb)

        if 'params' in options:
            params = []
            for key in options:
                if key == 'params':
                    params.append(options[key])
            options.pop('params')
            options.update({'params[]': params})

        options.update({'fromSoftware': 'EDSCC Discord Bot'})

        header = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        r = self.session.post(uri, data=options, timeout=2, headers=header, verify=False)

        if r.status_code == 200:
            reply = r.json()
            return reply
        else:
            reply = r.json()
            print(f"Status Code: {reply['status_code']}  Message: {reply['message']}")
            raise Exception('Server Error: {0}'.format(r.status_code))
