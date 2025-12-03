resource "aws_sqs_queue" "dlq" {
  name = "${var.project}-${var.env}-dlq"
}

resource "aws_sqs_queue" "dns_updates" {
  name                       = "${var.project}-${var.env}"
  visibility_timeout_seconds = 60
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount     = 5
  })
}