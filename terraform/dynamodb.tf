resource "aws_dynamodb_table" "attendance" {
  name         = "DailyWorkMode"
  billing_mode = "PAY_PER_REQUEST"

  hash_key  = "date"
  range_key = "username"

  attribute {
    name = "date"
    type = "S"
  }

  attribute {
    name = "username"
    type = "S"
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }
}
