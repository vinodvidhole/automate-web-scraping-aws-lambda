
## Web Scraping Yahoo! Finance and AWS Lambda Automation Implementation 

checkout my blog
https://medium.com/jovianml/automate-web-scraping-using-python-aws-lambda-amazon-s3-amazon-eventbridge-cloudwatch-c4c982c35fa7

AWS Layer creation 

- run following command on docker whcih will create chrome_headless.zip and then upload it as AWS Layer for python 3.7<br>
chmod +x chrome_headless_lambda_layer.sh<br>
./chrome_headless_lambda_layer.sh

- or upload zip file present in AWSLayers\chrome_headless.zip as AWS Layer for python 3.7

Use following lambda function 
https://github.com/vinodvidhole/automate-web-scraping-aws-lambda/blob/main/lambda_function.py

