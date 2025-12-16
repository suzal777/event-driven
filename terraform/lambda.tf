data "archive_file" "send_slack" {
  type        = "zip"
  source_file = "../lambda/send_slack.py"
  output_path = "send_slack.zip"
}

resource "aws_lambda_function" "send_slack" {
  function_name = "send-slack-attendance"
  role          = aws_iam_role.lambda_role.arn
  handler       = "send_slack.lambda_handler"
  runtime       = "python3.13"

  filename         = data.archive_file.send_slack.output_path
  source_code_hash = data.archive_file.send_slack.output_base64sha256

  timeout = 5
}


data "archive_file" "handle_response" {
  type        = "zip"
  source_file = "../lambda/handle_response.py"
  output_path = "handle_response.zip"
}

resource "aws_lambda_function" "handle_response" {
  function_name = "handle-slack-response"
  role          = aws_iam_role.lambda_role.arn
  handler       = "handle_response.lambda_handler"
  runtime       = "python3.13"

  filename         = data.archive_file.handle_response.output_path
  source_code_hash = data.archive_file.handle_response.output_base64sha256

  timeout = 5

  environment {
    variables = {
      TABLE_NAME   = aws_dynamodb_table.attendance.name
      EMAIL_DOMAIN = "@gmail.com"
      EMAIL_SENDER = "sujalphaiju@lftechnology.com"
    }
  }
}
