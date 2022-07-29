#（複数あるものは上のものほど優先される）
dict_cols = {
      'company_name'           : { 'element_id' : ['companynamecoverpage'] }
    , 'doc_name'         : { 'element_id' : ['documenttitlecoverpage'] }
    , 'submit_date'           : { 'element_id' : ['filingdatecoverpage'] }
    , 'start_date'       : { 'element_id' : ['currentfiscalyearstartdatedei'] }
    , 'end_date'       : { 'element_id' : ['currentfiscalyearenddatedei'] }
    #---ここまで必須---
    #以下は 'contextref' が必須
    , 'stock'   : { 'element_id' : ['totalnumberofissuedsharessummaryofbusinessresults'
                                            ,'totalnumberofissuedsharescommonstocksummaryofbusinessresults'
                                            ,'totalnumberofissuedshares']
                            ,'contextref' : 'CurrentYearInstant' }
    , 'cf_sales_cf'           : { 'element_id' : ['CashFlowsFromUsedInOperatingActivities'
                                            ,'cashflowsfromusedinoperatingactivitiesifrssummaryofbusinessresults'
                                            ,'CashFlowsFromUsedInOperatingActivitiesUSGAAPSummaryOfBusinessResults'
                                            ,'netcashprovidedbyusedinoperatingactivitiessummaryofbusinessresults'
                                            ,'NetCashProvidedByUsedInOperatingActivities']
                            ,'contextref' : 'CurrentYearDuration' }
    , 'cf_finance_cf'           : { 'element_id' : ['CashFlowsFromUsedInFinancingActivities'
                                            ,'cashflowsfromusedinfinancingactivitiesifrssummaryofbusinessresults'
                                            ,'CashFlowsFromUsedInFinancingActivitiesUSGAAPSummaryOfBusinessResults'
                                            ,'NetCashProvidedByUsedInFinancingActivities'
                                            ,'netcashprovidedbyusedinfinancingactivitiessummaryofbusinessresults']
                            ,'contextref' : 'CurrentYearDuration' }
    , 'cf_investment_cf'           : { 'element_id' : ['CashFlowsFromUsedInInvestingActivities'
                                            ,'cashflowsfromusedininvestingactivitiesifrssummaryofbusinessresults'
                                            ,'CashFlowsFromUsedInInvestingActivitiesUSGAAPSummaryOfBusinessResults'
                                            ,'NetCashProvidedByUsedInInvestmentActivities'
                                            ,'netcashprovidedbyusedininvestingactivitiessummaryofbusinessresults']
                            ,'contextref' : 'CurrentYearDuration' }
    , 'cf_money_of_year_end': { 'element_id' : ['CashAndCashEquivalents'
                                            ,'CashAndCashEquivalentsSummaryOfBusinessResults'
                                            ,'CashAndCashEquivalentsUSGAAPSummaryOfBusinessResults'
                                            ,'CashAndCashEquivalentsIFRSSummaryOfBusinessResults']
                            ,'contextref' : 'CurrentYearDuration' }
    , 'pl_net_income'           : { 'element_id' : ['profitlossattributabletoownersofparentsummaryofbusinessresults'
                                            ,'ProfitLossAttributableToOwnersOfParentIFRSSummaryOfBusinessResults'
                                            ,'NetIncomeLossAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults'
                                            ,'netincomelosssummaryofbusinessresults']
                            ,'contextref' : 'CurrentYearDuration' }
    , 'pl_ordinaly_profit'           : { 'element_id' : ['OrdinaryIncome'
                                            ,'OrdinaryIncomeLossSummaryOfBusinessResults']
                            ,'contextref' : 'CurrentYearDuration' }  
    , 'pl_operating_income'           : { 'element_id' : ['OperatingIncome'
                                            ,'ProfitLossFromOperatingActivities'
                                            ,'OperatingIncomeLoss'
                                            ,'OperatingIncomeLossUSGAAPSummaryOfBusinessResults'
                                            ,'OperatingProfitLossIFRSSummaryOfBusinessResults'
                                            ,'OperatingProfitIFRSSummaryOfBusinessResults'
                                            ,'OperatingIncomeLossIFRSSummaryOfBusinessResults'
                                            ,'OperatingIncomeIFRSSummaryOfBusinessResults']
                            ,'contextref' : 'CurrentYearDuration' }                      
    , 'pl_amount_of_sales'           : { 'element_id' : ['businessrevenuesummaryofbusinessresults'
                                            ,'ContractsCompletedRevOA'
                                            ,'netoperatingrevenuesummaryofbusinessresults'
                                            ,'netsales'
                                            ,'NetSalesNS'
                                            ,'NetSalesAndOperatingRevenue'
                                            ,'netsalessummaryofbusinessresults'
                                            ,'NetSalesIFRSSummaryOfBusinessResults'
                                            ,'NetSalesAndServiceRevenueSummaryOfBusinessResults'
                                            ,'NetSalesAndOtherOperatingRevenueSummaryOfBusinessResults'
                                            ,'NetSalesAndOperatingRevenueSummaryOfBusinessResults'
                                            ,'NetSalesAndOperatingRevenue2SummaryOfBusinessResults'
                                            ,'OperatingRevenueELE'
                                            ,'OperatingRevenueRWY'
                                            ,'OperatingRevenueSEC'
                                            ,'operatingrevenue1summaryofbusinessresults'
                                            ,'PLJHFDAKJHGF'
                                            ,'Revenue'
                                            ,'RevenueSummaryOfBusinessResults'
                                            ,'RevenueIFRSSummaryOfBusinessResults'
                                            ,'RevenuesUSGAAPSummaryOfBusinessResults'
                                            ,'revenueifrssummaryofbusinessresults'
                                            ,'SalesAllSegments'
                                            ,'SalesDetails'
                                            ,'SalesAndOtherOperatingRevenueSummaryOfBusinessResults'
                                            ,'ShippingBusinessRevenueWAT'
                                            ,'ShippingBusinessRevenueAndOtherOperatingRevenueWAT'
                                            ,'ShippingBusinessRevenueAndOtherServiceRevenueWAT'
                                            ,'TotalSales'
                                            ,'TotalTradingTransactionIFRSSummaryOfBusinessResults'
                                            ,'TotalTradingTransactionsIFRSSummaryOfBusinessResults']
                            ,'contextref' : 'CurrentYearDuration' }
    , 'bs_cash_deposit'      : { 'element_id' : ['cashanddeposits']
                            ,'contextref' : 'CurrentYearInstant' }
    , 'bs_total_debt'      : { 'element_id' : ['liabilities']
                            ,'contextref' : 'CurrentYearInstant' }
    , 'bs_current_assets'      : { 'element_id' : ['CurrentAssets']
                            ,'contextref' : 'CurrentYearInstant' }
    , 'bs_fixed_assets'      : { 'element_id' : ['NoncurrentAssets']
                            ,'contextref' : 'CurrentYearInstant' }
    , 'bs_current_liabilities'      : { 'element_id' : ['CurrentLiabilities']
                            ,'contextref' : 'CurrentYearInstant' }
    , 'bs_fixed_liabilities'      : { 'element_id' : ['NoncurrentLiabilities']
                            ,'contextref' : 'CurrentYearInstant' }
    , 'bs_capital'      : { 'element_id' : ['CapitalStock'
                                          ,'IssuedCapital'
                                          ,'CapitalStockSummaryOfBusinessResults']
                            ,'contextref' : 'CurrentYearInstant' }
    , 'bs_retained_earnings'   : { 'element_id' : ['RetainedEarnings']
                            ,'contextref' : 'CurrentYearInstant' }

    }