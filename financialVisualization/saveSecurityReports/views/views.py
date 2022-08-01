import datetime
import os
import shutil
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from saveSecurityReports import APP_LABEL, EDINET_CODE_DIR, WORK_DIR
from saveSecurityReports.services.getDoclistServices import edinet_operator
from saveSecurityReports.services.getEDINETCode import get_dict_edinet_codes
from saveSecurityReports.services.getXBRLDoc import xbrl_to_df_operator
from saveSecurityReports.services.financialDataConfig import dict_cols
from saveSecurityReports.services.getFinancialData import eggs_operator

# クライアントからのリクエストに応じて必要なロジックに割り振り、レンダリングする


@login_required
def show_management_view(request):
    return render(request, '%s/admin.html' % APP_LABEL)


@login_required
def save_specified_date(request):
    if request.method == 'POST':
        since_datetime = datetime.datetime.strptime(
            request.POST['since'], '%Y-%m-%d')
        until_datetime = datetime.datetime.strptime(
            request.POST['until'], '%Y-%m-%d')
        print('=======有価証券報告書のデータ保存指定区間=======\nSince: ' +
              request.POST['since'] + '\nto: ' + request.POST['until'] + '\n================================================')

        save_specified_date_exec(since_datetime, until_datetime)

    # TODO レンダリング後のURLが/saveSpecifiedDateになっているので/adminにしたい
    return render(request, '%s/admin.html' % APP_LABEL, context={'since': request.POST['since'], 'until': request.POST['until']})


def save_specified_date_exec(since_datetime, until_datetime):
    # 作業ディレクトリ作成
    os.mkdir(WORK_DIR)

    # 書類一覧取得API実行
    submit_documents_dict_dict = edinet_operator(
        since_datetime, until_datetime)

    # xbrl取得API実行
    xbrl_df = xbrl_to_df_operator(submit_documents_dict_dict=submit_documents_dict_dict,
                                  work_dir=WORK_DIR, since_datetime=since_datetime.strftime('%Y-%m-%d'), until_datetime=until_datetime.strftime('%Y-%m-%d'))

    # EDINET Code取得 (該当ファイルは定期的にアップデートする必要がある)
    dict_codes = get_dict_edinet_codes(EDINET_CODE_DIR, 'ＥＤＩＮＥＴコード')

    # 有価証券報告書データDB保存
    egg_operator = eggs_operator(dict_codes, dict_cols, work_dir=WORK_DIR)
    egg_operator.get_elements(xbrl_df)

    # tmpディレクトリは削除しているので、csvファイルの中身など見たい場合はコメントアウトする
    shutil.rmtree(WORK_DIR)
