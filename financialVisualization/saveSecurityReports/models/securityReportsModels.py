from tabnanny import verbose
from django.db import models

#有価証券報告書のデータモデル
class SecurityReports(models.Model):
    class Meta:
        db_table = 'security_reports'
        
    #フィールドを定義
    edinet_code = models.CharField(verbose_name='EDINETコード', max_length=255, default='')
    company_name = models.CharField(verbose_name='会社名', max_length=255)
    doc_name = models.CharField(verbose_name='提出書類', max_length=255)
    submit_date = models.DateField(verbose_name='提出日')
    start_date = models.DateField(verbose_name='年度開始日')
    end_date = models.DateField(verbose_name='年度終了日')
    stock = models.IntegerField(verbose_name='発行済み株式数', blank=True)
    cf_sales_cf = models.DecimalField(verbose_name='営業CF', blank=True, max_digits=20, decimal_places=5)
    cf_finance_cf = models.DecimalField(verbose_name='財務CF', blank=True, max_digits=20, decimal_places=5)
    cf_investment_cf = models.DecimalField(verbose_name='投資CF', blank=True, max_digits=20, decimal_places=5)
    cf_money_of_year_end = models.DecimalField(verbose_name='現金及び現金同等物の期末残高', blank=True, max_digits=20, decimal_places=5)
    pl_net_income = models.DecimalField(verbose_name='純利益', blank=True, max_digits=20, decimal_places=5)
    pl_ordinaly_profit = models.DecimalField(verbose_name='経常利益', blank=True, max_digits=20, decimal_places=5)
    pl_operating_income = models.DecimalField(verbose_name='営業利益', blank=True, max_digits=20, decimal_places=5)
    pl_amount_of_sales = models.DecimalField(verbose_name='売上高', blank=True, max_digits=20, decimal_places=5)
    bs_cash_deposit = models.DecimalField(verbose_name='現金預金', blank=True, max_digits=20, decimal_places=5)
    bs_total_debt = models.DecimalField(verbose_name='負債合計', blank=True, max_digits=20, decimal_places=5)
    bs_current_assets = models.DecimalField(verbose_name='流動資産', blank=True, max_digits=20, decimal_places=5)
    bs_fixed_assets = models.DecimalField(verbose_name='固定資産', blank=True, max_digits=20, decimal_places=5)
    bs_current_liabilities = models.DecimalField(verbose_name='流動負債', blank=True, max_digits=20, decimal_places=5)
    bs_fixed_liabilities = models.DecimalField(verbose_name='固定負債', blank=True, max_digits=20, decimal_places=5)
    bs_capital = models.DecimalField(verbose_name='資本金', blank=True, max_digits=20, decimal_places=5)
    bs_retained_earnings = models.DecimalField(verbose_name='利益剰余金', blank=True, max_digits=20, decimal_places=5)
    security_code = models.CharField(verbose_name='証券コード', max_length=4, blank=True)
    industory = models.CharField(verbose_name='業種', max_length=255, blank=True)
    correction_flag = models.BooleanField(verbose_name='訂正フラグ', blank=True)
    file_name = models.CharField(verbose_name='ファイル名', max_length=255, blank=True)

    def __str__(self):
        return  "EDINETコード: " + self.edinet_code\
                +"\n会社名: " + self.company_name\
                + "\n提出書類: " + self.doc_name\
                + "\n提出日: " + self.submit_date\
                + "\n年度開始日: " + self.start_date\
                + "\n年度終了日: " + self.end_date\
                + "\n発行済み株式数: " + str(self.stock)\
                + "\n営業CF: " + str(self.cf_sales_cf)\
                + "\n財務CF: " + str(self.cf_finance_cf)\
                + "\n投資CF: " + str(self.cf_investment_cf)\
                + "\n現金及び現金同等物の期末残高: " + str(self.cf_money_of_year_end)\
                + "\n純利益: " + str(self.pl_net_income)\
                + "\n経常利益: " + str(self.pl_ordinaly_profit)\
                + "\n営業利益: " + str(self.pl_operating_income)\
                + "\n売上高: " + str(self.pl_amount_of_sales)\
                + "\n現金預金: " + str(self.bs_cash_deposit)\
                + "\n負債合計: " + str(self.bs_total_debt)\
                + "\n流動資産: " + str(self.bs_current_assets)\
                + "\n固定資産: " + str(self.bs_fixed_assets)\
                + "\n流動負債: " + str(self.bs_current_liabilities)\
                + "\n固定負債: " + str(self.bs_fixed_liabilities)\
                + "\n資本金: " + str(self.bs_capital)\
                + "\n利益余剰金: " + str(self.bs_retained_earnings)\
                + "\n証券コード: " + str(self.security_code)\
                + "\n業種: " + str(self.industory)\
                + "\n訂正フラグ: " + str(self.correction_flag)\
                + "\nファイル名: " + self.file_name 
