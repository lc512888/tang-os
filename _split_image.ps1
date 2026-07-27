Add-Type -AssemblyName System.Drawing
$src = "$env:USERPROFILE\Desktop\tang.png"
$img = [System.Drawing.Image]::FromFile($src)
$totalH = $img.Height
$scale = 800.0 / $img.Width
$chunkH = [int](4000 * $scale)
$totalScaled = [int]($totalH * $scale)
$numChunks = [math]::Ceiling($totalScaled / $chunkH)
Write-Output "Total: $($img.Width)x$totalH, chunks: $numChunks"
for ($i = 0; $i -lt $numChunks; $i++) {
    $y = $i * $chunkH
    $h = [math]::Min($chunkH, $totalScaled - $y)
    if ($h -le 0) { break }
    $srcY = [int]($y / $scale)
    $srcH = [int]($h / $scale)
    $bmp = New-Object System.Drawing.Bitmap(800, $h)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $rect = New-Object System.Drawing.Rectangle(0, 0, 800, $h)
    $srcRect = New-Object System.Drawing.Rectangle(0, $srcY, $img.Width, $srcH)
    $g.DrawImage($img, $rect, $srcRect, [System.Drawing.GraphicsUnit]::Pixel)
    $g.Dispose()
    $out = "$env:TEMP\tang_$i.png"
    $bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp.Dispose()
    Write-Output "Chunk $i saved: $out"
}
$img.Dispose()
Write-Output "Done"
