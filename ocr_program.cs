using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Windows.Graphics.Imaging;
using Windows.Media.Ocr;
using Windows.Storage;
using Windows.Storage.Streams;

class OcrProgram {
    static void Main(string[] args) {
        var path = args[0];
        var output = args.Length > 1 ? args[1] : Path.GetTempPath() + "ocr_output.txt";
        try {
            var task = RecognizeAsync(path);
            task.Wait();
            File.WriteAllText(output, task.Result);
            Console.WriteLine("OK: " + output);
        } catch (Exception ex) {
            Console.WriteLine("ERROR: " + ex.ToString());
        }
    }

    static async Task<string> RecognizeAsync(string filePath) {
        var file = await StorageFile.GetFileFromPathAsync(filePath);
        using (var stream = await file.OpenReadAsync()) {
            var decoder = await BitmapDecoder.CreateAsync(stream);
            using (var sb = await decoder.GetSoftwareBitmapAsync()) {
                var engine = OcrEngine.TryCreateFromUserProfileLanguages();
                var result = await engine.RecognizeAsync(sb);
                var lines = result.Lines.Select(l => l.Text);
                return string.Join(Environment.NewLine, lines);
            }
        }
    }
}
