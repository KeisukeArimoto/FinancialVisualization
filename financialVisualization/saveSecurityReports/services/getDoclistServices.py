# 有価証券報告書のデータ取得に関わるロジックを記載
# viewからデータをもらって、加工して、modelsに渡すまでを担当 (クライアントやDBには依存しない)

import time
import json
import requests
from tqdm import tqdm
from datetime import timedelta

import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


class catcher():
    def __init__(self, since, until, wait_time=2):
        self.csv_tag = ['id', 'title', 'url', 'code', 'update']
        self.encode_type = 'utf-8'
        self.wait_time = wait_time
        self.base_url = 'https://disclosure.edinet-fsa.go.jp/api/v1/documents'
        self.out_of_since = False
        self.since = since
        self.until = until
        self.file_info_str = since.strftime(
            '_%y%m%d_') + until.strftime('%y%m%d')
        self.edinet_dict_key = 0

    def __get_link_info_str(self, datetime):
        str_datetime = datetime.strftime('%Y-%m-%d')
        params = {"date": str_datetime, "type": 2}
        count, retry = 0, 3
        while True:
            try:
                response = requests.get(
                    f'{ self.base_url }.json', params=params, verify=False)
                return response.text
            except Exception:
                print(f'{str_datetime} のアクセスに失敗しました。[ {count} ]')
                if count < retry:
                    count += 1
                    time.sleep(3)
                    continue
                else:
                    raise

    def __parse_json(self, string):
        res_dict = json.loads(string)
        return res_dict["results"]

    def __get_link(self, target_list):
        edinet_dict = {}
        for target_dict in target_list:
            title = f'{ target_dict["filerName"] } { target_dict["docDescription"] }'
            if not self.__is_yuho(title):
                continue
            docID = target_dict["docID"]
            url = f'{ self.base_url }/{ docID }'
            edinet_code = target_dict['edinetCode']
            updated = target_dict['submitDateTime']
            edinet_dict[self.edinet_dict_key] = {'id': docID, 'title': title,
                                                 'url': url, 'code': edinet_code, 'update': updated}
            self.edinet_dict_key += 1
        return edinet_dict

    def __is_yuho(self, title):
        if all((yuho_word in str(title)) for yuho_word in ['有価証券報告書', '株式会社']) and '受益証券' not in str(title):
            return True
        return False

    def create_xbrl_url_dict_dict(self):
        target_date, result_dict = self.since, {}
        while True:
            print(f'date { target_date.strftime( "%Y-%m-%d" ) }, loading...')
            response_string = self.__get_link_info_str(target_date)
            target_list = self.__parse_json(response_string)
            info_dict = self.__get_link(target_list)
            result_dict = result_dict | info_dict
            time.sleep(self.wait_time)
            target_date = target_date + timedelta(days=1)
            if target_date > self.until:
                break
        print('complete a download!!')
        return result_dict


def edinet_operator(since, until):
    edinet_catcher = catcher(since, until)
    return edinet_catcher.create_xbrl_url_dict_dict()
