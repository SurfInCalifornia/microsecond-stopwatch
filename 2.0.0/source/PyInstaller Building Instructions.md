PyInstaller Building Instructions for Stopwatch 2.0.0:

Open a terminal window in the same folder as Stopwatch.pyw. Then run the following command:

pyinstaller --onedir --windowed --icon=logo.ico --add-data "logo.ico;." Stopwatch.pyw