from yfapi import YahooFinanceAPI, Interval
from datetime import date
import pandas as pd
import s3_op

def import_data_from_api():
    try:
        data = YahooFinanceAPI(Interval.DAILY)

        now = date.today()

        from_date = date(2021,1,1)

        full_data = data.get_data_for_tickers(["aapl","amzn"],from_date,now)

        apple_data = full_data["aapl"]
        apple_data["company_id"] = "aapl"
        amazon_data = full_data["amzn"]
        amazon_data["company_id"] = "amzn"
        apple_data_csv = pd.DataFrame(apple_data)
        amazon_data_csv = pd.DataFrame(amazon_data)
        final_data = pd.concat([apple_data_csv,amazon_data_csv],axis=0)
        final_data.to_csv("final_data.csv", index=False, sep=',', encoding='utf-8')
        # apple_data_csv.to_csv("apple_data.csv",index=False,sep=',', encoding='utf-8')
        # amazon_data_csv.to_csv("amazon_data.csv",index=False,sep=',', encoding='utf-8')

        return True
    except Exception as e:
        print("Error in importing data from API")
        print("Exception: ",e)
