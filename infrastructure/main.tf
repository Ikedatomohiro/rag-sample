provider "aws" {
  region = var.aws_region
}

resource "aws_dynamodb_table" "vectors_for_rag" {
  name         = "rag-sample"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Name = "rag-sample"
  }
}
