# DataGuardian

**DataGuardian** is an innovative platform designed to help users monitor and audit their data privacy in real-time across various online platforms. The project integrates AWS Lambda for serverless processing, AWS API Gateway for data ingestion, AWS DynamoDB for storing audit results, and a web interface for visualizing privacy audit outcomes.

## Features

- Real-time data privacy auditing across multiple platforms
- Serverless architecture using AWS Lambda
- Data ingestion via AWS API Gateway
- Data storage in AWS DynamoDB
- Interactive and responsive web interface with data visualization
- Integration with AWS SDKs
- Comprehensive unit tests

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/DataGuardian.git
    cd DataGuardian
    ```

2. Build the Lambda function:
    ```bash
    cd serverless_functions
    ./build_lambda.sh
    ```

3. Deploy the infrastructure using AWS SAM:
    ```bash
    cd deployment
    ./deploy_infrastructure.sh
    ```

## Usage

- Access the API endpoint via AWS API Gateway
- Monitor data storage in AWS DynamoDB
- Visualize privacy audit results in the web interface

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
