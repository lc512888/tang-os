$cscode = @'
using System;
using System.IO;
using System.Threading.Tasks;
using Windows.Graphics.Imaging;
using Windows.Media.Ocr;
using Windows.Storage;
using Windows.Storage.Streams;

public class OcrHelper {
    public static async Task<string> RecognizeAsync(string filePath) {
        var file = await StorageFile.GetFileFromPathAsync(filePath);
        var stream = await file.OpenReadAsync();
        var decoder = await BitmapDecoder.CreateAsync(stream);
        var sb = await decoder.GetSoftwareBitmapAsync();
        var engine = OcrEngine.TryCreateFromUserProfileLanguages();
        var result = await engine.RecognizeAsync(sb);
        sb.Dispose();
        stream.Dispose();
        return string.Join("\n", result.Lines.Select(l => l.Text));
    }
}
'@

Add-Type -ReferencedAssemblies @(
    "System.Runtime.WindowsRuntime",
    "System.Runtime.WindowsRuntime.UI.Xaml",
    "Windows.Foundation.UniversalApiContract"
) -TypeDefinition $cscode -Language CSharp

$text = [OcrHelper]::RecognizeAsync("$env:TEMP\tang_0.png").GetAwaiter().GetResult()
Write-Output $text
