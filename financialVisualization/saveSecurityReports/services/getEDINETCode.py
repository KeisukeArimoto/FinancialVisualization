import codecs
import pandas as pd

def get_dict_edinet_codes( DIR ,index='証券コード' ) :
    file_path = f'{DIR}/EdinetcodeDlInfo.csv'

    with codecs.open( file_path, "r", "Shift-JIS", "ignore" ) as file :
        df = pd.read_csv( file ,skiprows=[0] ,usecols=['ＥＤＩＮＥＴコード','提出者名','証券コード','提出者業種'] )
    df = df.loc[ df['証券コード'] > 0 ,: ]
    ##EDINETの証券コードには通常の証券コードの最後に「0」が付与されているため、10で割る
    df['証券コード'] = df['証券コード'] / 10
    df['証券コード'] = df['証券コード'].astype( int )
    result = df.set_index( index ).T.to_dict()
    print( f'対象(EDINET): { len( result ) }銘柄' )
    return result
