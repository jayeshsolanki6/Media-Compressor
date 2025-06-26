import os
import soundfile as sf
from moviepy.editor import VideoFileClip
from tkinter import Tk, Button, Label, filedialog, StringVar, Entry
from PIL import Image

def browse_file():
    global file_path, file_type
    file_path = filedialog.askopenfilename(filetypes=[
        ("Media Files", "*.wav;*.flac;*.mp3;*.mp4;*.avi;*.mov;*.jpg;*.jpeg;*.png;*.bmp")])
    if file_path:
        file_type = os.path.splitext(file_path)[1].lower()
        label.config(text=f"Selected file: {os.path.basename(file_path)}")

def compress_audio():
    if file_path:
        # Read the audio file
        data, sample_rate = sf.read(file_path)
        
        # Reduce the sample rate (e.g., halve it)
        new_sample_rate = sample_rate // 2
        
        # Downsample the audio data by taking every second sample
        compressed_data = data[::2]
        
        compressed_file_path = os.path.splitext(file_path)[0] + "_compressed.wav"
        
        # Write the new audio file with reduced sample rate
        sf.write(compressed_file_path, compressed_data, new_sample_rate)
        label.config(text=f"Compressed audio saved as: {os.path.basename(compressed_file_path)}")
    else:
        label.config(text="Please select an audio file first.")

def compress_video(input_file, output_file, codec='libx264', bitrate='100k'):
    # Load the video file
    video = VideoFileClip(input_file)
    
    # Write the compressed video to the output file
    video.write_videofile(output_file, codec=codec, bitrate=bitrate, logger=None)
    
    # Close the video file
    video.close()

def compress_image(input_path):
    """Compress the selected image based on the specified quality."""
    quality = quality_entry.get()
    if quality.isdigit() and 1 <= int(quality) <= 100:
        img = Image.open(input_path)
        img.save(input_path.rsplit('.', 1)[0] + "_compressed.jpg", "JPEG", quality=int(quality))
        status_label.config(text="Image compressed.")
    else:
        status_label.config(text="Quality must be an integer between 1 and 100.")

def compress_file():
    if file_path:
        if file_type in ['.wav', '.flac', '.mp3']:
            compress_audio()
        elif file_type in ['.mp4', '.avi', '.mov']:
            output_video = filedialog.asksaveasfilename(
                title="Save Compressed Video As", 
                defaultextension=".mp4",
                filetypes=[("MP4 Files", "*.mp4")]
            )
            if output_video:
                # Get the user-defined bitrate
                user_bitrate = bitrate_entry.get() or '100k'  # Default bitrate if none provided
                
                status_var.set("Compressing video...")  # Update status message
                window.update_idletasks()  # Refresh the window
                
                compress_video(file_path, output_video, bitrate=user_bitrate)
                
                status_var.set("Video compression completed successfully.")  # Update status message
        elif file_type in ['.jpg','.jpeg','.png','.bmp']:
            compress_image(file_path)
        else:
            label.config(text="Unsupported file type. Please select an audio or video file.")
    else:
        label.config(text="Please select a file first.")

# Set up the Tkinter window
window = Tk()
window.title("Media Compressor")
window.geometry("720x480")
window.config(bg='light green')

file_path = None
file_type = None

# Create a StringVar for status messages
status_var = StringVar()

# Create buttons and labels
label = Label(window, text="MEDIA COMPRESSOR", font=('Serif', 16), bg='orange', fg='blue')
label.pack(pady=10)

browse_button = Button(window, text="Browse File", command=browse_file, font=('Arial', 12), bg='cyan', fg='blue')
browse_button.pack(pady=10)

Label(window, text="Enter Bitrate (e.g., 100k for video):", font=('Serif', 12), bg='yellow', fg='blue').pack()
bitrate_entry = Entry(window, fg='blue', bg='light grey')
bitrate_entry.pack(pady=5)

Label(window, text="Enter quality (1-100 for image):", bg='yellow', fg='blue', font='serif 12').pack(pady=10)
quality_entry = Entry(window, bg='light gray', fg='blue', font='serif 10')
quality_entry.pack(pady=5)

compress_button = Button(window, text="Compress", command=compress_file, font=('Arial', 12), bg='cyan', fg='blue')
compress_button.pack(pady=20)

status_label = Label(window, textvariable=status_var, fg='green', bg='light green')
status_label.pack(pady=10)
status_label = Label(window, text="",bg='light green', fg='blue', font='serif 10')
status_label.pack(pady=5)
# Start the GUI event loop
window.mainloop()
