#!/usr/bin/bash

cd v-env/lib/python3.7/site-packages
zip -r9 ${OLDPWD}/function.zip .
cd ${OLDPWD}
zip -g function.zip function.py
aws lambda update-function-code --function-name mailchimp-proxy --zip-file fileb://function.zip
