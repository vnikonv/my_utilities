$llamaServer = "llama-server"
$model = "E:\LLMS\models\gpt-oss-20b-F16.gguf"
$verbose = "--verbose-prompt"
$ngl = 25

& $llamaServer -m $model $verbose -ngl $ngl
