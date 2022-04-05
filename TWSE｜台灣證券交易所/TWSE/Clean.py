import pandas as pd

class Clean:
    '''將json轉換成DataFrame'''
    def to_df(data, stock_code=None):
        df = pd.DataFrame(data['data'])
        df.columns = data['fields']
        df['日期'] = df['日期'].apply(Clean.ROC_to_date)
        df = df.applymap(Clean.comma)
        df = df.applymap(Clean.to_float)
        if stock_code:
            df['股票代碼'] = stock_code

        return df

    def to_df_num(data, num=''):
        df = pd.DataFrame(data[f'data{num}'])
        df.columns = data[f'fields{num}']

        df = df.applymap(Clean.comma)
        df = df.applymap(Clean.to_float)
        df = df.applymap(Clean.html_format)

        return df

    def to_float(x):
        try:
            return float(x)
        except ValueError:
            return x

    def pct_to_float(x):
        if '%' in x:
            try:
                return float(x.strip('%'))/100
            except ValueError:
                return x	
        else:
            return x	
	
    def comma(x):
        try:
            return str(x).replace(',','')
        except ValueError:
            return x
    def replace_triangle(x):
        list_replace = ['▲','▼']
        try:
            return x.replace(list_replace[0], '').replace(list_replace[1], '')
        except:
            return x
		
    def ROC_to_date(ROC_date):
        import datetime
	    
        list_ROC_date = [int(d) for d in ROC_date.split('/')]
        date = datetime.datetime(list_ROC_date[0]+1911, list_ROC_date[1], list_ROC_date[2])
	    
        return datetime.datetime.date(date)
    def html_format(x):
        try:
            x = x.replace('<p style= color:green>', '')
            x = x.replace('<p style= color:red>', '')
            x = x.replace("<p style ='color:green'>", '')
            x = x.replace("<p style ='color:red'>", '')
            x = x.replace('</p>', '')
            return x
        except AttributeError:
            return x