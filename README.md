
## Web Scraping Yahoo! Finance and AWS Lambda Automation Implementation 

AWS Layer creation 

- run following command on docker whcih will create chrome_headless.zip and then upload it as AWS Layer for python 3.7<br>
chmod +x chrome_headless_lambda_layer.sh<br>
./chrome_headless_lambda_layer.sh

- or upload zip file present in AWSLayers\chrome_headless.zip as AWS Layer for python 3.7

Use following lambda function 
https://github.com/vinodvidhole/yahoo-finance-scraper/blob/main/lambda_function.py

