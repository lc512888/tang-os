$chunk = 0
$path = "$env:TEMP\tang_$chunk.png"
Write-Output "Processing: $path"

[Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
[Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime] | Out-Null
[Windows.Storage.Streams.RandomAccessStreamReference, Windows.Storage.Streams, ContentType = WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType = WindowsRuntime] | Out-Null

$eng = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
Write-Output "Language: $($eng.RecognizerLanguage)"

# Sync pattern for WinRT async calls
$asyncOp = [Windows.Storage.StorageFile]::GetFileFromPathAsync($path)
while ($asyncOp.Status -eq 'Started') { Start-Sleep -Milliseconds 50 }
$file = $asyncOp.GetResults()
Write-Output "File: $($file.Name)"

$asyncOp2 = [Windows.Storage.Streams.RandomAccessStreamReference]::CreateFromFile($file)
$asyncOp3 = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($asyncOp2)
while ($asyncOp3.Status -eq 'Started') { Start-Sleep -Milliseconds 50 }
$decoder = $asyncOp3.GetResults()

$asyncOp4 = $decoder.GetSoftwareBitmapAsync()
while ($asyncOp4.Status -eq 'Started') { Start-Sleep -Milliseconds 50 }
$sb = $asyncOp4.GetResults()
Write-Output "Bitmap: $($sb.PixelWidth)x$($sb.PixelHeight)"

$asyncOp5 = $eng.RecognizeAsync($sb)
while ($asyncOp5.Status -eq 'Started') { Start-Sleep -Milliseconds 50 }
$result = $asyncOp5.GetResults()
$sb.Dispose()

Write-Output "=== TEXT START ==="
$result.Lines | ForEach-Object { $_.Text }
Write-Output "=== TEXT END ==="
