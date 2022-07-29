import os
import re
from tabnanny import check
import pandas as pd
from tqdm import tqdm

from ..models.securityReportsModels import SecurityReports

# csv出力機能はコメントアウトで残しておく


class eggs_operator():
    def __init__(self, dict_codes, dict_cols, result_file_name='com_indices.csv', work_dir=None):
        self.base_path = f'{ os.getcwd() if work_dir==None else work_dir }'
        self.result_file_name = result_file_name
        self.dict_codes = dict_codes
        self.dict_cols = dict_cols

    def __get_element(self, df, col):
        element_ids = self.dict_cols[col]['element_id']
        if col in ['company_name', 'doc_name', 'submit_date', 'start_date', 'end_date']:
            check1 = df[df['element_id'].str.contains(element_ids[0].lower())]
            if len(check1) == 1:
                return check1['amount'].values[0]
            else:
                return ''
        else:
            contextref = self.dict_cols[col]['contextref']
            for element_id in element_ids:
                # element_idのレコードの内、configで定義したelement_idを持つdfを抽出
                check1 = df[df['element_id'].str.contains(element_id.lower())]
                check2 = check1[check1['contextref'] == contextref].copy()
                if len(check2) == 1:
                    return check2['amount'].values[0]
                elif len(check2) > 1:
                    # element_idの文字列が含まれるデータが複数ある場合はelement_idの文字列長が一番短いものをとる
                    check2['str_len'] = check2['element_id'].apply(
                        lambda x: len(str(x)))
                    return check2.loc[check2['str_len'] == check2['str_len'].min(), 'amount'].values[0]
            for element_id in element_ids:
                check1 = df[df['element_id'].str.contains(element_id.lower())]
                check2 = check1[check1['contextref'] ==
                                f'{ contextref }_NonConsolidatedMember'].copy()
                if len(check2) == 1:
                    return check2['amount'].values[0]
                elif len(check2) > 1:
                    check2['str_len'] = check2['element_id'].apply(
                        lambda x: len(str(x)))
                    return check2.loc[check2['str_len'] == check2['str_len'].min(), 'amount'].values[0]
            return 0

    def get_elements(self, xbrl_df):
        # xbrlのデータ一行一行について処理
        file_nm_matched_df = xbrl_df[xbrl_df['element_id'] == 'jpcrp_cor:companynamecoverpage'].drop_duplicates()[
            'file_nm'].values
        for file_nm in tqdm(file_nm_matched_df):
            edinet_code_for_search = re.search(r'E[0-9]{5}', file_nm).group(0)
            if not edinet_code_for_search in self.dict_codes:
                continue
            # 1つの書類内のデータをすべて抽出 (同じファイル名の行をすべて抽出)
            df_target = xbrl_df[xbrl_df['file_nm']
                                == file_nm].drop_duplicates()
            data = {col: self.__get_element(df_target, col)
                    for col in self.dict_cols}
            data['security_code'] = self.dict_codes[edinet_code_for_search]['証券コード']
            data['industory'] = self.dict_codes[edinet_code_for_search]['提出者業種']
            data['correction_flag'] = 1 if '訂正' in data['doc_name'] else 0
            data['file_name'] = file_nm

            security_reports_instance = SecurityReports(
                edinet_code=str(edinet_code_for_search),
                company_name=data['company_name'],
                doc_name=data['doc_name'],
                submit_date=data['submit_date'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                stock=data['stock'],
                cf_sales_cf=data['cf_sales_cf'],
                cf_finance_cf=data['cf_finance_cf'],
                cf_investment_cf=data['cf_investment_cf'],
                cf_money_of_year_end=data['cf_money_of_year_end'],
                pl_net_income=data['pl_net_income'],
                pl_ordinaly_profit=data['pl_ordinaly_profit'],
                pl_operating_income=data['pl_operating_income'],
                pl_amount_of_sales=data['pl_amount_of_sales'],
                bs_cash_deposit=data['bs_cash_deposit'],
                bs_total_debt=data['bs_total_debt'],
                bs_current_assets=data['bs_current_assets'],
                bs_fixed_assets=data['bs_fixed_assets'],
                bs_current_liabilities=data['bs_current_liabilities'],
                bs_fixed_liabilities=data['bs_fixed_liabilities'],
                bs_capital=data['bs_capital'],
                bs_retained_earnings=data['bs_retained_earnings'],
                security_code=data['security_code'],
                industory=data['industory'],
                correction_flag=data['correction_flag'],
                file_name=data['file_name']
            )
            if not SecurityReports.objects.filter(company_name=security_reports_instance.company_name,
                                                  doc_name=security_reports_instance.doc_name,
                                                  submit_date=security_reports_instance.submit_date).exists:
                security_reports_instance.save()

            # 【残しておく】以下3行はCSV出力用 (使用する場合はコメントアウトを外す)
        # pandasのデータフレーム作成
        # com_indices = pd.DataFrame()
        #         raw = pd.DataFrame( data ,index=[ edinet_code_for_search ] )
        #         com_indices = pd.concat( [ com_indices ,raw ] )
        # com_indices.to_csv( os.path.join( self.base_path ,self.result_file_name ) )
