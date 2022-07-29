import os
import re
import io
import time
import requests
import pandas as pd
from tqdm import tqdm
from zipfile import ZipFile
from xbrl import XBRLParser

from saveSecurityReports import WORK_DIR

default_tag = ['file_nm', 'element_id', 'amount']
custom_tag = ['unit_ref', 'decimals', 'contextref']
encode_type = 'utf-8'


class downloader():
    def __init__(self, wait_time=1, work_dir=None, since_datetime=None, until_datetime=None):
        self.wait_time = wait_time
        self.base_path = f'{ os.getcwd() if work_dir==None else work_dir }'
        self.xbrl_file_name = f'{ WORK_DIR }/xbrl_files_downloaded_in_{ since_datetime }_{ until_datetime }/'

    def __make_directory(self, dir_path):
        os.makedirs(dir_path, exist_ok=True)

    def __download_xbrl_file(self, submit_documents_dict):
        for no in tqdm(submit_documents_dict):
            info_dict = submit_documents_dict[no]
            company_path = f'{ self.xbrl_file_name }{ info_dict["code"] }/'
            ir_path = f'{ company_path }{ info_dict["id"] }'
            self.__make_directory(company_path)
            self.__make_directory(ir_path)
            self.__download_and_unzip(info_dict['url'], ir_path)
            no += 1

    def __download_and_unzip(self, url, dir_path):
        count, retry = 0, 3
        while True:
            r = requests.get(url, params={'type': 1})
            time.sleep(self.wait_time)
            if r.status_code == 200:
                z = ZipFile(io.BytesIO(r.content))
                z.extractall(dir_path)
                break
            else:
                print(f'download failed [{ count }]_{ url }')
                if count < retry:
                    count += 1
                    continue
                else:
                    raise

    def download(self, submit_documents_dict):
        if len(submit_documents_dict) > 0:
            self.__make_directory(self.xbrl_file_name)
            self.__download_xbrl_file(submit_documents_dict)
        print('complete a download!!')


class XbrlParser(XBRLParser):
    def __init__(self, xbrl_filepath):
        self.xbrl_filepath = xbrl_filepath

    def parse_xbrl(self):
        # parse xbrl file
        with open(self.xbrl_filepath, 'r', encoding='utf-8') as of:
            xbrl = XBRLParser.parse(of)
        result_list = []
        name_space = 'jp*'
        for node in xbrl.find_all(name=re.compile(name_space+':*')):
            if self.ignore_pattern(node):
                continue
            row_dict = {}
            column_list = ['file_nm', 'element_id', 'amount']
            row_dict['file_nm'] = self.xbrl_filepath.rsplit(os.sep, 1)[1]
            row_dict['element_id'] = node.name
            row_dict['amount'] = node.string
            for tag in custom_tag:
                row_dict[tag] = self.get_attrib_value(node, tag)
                column_list.append(tag)
            result_list.append(row_dict)
        return result_list

    def ignore_pattern(self, node):
        if 'xsi:nil' in node.attrs:
            if node.attrs['xsi:nil'] == 'true':
                return True
        if not isinstance(node.string, str):
            return True  # 結果が空の場合は対象外にする
        if str(node.string).find(u'\n') > -1:
            return True  # 結果が空の場合は対象外にする
        if u'textblock' in str(node.name):
            return True  # 結果が空の場合は対象外にする
        return False

    def get_attrib_value(self, node, attrib):
        if attrib in node.attrs.keys():
            return node.attrs[attrib]
        else:
            return None


class parse_operator():
    def __init__(self, submit_documents_dict_dict, work_dir=None, since_datetime=None, until_datetime=None):
        self.submit_documents_dict_dict = submit_documents_dict_dict
        self.base_path = f'{ os.getcwd() if work_dir==None else work_dir }'
        self.str_period = since_datetime + "_" + until_datetime

    def __fild_all_files(self):
        result = []
        for root, dirs, files in os.walk(self.search_path):
            for file in files:
                if not self.__is_xbrl_file(root, file):
                    continue
                result.append(os.path.join(root, file))
        return result

    def __is_xbrl_file(self, root_path, file_name):
        if not file_name.endswith('.xbrl'):
            return False  # xbrlファイルでなければ対象外
        if u'AuditDoc' in str(root_path):
            return False  # AuditDocは対象外
        if 'xbrl_files_downloaded_in_' + self.str_period in str(root_path):
            return True

    def __dump_file(self, writer, dicts_info):
        i = 0
        while i < len(dicts_info):
            row_dict = dicts_info[i]
            writer.writerow(row_dict)
            i += 1

    def xbrl_to_df(self, since_datetime=None, until_datetime=None):
        self.search_path = f'{ WORK_DIR }/xbrl_files_downloaded_in_{ since_datetime }_{ until_datetime }/'
        all_dicts_info_list = []
        for submit_documents_data in tqdm(self.submit_documents_dict_dict):
            list_xbrl_files = self.__fild_all_files()
            for xbrl_file in list_xbrl_files:
                xp = XbrlParser(xbrl_file)
                dfs_info_list = xp.parse_xbrl()
                all_dicts_info_list.extend(dfs_info_list)
        print('completed conversions!!')
        return pd.DataFrame(all_dicts_info_list)


def xbrl_to_df_operator(submit_documents_dict_dict, work_dir=None, since_datetime=None, until_datetime=None):
    xbrl_downloader = downloader(
        work_dir=work_dir, since_datetime=since_datetime, until_datetime=until_datetime)
    xbrl_downloader.download(submit_documents_dict_dict)
    xbrl_parse_operator = parse_operator(
        submit_documents_dict_dict, work_dir=work_dir, since_datetime=since_datetime, until_datetime=until_datetime)
    return xbrl_parse_operator.xbrl_to_df(since_datetime, until_datetime)
