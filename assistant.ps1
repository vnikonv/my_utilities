$llamaServer = "llama-server"
$model = "E:\LLMS\models\gpt-oss-20b-F16.gguf"
$context = 0
$verbose = "--verbose-prompt"

& $llamaServer -m $model -c $context $verbose
