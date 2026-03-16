# Start the assistant model
# Path to the model
$model = "E:\LLMS\models\gpt-oss-20b-F16.gguf"

# Context length
$context = 4096

# Execute llama-server
& "llama-server" `
    -m $model `      # model file
    -c $context `    # context length
