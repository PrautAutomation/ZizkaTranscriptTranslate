### Step 1: Install Python

If you already have Python installed, you can skip this. I recommend version **3.9 or newer**.

1.  Go to the official Python website: [python.org/downloads/windows](https://www.python.org/downloads/windows/)
2.  Download the **64-bit Installer** for the latest stable version (e.g., Python 3.12.x).
3.  **VERY IMPORTANT:** During installation, make sure to check the box that says **"Add python.exe to PATH"**. This will save you a lot of headaches with the command line.
4.  Complete the installation.

---

### Step 2: Install FFmpeg
New 
FFmpeg is essential for Whisper to process audio and video files.

1.  Go to [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2.  Click the Windows icon (the one with the Windows logo).
3.  Click on **"Windows builds from gyan.dev"**.
4.  Scroll down and download the `.7z` file (e.g., `ffmpeg-git-full.7z` or similar). It will contain the word `full`.
5.  **Extract this file** (you might need 7-Zip if you don't have it installed) to an easily memorable directory, like `C:\ffmpeg`. You should then have a `C:\ffmpeg\bin` directory – this is important.
6.  **Add FFmpeg to your system's PATH variable:**
    * In the Windows search bar (next to the Start button), type "environment variables" and click on "Edit the system environment variables".
    * In the "System Properties" window, click the **"Environment Variables..."** button.
    * In the "System variables" section (the bottom half), find the variable named **"Path"** and double-click it.
    * Click "New" and add the path to the `bin` folder of FFmpeg. For example: `C:\ffmpeg\bin`
    * Click "OK" on all open windows.
7.  **Verify:** Open a **new** `Command Prompt` (CMD) window and type `ffmpeg -version`. You should see FFmpeg information. If not, restart your computer or double-check the path in your environment variables.

---

### Step 3: Install PyTorch with CUDA Support (for your RTX 4090)

This is the crucial step for leveraging your 4090.

1.  Open a **new** `Command Prompt` (CMD) window.
2.  Go to the PyTorch website: [pytorch.org/get-started/locally](https://pytorch.org/get-started/locally)
3.  Select your preferences:
    * **Stable**
    * Your OS: **Windows**
    * Package: **Pip**
    * Language: **Python**
    * CUDA: **CUDA 12.1** (or newer, if available and your drivers support it. Always choose the latest one available that works with your current NVIDIA drivers. The RTX 4090 needs a newer CUDA version than 11.x).
4.  Copy the command that appears. It will look something like this (the exact version might differ):
    ```bash
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    ```
5.  **Paste this command into your CMD and press Enter.** Wait for everything to download and install. It will be a few hundred MBs.

---

### Step 4: Install OpenAI Whisper

1.  In the same CMD window (or a new one), type:
    ```bash
    pip install openai-whisper
    ```
2.  Wait for the installation to complete.

---

### Step 5: Use Whisper for Czech transcription!

Now for the most important part – running it.

1.  Open a **text editor** (Notepad, VS Code, etc.).
2.  Paste the following Python code into it:

    ```python
    import whisper
    import os

    # Path to your audio file
    # You can specify the full path, e.g., r"C:\Users\Your_Name\Desktop\my_audio.mp3"
    # Make sure the file exists!
    audio_file_path = "your_audio_file.wav" # Replace with the actual path to your file!

    # Which model to use.
    # "large-v3" is the largest and most accurate model, ideal for your 4090.
    # You can also try "medium" or "large" if you prefer smaller file sizes.
    model_name = "large-v3"

    print(f"Loading model '{model_name}'. This might take a while the first time as it downloads.")
    model = whisper.load_model(model_name)

    print(f"Transcribing audio file: {audio_file_path}")
    print("This might take a moment, but with a 4090, it will be fast!")

    # language="cs" explicitly tells Whisper to expect Czech.
    # It helps improve accuracy for the Czech language.
    result = model.transcribe(audio_file_path, language="cs", fp16=True)
    # fp16=True uses "float16" precision, which is faster on NVIDIA GPUs
    # and uses less VRAM. With a 4090, this is usually beneficial.

    print("\n--- Transcribed Text ---")
    print(result["text"])
    print("----------------------")

    # You can also save the text to a file
    output_filename = os.path.splitext(audio_file_path)[0] + "_transcription.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f"Transcribed text saved to: {output_filename}")

    ```
3.  **Save this file** as `transcribe.py` (or any name ending with `.py`) in a location you can easily access (e.g., `C:\Users\Your_Name\Documents`).
4.  **Place your audio file** (e.g., `my_audio.mp3` or `my_audio.wav`) in the **same folder** where you saved `transcribe.py`.
5.  **Edit the `audio_file_path` line** in the Python script to match your file's name (or its full path if it's not in the same folder). For example: `audio_file_path = "my_audio.mp3"`

---

### Step 6: Run the Script from Command Prompt

1.  Open a **new** `Command Prompt` (CMD) window.
2.  Navigate to the folder where you saved `transcribe.py` and your audio file. Use the `cd` command. For example:
    ```bash
    cd C:\Users\Your_Name\Documents
    ```
    (replace `C:\Users\Your_Name\Documents` with your actual path)
3.  Run the script:
    ```bash
    python transcribe.py
    ```
4.  **The first time you run it,** the selected Whisper model (`large-v3`) will download. This can take some time (it's a few GBs), but after that, it will just load from your disk. With your 4090, the actual transcription should be incredibly fast!