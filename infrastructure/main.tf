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

resource "aws_dynamodb_table" "vectors_for_kankyouhakusyo_rag" {
  name         = "kankyouhakusyo-r6"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Name = "kankyouhakusyo-r6"
  }
}

# s3 backet を作成
resource "aws_s3_bucket" "vectors_for_kankyouhakusyo_rag" {
  bucket = "rag-sample-content"

  tags = {
    Name = "rag-sample-content"
  }
}
