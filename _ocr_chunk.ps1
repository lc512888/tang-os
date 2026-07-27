# Load WinRT for OCR
[Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null

$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$path = "$env:TEMP\tang_0.png"

# Load image via WinRT
$file = [Windows.Storage.StorageFile]::GetFileFromPathAsync($path).GetAwaiter().GetResult()
$stream = [Windows.Storage.Streams.RandomAccessStreamReference]::CreateFromFile($file)
$decoder = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream).GetAwaiter().GetResult()
$sb = $decoder.GetSoftwareBitmapAsync().GetAwaiter().GetResult()

# OCR
$result = $engine.RecognizeAsync($sb).GetAwaiter().GetResult()
$sb.Dispose()

# Output text
$result.Lines | ForEach-Object { $_.Text }
