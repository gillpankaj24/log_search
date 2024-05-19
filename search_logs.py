import datetime

from dropbox_connector import dropbox_connect, dropbox_list_files, dropbox_download_file


class SearchLogs:
    """
    Class to search logs
    """
    dbx = dropbox_connect()
    required_keys = ['from', 'searchKeyword', 'to']

    def validate_request_params(self, data: dict = {}):
        """
        Validate request data
        :param data: Request data
        :return: success, response
        """
        # Check if all required keys are present
        if sorted(data.keys()) != self.required_keys:
            return False, {
                'error': f'Request params do not match with required params. Required params: {self.required_keys}'
            }
        # Check if searchKeyword lies between 0 and 500
        if len(data['searchKeyword']) > 500 or len(data['searchKeyword']) < 3:
            return False, {'error': 'Length of search keyword should be between 3 to 500 characters.'}
        try:
            from_date = datetime.datetime.strptime(data['from'], '%Y-%m-%d').date()
            to_date = datetime.datetime.strptime(data['to'], '%Y-%m-%d').date()
        except ValueError:
            return False, {'error': 'Invalid date. Date is expected in format yyyy-mm-dd.'}
        # Check if to_date is greater than from_date
        if from_date > to_date:
            return False, {'error': 'to date should be greater than from date.'}
        # Check if max diff between dates is 30
        if (to_date - from_date).days > 30:
            return False, {'error': 'The max diff between to and from date can be 30.'}
        return True, {'searchKeyword': data['searchKeyword'], 'to': to_date, 'from': from_date}

    @staticmethod
    def fetch_folder_names(start_date, end_date):
        """
        Fetch the required folders to be checked for logs for a time range
        :param start_date: Time to start looking at logs
        :param end_date: Time till we need to see logs
        :return: List of dates
        """
        dates = [str(start_date)]
        for i in range(1, (end_date-start_date).days + 1):
            dates.append(str(start_date + datetime.timedelta(days=i)))
        return dates

    def search_logs(self, data: dict = {}):
        """
        Search logs between a time interval
        :param data:
        :return:
        """
        result = []
        dates_for_logs = self.fetch_folder_names(data['from'], data['to'])
        for date in dates_for_logs:
            try:
                files = [file.name for file in dropbox_list_files(self.dbx, f'/logs/{date}')]
                for file in files:
                    file_data = dropbox_download_file(self.dbx, f'/logs/{date}/{file}')
                    for line in file_data.splitlines():
                        if data['searchKeyword'] in line:
                            result.append(f'{date} {line}')
            except:
                print(f'No logs found for date {date}')
        return {"logs": result}


search_logs_data = SearchLogs()
