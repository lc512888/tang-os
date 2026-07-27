Add-Type -AssemblyName System.Runtime.WindowsRuntime

$chunk = 0
$path = "$env:TEMP\tang_$chunk.png"
Write-Output "Processing: $path"

[Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
[Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime] | Out-Null
[Windows.Storage.Streams.RandomAccessStreamReference, Windows.Storage.Streams, ContentType = WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType = WindowsRuntime] | Out-Null

$eng = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
Write-Output "OCR Engine: $($eng.RecognizerLanguage)"

# Use AsTask() pattern for WinRT async
$op1 = [Windows.Storage.StorageFile]::GetFileFromPathAsync($path)
$task1 = [System.WindowsRuntimeSystemExtensions]::AsTask($op1)
$task1.Wait()
$file = $task1.Result
Write-Output "File: $($file.Name)"

$op2 = $file.OpenReadAsync()
$task2 = [System.WindowsRuntimeSystemExtensions]::AsTask($op2)
$task2.Wait()
$stream = $task2.Result
Write-Output "Stream opened"

$op3 = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)
$task3 = [System.WindowsRuntimeSystemExtensions]::AsTask($op3)
$task3.Wait()
$decoder = $task3.Result

$op4 = $decoder.GetSoftwareBitmapAsync()
$task4 = [System.WindowsRuntimeSystemExtensions]::AsTask($op4)
$task4.Wait()
$sb = $task4.Result
Write-Output "Bitmap: $($sb.PixelWidth)x$($sb.PixelHeight)"

$op5 = $eng.RecognizeAsync($sb)
$task5 = [System.WindowsRuntimeSystemExtensions]::AsTask($op5)
$task5.Wait()
$result = $task5.Result

$sb.Dispose()
$stream.Dispose()

Write-Output "=== TEXT START ==="
$result.Lines | ForEach-Object { $_.Text }
Write-Output "=== TEXT END ==="
