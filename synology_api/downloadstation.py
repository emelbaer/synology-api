from . import auth as syn


class DownloadStation:

    def __init__(self, ip_address, port, username, password):

        self.session = syn.Authentication(ip_address, port, username, password)
        self._bt_search_id = ''
        self._bt_search_id_list = []
        self.session.login('DownloadStation')
        self.session.get_api_list('DownloadStation')

        self.request_data = self.session.request_data
        self.download_list = self.session.app_api_list
        self._sid = self.session.sid
        self.base_url = self.session.base_url

        print('You are now logged in!')

    def logout(self):
        self.session.logout('DownloadStation')

    def get_info(self):
        api_name = 'SYNO.DownloadStation.Info'
        info = self.download_list[api_name]
        api_path = info['path']
        req_param = {'version': info['maxVersion'], 'method': 'getinfo'}

        return self.request_data(api_name, api_path, req_param)

    def get_config(self):
        api_name = 'SYNO.DownloadStation.Info'
        info = self.download_list[api_name]
        api_path = info['path']
        req_param = {'version': info['maxVersion'], 'method': 'getconfig'}

        return self.request_data(api_name, api_path, req_param)

    def set_server_config(self, bt_max_download=None, bt_max_upload=None, emule_max_download=None,
                          emule_max_upload=None, nzb_max_download=None, http_max_download=None, ftp_max_download=None,
                          emule_enabled=None, unzip_service_enabled=None, default_destination=None,
                          emule_default_destination=None):

        api_name = 'SYNO.DownloadStation.Info'
        info = self.download_list[api_name]
        api_path = info['path']
        req_param = {'version': info['maxVersion'], 'method': 'setserverconfig'}

        for key, val in locals().items():
            if key not in ['self', 'api_name', 'info', 'api_path', 'req_param']:
                if val is not None:
                    req_param[str(key)] = val

        return self.request_data(api_name, api_path, req_param)

    def schedule_info(self):
        api_name = 'SYNO.DownloadStation.Schedule'
        info = self.download_list[api_name]
        api_path = info['path']
        req_param = {'version': info['maxVersion'], 'method': 'getconfig'}

        return self.request_data(api_name, api_path, req_param)

    def schedule_set_config(self, enabled=False, emule_enabled=False):
        api_name = 'SYNO.DownloadStation.Schedule'
        info = self.download_list[api_name]
        api_path = info['path']
        req_param = {'version': info['maxVersion'], 'method': 'setconfig', 'enabled': str(enabled).lower(),
                     'emule_enabled': str(emule_enabled).lower()}

        if type(enabled) is not bool or type(emule_enabled) is not bool:
            return 'Please set enabled to True or False'

        return self.request_data(api_name, api_path, req_param)

    def tasks_list(self, additional_param=None):
        """
offset  Optional. Beginning task on the requested record. Default to “0”.
limit   Optional. Number of records requested: “-1” means to list all tasks. Default to “-1”.
additional  Optional. Additional requested info, as string-list. When an additional option is requested, objects will be provided in the specified additional option.
    Possible additional options include:
     detail: returns Task_Detail object
     transfer: returns Task_Transfer object
     file: returns Task_File object (BT only)
     tracker: returns Task_Tracker object (BT only)
     peer: returns Task_Peer object (BT only)
        """
        api_name = 'SYNO.DownloadStation.Task'
        info = self.download_list[api_name]
        api_path = info['path']
        req_param = {'version': info['maxVersion'], 'method': 'list', 'additional': additional_param}

        if additional_param is None:
            additional_param = ['detail', 'transfer', 'file', 'tracker', 'peer']

        if type(additional_param) is list:
            req_param['additional'] = ",".join(additional_param)

        return self.request_data(api_name, api_path, req_param)

    def task_create(self, uri, unzip_password=None, destination=None):
        """
uri             Optional. Accepts HTTP/FTP/magnet/ED2K links or the file path starting with a shared folder, multiple enter as list.
file            Optional. File uploading from client. For more info, please see Limitations:
                    Due to multipart upload limitations, creating tasks by uploading files should adhere to one of the following implementations:
                        a Set the upload files as the only POST request method data, and set other files as GET parameters.
                        b Set all the parameters as POST data, and the upload file should implement LAST parameters.
username        Optional. Login username (FTP,...)
password        Optional. Login password (FTP,...)
unzip_password  Optional. Password for unzipping download tasks
destination     Optional. Download destination path (!!) starting with a shared folder
        """
        api_name = 'SYNO.DownloadStation.Task'
        info = self.download_list[api_name]
        api_path = info['path']
        param = {'version': info['maxVersion'], 'method': 'create', 'uri': uri}

        if isinstance(uri, list):
            param['uri'] = ",".join(uri)
        if unzip_password is not None:
            param['unzip_password'] = unzip_password
        if destination is not None:
            param['destination'] = destination
        
        return self.request_data(api_name, api_path, param, method="post")

    def tasks_info(self, task_id, additional_param=None):
        api_name = 'SYNO.DownloadStation.Task'
        info = self.download_list[api_name]
        api_path = info['path']
        req_param = {'version': info['maxVersion'], 'method': 'getinfo', 'id': task_id, 'additional': additional_param}

        if additional_param is None:
            additional_param = ['detail', 'transfer', 'file', 'tracker', 'peer']

        if type(additional_param) is list:
            req_param['additional'] = ",".join(additional_param)

        if type(task_id) is list:
            req_param['id'] = ",".join(task_id)

        return self.request_data(api_name, api_path, req_param)

    def task_delete(self, task_id, force=False):
        """
Parameter   Description
id          Task IDs to be deleted, multiple enter as list.
force       Delete tasks and force to move uncompleted download files to the destination.
        """
        api_name = 'SYNO.DownloadStation.Task'
        info = self.download_list[api_name]
        api_path = info['path']
        param = {'version': info['maxVersion'], 'method': 'delete', 'id': task_id,
                 'force_complete': str(force).lower()}

        if type(task_id) is list:
            param['id'] = ",".join(task_id)

        return self.request_data(api_name, api_path, param)

    def task_pause(self, task_id):
        api_name = 'SYNO.DownloadStation.Task'
        info = self.download_list[api_name]
        api_path = info['path']
        param = {'version': info['maxVersion'], 'method': 'pause', 'id': task_id}

        if type(task_id) is list:
            param['id'] = ",".join(task_id)

        return self.request_data(api_name, api_path, param)

    def task_resume(self, task_id):
        api_name = 'SYNO.DownloadStation.Task'
        info = self.download_list[api_name]
        api_path = info['path']
        param = {'version': info['maxVersion'], 'method': 'resume', 'id': task_id}

        if type(task_id) is list:
            param['id'] = ",".join(task_id)

        return self.request_data(api_name, api_path, param)

    def task_edit(self, task_id, destination='sharedfolder'):
        api_name = 'SYNO.DownloadStation.Task'
        info = self.download_list[api_name]
        api_path = info['path']
        param = {'version': info['maxVersion'], 'method': 'edit', 'id': task_id, 'destination': destination}

        if type(task_id) is list:
            param['id'] = ",".join(task_id)

        return self.request_data(api_name, api_path, param)

    def statistic_get_info(self):
        api_name = 'SYNO.DownloadStation.Statistic'
        info = self.download_list[api_name]
        api_path = info['path']
        param = {'version': info['maxVersion'], 'method': 'getinfo'}

        return self.request_data(api_name, api_path, param)

    def rss_site_get_info_list(self, offset=None, limit=None):
        api_name = 'SYNO.DownloadStation.RSS.Site'
        info = self.download_list[api_name]
        api_path = info['path']
        param = {'version': info['maxVersion'], 'method': 'list'}

        if offset is not None:
            param['offset'] = offset
        if limit is not None:
            param['limit'] = limit

        return self.request_data(api_name, api_path, param)

    def rss_site_refresh(self, rss_id=None):
        api_name = 'SYNO.DownloadStation.RSS.Site'
        info = self.download_list[api_name]
        api_path = info['path']
        param = {'version': info['maxVersion'], 'method': 'refresh', 'id': rss_id}

        if rss_id is None:
            return 'Enter a valid ID check if you have any with get_rss_list()'
        elif type(rss_id) is list:
            rss_id = ','.join(rss_id)
            param['id'] = rss_id

        return self.request_data(api_name, api_path, param)

    def rss_feed_list(self, rss_id=None, offset=None, limit=None):
        api_name = 'SYNO.DownloadStation.RSS.Feed'
        info = self.download_list[api_name]
        api_path = info['path']
        param = {'version': info['maxVersion'], 'method': 'list', 'id': rss_id}

        if rss_id is None:
            return 'Enter a valid ID check if you have any with get_rss_list()'
        elif type(rss_id) is list:
            rss_id = ','.join(rss_id)
            param['id'] = rss_id

        if offset is not None:
            param['offset'] = offset
        if limit is not None:
            param['limit'] = limit

        return self.request_data(api_name, api_path, param)

    def bt_search_start(self, keyword=None, module='all'):
        api_name = 'SYNO.DownloadStation.BTSearch'
        info = self.download_list[api_name]
        api_path = info['path']
        param = {'version': info['maxVersion'], 'method': 'start'}

        if keyword is None:
            return 'Did you enter a keyword to search?'
        else:
            param['keyword'] = keyword

        param['module'] = module

        self._bt_search_id = self.request_data(api_name, api_path, param)['data']['taskid']

        self._bt_search_id_list.append(self._bt_search_id)

        return 'You can now check the status of request with get_bt_search_results(), your id is: ' + self._bt_search_id

    def bt_search_get_results(self, taskid=None, offset=None, limit=None, sort_by=None, sort_direction=None,
                              filter_category=None, filter_title=None):
        api_name = 'SYNO.DownloadStation.BTSearch'
        info = self.download_list[api_name]
        api_path = info['path']
        param = {'version': info['maxVersion'], 'method': 'list', 'taskid': taskid}

        for key, val in locals().items():
            if key not in ['self', 'api_name', 'info', 'api_path', 'param', 'taskid']:
                if val is not None:
                    param[str(key)] = val

        if taskid is None:
            return 'Enter a valid taskid, you can choose one of ' + str(self._bt_search_id_list)
        elif type(taskid) is list:
            param['taskid'] = ','.join(taskid)

        return self.request_data(api_name, api_path, param)

    def bt_search_get_category(self):
        api_name = 'SYNO.DownloadStation.BTSearch'
        info = self.download_list[api_name]
        api_path = info['path']
        param = {'version': info['maxVersion'], 'method': 'get'}

        return self.request_data(api_name, api_path, param)

    def bt_search_clean(self, taskid=None):
        api_name = 'SYNO.DownloadStation.BTSearch'
        info = self.download_list[api_name]
        api_path = info['path']
        param = {'version': info['maxVersion'], 'method': 'clean', 'taskid': taskid}

        if taskid is None:
            return 'Enter a valid taskid, you can choose one of ' + str(self._bt_search_id_list)
        elif type(taskid) is list:
            param['taskid'] = ','.join(taskid)
            for item in taskid:
                self._bt_search_id_list.remove(item)
        else:
            self._bt_search_id_list.remove(taskid)

        return self.request_data(api_name, api_path, param)

    def bt_search_get_module(self):
        api_name = 'SYNO.DownloadStation.BTSearch'
        info = self.download_list[api_name]
        api_path = info['path']
        param = {'version': info['maxVersion'], 'method': 'getModule'}

        return self.request_data(api_name, api_path, param)

