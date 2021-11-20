# UpdateCheckerLambdas

WIP!
Soon to be a collection of lambdas which will go and check whether an update for a product is available. 
The version is checked against a version stored in DynamoDB.

### Technologies
- AWS
- Lambdas
- Serverless Framework
- Python

### How to use it:
#### Deploy
```
sls deploy
```

#### Invoke
Invoke a specific lambda function
```
sls invoke -f ikea
```

#### Logs
Get cloudwatch logs for a specific lambda function
```
sls logs -f ikea
```

#### Remove
Removes everything from AWS
```
sls remove
```


### Secrets
Secrets have been stored in AWS via AWS SSM parameter store: https://www.serverless.com/blog/aws-secrets-management/

### Install python certificates
Can't send mails because you installed python via brew and now it's complaining about certificates?
Just run some `shadystufftoinstallcertificates.py`.

