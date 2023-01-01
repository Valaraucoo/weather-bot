# Weather Bot for Facebook 🤖 ☀️ 

This is a simple bot that will tell you the weather in my hometown. It is a simple example of how to use the [Weather API](https://www.weatherapi.com/) to get the weather in a specific location, e.g.

<img width=600 src="https://kw-landing-page.s3.eu-central-1.amazonaws.com/SCR-20230101-px3.png" />

#### How it works?

SAM is a framework that allows you to build serverless applications. It is a wrapper around CloudFormation and allows you to define your application using a simple template. The template is a JSON file that defines the resources that your application needs. In this case, we are using the AWS Lambda function to run our code and the CloudWatch Events to trigger the function.

SAM automatically creates the necessary IAM roles and permissions for the resources that you define in the template. It also creates the CloudFormation stack for you.

#### How to deploy?

You can deploy this application using the SAM CLI. The SAM CLI is an extension of the AWS CLI that adds functionality for building and testing Lambda applications:

```console
sam deploy --guided
```

Or you can push the code to your GitHub repo and the GitHubActions will deploy it for you.
