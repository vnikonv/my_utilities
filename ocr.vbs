Set WshShell = CreateObject("WScript.Shell")

' Input file path
input = WScript.Arguments(0)

' Output file path
output = Left(input, InStrRev(input, ".") - 1)

' An input window for entering the prompt
prompt = InputBox("Enter the prompt:", "LLaMA Prompt")

' Stop if cancel or empty input
If prompt = "" Then WScript.Quit

cmd = "cmd.exe /c llama-mtmd-cli --model ""E:\LLMS\models\Qwen3VL-8B\Qwen3VL-8B-Instruct-Q4_K_M.gguf"" " & _
      "--mmproj-offload -mm ""E:\LLMS\models\Qwen3VL-8B\mmproj-Qwen3VL-8B-Instruct-F16.gguf"" " & _
      "--image """ & input & """ " & _
      "--prompt """ & prompt & """ " & _
      "-ngl all > """ & output & ".txt"""

WshShell.Run cmd, 0, True