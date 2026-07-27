$chunk = 0
$path = "$env:TEMP\tang_$chunk.png"
Write-Output "Processing: $path"

[Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
[Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime] | Out-Null
[Windows.Storage.Streams.RandomAccessStreamReference, Windows.Storage.Streams, ContentType = WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType = WindowsRuntime] | Out-Null

$eng = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
Write-Output "Language: $($eng.RecognizerLanguage)"

$file = [Windows.Storage.StorageFile]::GetFileFromPathAsync($path).GetAwaiter().GetResult()
Write-Output "File loaded: $($file.Name)"

$stream = [Windows.Storage.Streams.RandomAccessStreamReference]::CreateFromFile($file)
$decoder = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream).GetAwaiter().GetResult()
$sb = $decoder.GetSoftwareBitmapAsync().GetAwaiter().GetResult()

# Convert to grayscale for better OCR
$sb2 = [Windows.Graphics.Imaging.SoftwareBitmap]::Convert($sb, [Windows.Graphics.Imaging.BitmapPixelFormat]::Gray8)

$result = $eng.RecognizeAsync($sb2).GetAwaiter().GetResult()
$sb.Dispose()
$sb2.Dispose()

Write-Output "=== TEXT START ==="
$result.Lines | ForEach-Object { $_.Text }
Write-Output "=== TEXT END ==="
