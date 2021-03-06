import requests

requestHeaders = {
        #'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        #'Content-type': 'multipart/form-data',
}

class Authentication:
    def __init__(self, ip_address, port, username, password):
        self._ip_address = ip_address
        self._port = port
        self._username = username
        self._password = password
        self._sid = None
        self._session_expire = True
        self._base_url = 'http://%s:%s/webapi/' % (self._ip_address, self._port)

        self.full_api_list = {}
        self.app_api_list = {}

    def login(self, application):
        login_api = 'auth.cgi?api=SYNO.API.Auth'
        param = {'version': '2', 'method': 'login', 'account': self._username,
                 'passwd': self._password, 'session': application, 'format': 'sid'}

        if not self._session_expire and self._sid is not None:
            self._session_expire = False
            return 'User already logged'
        else:
            session_request = requests.get(self._base_url + login_api, param)
            self._sid = session_request.json()['data']['sid']
            self._session_expire = False
            return 'User logging... New session started!'

    def logout(self, application):
        logout_api = 'auth.cgi?api=SYNO.API.Auth'
        param = {'version': '2', 'method': 'logout', 'session': application}

        response = requests.get(self._base_url + logout_api, param)
        if response.json()['success'] is True:
            self._session_expire = True
            self._sid = None
            return 'Logged out'
        else:
            self._session_expire = True
            self._sid = None
            return 'No valid session is open'

    def get_api_list(self, app=None):
        query_path = 'query.cgi?api=SYNO.API.Info'
        list_query = {'version': '1', 'method': 'query', 'query': 'all'}

        response = requests.get(self._base_url + query_path, list_query).json()

        if app is not None:
            for key in response['data']:
                if app.lower() in key.lower():
                    self.app_api_list[key] = response['data'][key]
        else:
            self.full_api_list = response['data']

        return

    def show_api_name_list(self):
        prev_key = ''
        for key in self.full_api_list:
            if key != prev_key:
                print(key)
                prev_key = key
        return

    def show_json_response_type(self):
        for key in self.full_api_list:
            for sub_key in self.full_api_list[key]:
                if sub_key == 'requestFormat':
                    if self.full_api_list[key]['requestFormat'] == 'JSON':
                        print(key + '   Returns JSON data')
        return

    def search_by_app(self, app):
        print_check = 0
        for key in self.full_api_list:
            if app.lower() in key.lower():
                print(key)
                print_check += 1
                continue
        if print_check == 0:
            print('Not Found')
        return

    def request_data(self, api_name, api_path, req_param, method=None, response_json=True):  # 'post' or 'get'

        # Convert all booleen in string in lowercase because Synology API is waiting for "true" or "false"
        for k,v in req_param.items():
            if isinstance(v, bool):
                req_param[k] = str(v).lower()

        req_param['_sid'] = self._sid
        req_param['api'] = api_name

        url = ('%s%s' % (self._base_url, api_path))
        # checking and handling HTTP-Method (perform a request)
        if method is None or method.lower() == 'get':
            response = requests.get(url, headers=requestHeaders, params = req_param)
        elif method.lower() == 'post':
            response = requests.post(url, headers=requestHeaders, data = req_param)
        else: #raise error method not found
            raise ValueError("method value:'{}' is not valid".format(method))
        
        if response_json is True:
            return response.json()
        else:
            return response

    @property
    def sid(self):
        return self._sid

    @property
    def base_url(self):
        return self._base_url
