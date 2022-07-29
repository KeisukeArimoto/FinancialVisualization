from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from saveSecurityReports.views.views import save_specified_date_exec


def save_security_reports_daily():
    today_datetime = datetime.now().strftime('%Y-%m-%d')
    save_specified_date_exec(today_datetime, today_datetime)


def start():
    scheduler = BackgroundScheduler()
    # EDINETの書類提出時刻期限は平日9:00~17:15
    scheduler.add_job(save_security_reports_daily, 'cron',
                      hour=19, minute=0, second=0, day_of_week='mon-fri')
    scheduler.start()
