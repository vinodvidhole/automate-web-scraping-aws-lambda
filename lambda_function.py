try:
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    import boto3
    import csv
    from io import StringIO
    from datetime import datetime
    print("All Modules are ok ...")

except Exception as e:
    print("Error in Imports ")

YAHOO_FINANCE_URL = "https://finance.yahoo.com/trending-tickers"

class WebDriver(object):

    def __init__(self):
        self.options = Options()

        self.options.binary_location = '/opt/headless-chromium'
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--start-fullscreen')
        self.options.add_argument('--single-process')
        self.options.add_argument('--disable-dev-shm-usage')

    def get(self):
        driver = Chrome('/opt/chromedriver', options=self.options)
        return driver
        
def get_tickers(driver):
    """return the number of tickers available on the webpage"""
    TABLE_CLASS = "W(100%)"  
    tablerows = len(driver.find_elements(By.XPATH, value="//table[@class= '{}']/tbody/tr".format(TABLE_CLASS)))
    return tablerows

def parse_ticker(rownum, table_driver):
    """Parsing each Ticker row by row and return the data in the form of Python dictionary"""
    Symbol = table_driver.find_element(By.XPATH, value="//tr[{}]/td[1]".format(rownum)).text
    Name = table_driver.find_element(By.XPATH, value="//tr[{}]/td[2]".format(rownum)).text
    LastPrice = table_driver.find_element(By.XPATH, value="//tr[{}]/td[3]".format(rownum)).text
    MarketTime = table_driver.find_element(By.XPATH, value="//tr[{}]/td[4]".format(rownum)).text
    Change = table_driver.find_element(By.XPATH, value="//tr[{}]/td[5]".format(rownum)).text
    PercentChange = table_driver.find_element(By.XPATH, value="//tr[{}]/td[6]".format(rownum)).text	
    Volume = table_driver.find_element(By.XPATH, value="//tr[{}]/td[7]".format(rownum)).text
    MarketCap = table_driver.find_element(By.XPATH, value="//tr[{}]/td[8]".format(rownum)).text	

    return {
    'Symbol': Symbol,
    'Name': Name,
    'LastPrice': LastPrice,
    'MarketTime': MarketTime,
    'Change': Change,
    'PercentChange': PercentChange,
    'Volume': Volume,
    'MarketCap': MarketCap
    }

def upload_csv_s3(data_dictionary,s3_bucket_name,csv_file_name):
    data_dict = data_dictionary
    data_dict_keys = data_dictionary[0].keys()
    
    # creating a file buffer
    file_buff = StringIO()
    
    # writing csv data to file buffer
    writer = csv.DictWriter(file_buff, fieldnames=data_dict_keys)
    writer.writeheader()
    for data in data_dict:
        writer.writerow(data)
        
    # creating s3 client connection
    client = boto3.client('s3')
    
    # placing file to S3, file_buff.getvalue() is the CSV body for the file
    client.put_object(Body=file_buff.getvalue(), Bucket=s3_bucket_name, Key=csv_file_name)
    print('Done uploading to S3')

def lambda_handler(event, context):
    instance_ = WebDriver()
    driver = instance_.get()
    driver.get(YAHOO_FINANCE_URL)
    print('Fetching the page')
    table_rows = get_tickers(driver)
    print('Found {} Tickers'.format(table_rows))
    print('Parsing Trending tickers')
    table_data = [parse_ticker(i, driver) for i in range (1, table_rows + 1)]
    
    driver.close()
    driver.quit()
    
    #create csv and upload in s3 bucket
    dt_string = datetime.now().strftime("%Y-%m-%d_%H%M")
    csv_file_name =  'trending-tickers_'+dt_string +'.csv'
    upload_csv_s3(table_data,'automate-web-scraping',csv_file_name)

    response = {
        "Rows": table_rows,
        "body": table_data
    }

    return response
    
if __name__ == "__main__":
    lambda_handler(None, None)