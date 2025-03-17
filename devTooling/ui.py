import tkinter as tk
from tkinter import ttk
import scanPhidgets
import configuration_loader
import scanAudio
import scanWebcams
import scanMonitors
import os

class ConfigUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Configuration UI")
        self.geometry("600x400")
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        self.CL = configuration_loader.ConfigurationLoader(config_path)
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill='both')

        # Create tabs
        self.create_phidgets_tab(notebook)
        self.create_microphones_tab(notebook)
        self.create_speakers_tab(notebook)
        self.create_webcams_tab(notebook)
        self.create_monitors_tab(notebook)
        self.create_advanced_audio_tab(notebook)
        self.create_advanced_video_tab(notebook)

    def create_phidgets_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text='Phidgets')
        # Add widgets for phidgets configuration

        #Phidget 1 Serial #
        ttk.Label(frame, text="Phidget 1").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        ttk.Label(frame, text="Serial Number:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        phidget1_serial_entry = ttk.Entry(frame)
        phidget1_serial_entry.grid(row=1, column=1, padx=10, pady=5)
        phidget1_serial_entry.insert(0, self.CL.get_phidget_serial('phidget_1'))
        #Phidget 1 Channels #s
        ttk.Label(frame, text="Active Digital Channels:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        phidget1_channels_entry = ttk.Entry(frame)
        phidget1_channels_entry.grid(row=2, column=1, padx=10, pady=5)
        phidget1_channels_entry.insert(0, ','.join(map(str, self.CL.get_phidget_channels('phidget_1'))))
        ttk.Label(frame, text="(eg. 1,3,4)").grid(row=2, column=2, padx=10, pady=5, sticky='w')
        
        ttk.Label(frame, text="").grid(row=3, column=2, padx=10, pady=5, sticky='w')

        #Phidget 2 Serial #
        ttk.Label(frame, text="Phidget 2").grid(row=4, column=0, padx=10, pady=5, sticky='w')
        ttk.Label(frame, text="Serial Number:").grid(row=5, column=0, padx=10, pady=5, sticky='e')
        phidget2_serial_entry = ttk.Entry(frame)
        phidget2_serial_entry.grid(row=5, column=1, padx=10, pady=5)
        phidget2_serial_entry.insert(0, self.CL.get_phidget_serial('phidget_2'))
        #Phidget 2 Channels #s
        ttk.Label(frame, text="Active Digital Channels:").grid(row=6, column=0, padx=10, pady=5, sticky='e')
        phidget2_channels_entry = ttk.Entry(frame)
        phidget2_channels_entry.grid(row=6, column=1, padx=10, pady=5)
        phidget2_channels_entry.insert(0, ','.join(map(str, self.CL.get_phidget_channels('phidget_2'))))
        ttk.Label(frame, text="(eg. 1,3,4)").grid(row=6, column=2, padx=10, pady=5, sticky='w')
        
        # Add buttons below the existing widgets
        list_button = ttk.Button(frame, text="List Phidgets", command=self.list_phidgets)
        list_button.grid(row=7, column=0, padx=10, pady=10, sticky='w')

        identify_button = ttk.Button(frame, text="Identify Phidgets", command=self.identify_phidgets)
        identify_button.grid(row=7, column=1, padx=10, pady=10, sticky='w')

        # Add labels to display the output
        self.list_output_label = ttk.Label(frame, text="")
        self.list_output_label.grid(row=8, column=0, columnspan=3, padx=10, pady=5, sticky='w')

        self.identify_output_label = ttk.Label(frame, text="")
        self.identify_output_label.grid(row=9, column=0, columnspan=3, padx=10, pady=5, sticky='w')

    def list_phidgets(self):
        # Clear previous output
        self.list_output_label.config(text="")
        self.identify_output_label.config(text="")

        # Fetch and display the list of Phidget serial numbers
        serial_numbers = scanPhidgets.list_phidgets()
        if serial_numbers:
            output = "Found Phidget Serial Numbers:\n" + "\n".join(serial_numbers)
        else:
            output = "No Phidget devices found."
        self.list_output_label.config(text=output)

    def identify_phidgets(self):
        # Clear previous output
        self.list_output_label.config(text="")
        self.identify_output_label.config(text="Listening... Activate any button.")

        # Fetch and display the serial number of the Phidget that detected a change
        self.update_idletasks()  # Update the UI to show the "Listening..." message immediately
        serial_number = scanPhidgets.listen_phidgets()
        if serial_number:
            output = f"Phidget Detected Serial #: {serial_number}"
        else:
            output = "No change detected on any Phidget."
        self.identify_output_label.config(text=output)
        

    def create_microphones_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text='Microphones')
        # Add widgets for microphones configuration
        ttk.Label(frame, text="Microphone 1 Index:").grid(row=0, column=0, padx=10, pady=5)
        mic1_entry = ttk.Entry(frame)
        mic1_entry.grid(row=0, column=1, padx=10, pady=5)
        mic1_entry.insert(0, self.CL.get_microphone_index('microphone_1'))
        ttk.Label(frame, text="Microphone 2 Index:").grid(row=1, column=0, padx=10, pady=5)
        mic2_entry = ttk.Entry(frame)
        mic2_entry.grid(row=1, column=1, padx=10, pady=5)
        mic2_entry.insert(0, self.CL.get_microphone_index('microphone_2'))

        # Add buttons below the existing widgets
        list_button = ttk.Button(frame, text="Scan Audio", command=self.scan_audio_devices)
        list_button.grid(row=2, column=0, padx=10, pady=10, sticky='w')

      # Add a scrollable listbox to display the audio devices
        self.audio_devices_listbox = tk.Listbox(frame, height=10, width=50)
        self.audio_devices_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.audio_devices_listbox.yview)
        scrollbar.grid(row=3, column=2, sticky='ns')
        self.audio_devices_listbox.config(yscrollcommand=scrollbar.set)

    def scan_audio_devices(self):
        # Clear previous output
        self.audio_devices_listbox.delete(0, tk.END)

        # Fetch and display the list of audio devices
        devices = scanAudio.list_audio_devices()
        for idx, device in enumerate(devices):
            self.audio_devices_listbox.insert(tk.END, f"Device {idx} - {device}")

    def create_speakers_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text='Speakers')
        # Add widgets for speakers configuration
        ttk.Label(frame, text="Speaker 1 Index:").grid(row=0, column=0, padx=10, pady=5)
        speaker1_entry = ttk.Entry(frame)
        speaker1_entry.grid(row=0, column=1, padx=10, pady=5)
        speaker1_entry.insert(0, self.CL.get_speaker_index('speaker_1'))
        print (speaker1_entry.get())
        speaker1_play_button = ttk.Button(frame, text="Play Sound", command=lambda: scanAudio.play_test_tone(int(speaker1_entry.get()), int(self.sample_rate_entry.get())))
        speaker1_play_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')

        ttk.Label(frame, text="Speaker 2 Index:").grid(row=1, column=0, padx=10, pady=5)
        speaker2_entry = ttk.Entry(frame)
        speaker2_entry.grid(row=1, column=1, padx=10, pady=5)
        speaker2_entry.insert(0, self.CL.get_speaker_index('speaker_2'))
        speaker1_play_button = ttk.Button(frame, text="Play Sound", command=lambda: scanAudio.play_test_tone(int(speaker2_entry.get()), int(self.sample_rate_entry.get())))
        speaker1_play_button.grid(row=1, column=2, padx=10, pady=10, sticky='e')

        # Add buttons below the existing widgets
        list_button = ttk.Button(frame, text="Scan Audio", command=self.scan_speaker_audio_devices)
        list_button.grid(row=2, column=0, padx=10, pady=10, sticky='w')

      # Add a scrollable listbox to display the audio devices
        self.speaker_devices_listbox = tk.Listbox(frame, height=10, width=50)
        self.speaker_devices_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.speaker_devices_listbox.yview)
        scrollbar.grid(row=3, column=2, sticky='ns')
        self.speaker_devices_listbox.config(yscrollcommand=scrollbar.set)


    def scan_speaker_audio_devices(self):
        # Clear previous output
        self.speaker_devices_listbox.delete(0, tk.END)

        # Fetch and display the list of audio devices
        devices = scanAudio.list_audio_devices()
        for idx, device in enumerate(devices):
            self.speaker_devices_listbox.insert(tk.END, f"Device {idx} - {device}")



    def create_webcams_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text='Webcams')
        # Add widgets for webcams configuration
        ttk.Label(frame, text="Webcam 1 Index:").grid(row=0, column=0, padx=10, pady=5)
        webcam1_entry = ttk.Entry(frame)
        webcam1_entry.grid(row=0, column=1, padx=10, pady=5)
        webcam1_entry.insert(0, self.CL.get_webcam_index('webcam_1'))
        ttk.Label(frame, text="Webcam 2 Index:").grid(row=1, column=0, padx=10, pady=5)
        webcam2_entry = ttk.Entry(frame)
        webcam2_entry.grid(row=1, column=1, padx=10, pady=5)
        webcam2_entry.insert(0, self.CL.get_webcam_index('webcam_2'))

        # Add buttons below the existing widgets
        list_button = ttk.Button(frame, text="Identify Webcam", command=scanWebcams.identify_webcams)
        list_button.grid(row=2, column=0, padx=10, pady=10, sticky='w')

    def create_monitors_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text='Monitors')
        # Add widgets for monitors configuration
        ttk.Label(frame, text="Monitor 1 Index:").grid(row=0, column=0, padx=10, pady=5)
        monitor1_entry = ttk.Entry(frame)
        monitor1_entry.grid(row=0, column=1, padx=10, pady=5)
        monitor1_entry.insert(0, self.CL.get_monitor_index('monitor_1'))
        ttk.Label(frame, text="Monitor 2 Index:").grid(row=1, column=0, padx=10, pady=5)
        monitor2_entry = ttk.Entry(frame)
        monitor2_entry.grid(row=1, column=1, padx=10, pady=5)
        monitor2_entry.insert(0, self.CL.get_monitor_index('monitor_2'))

        # Add buttons below the existing widgets
        list_button = ttk.Button(frame, text="Identify Monitors", command=scanMonitors.scan_monitor_windows)
        list_button.grid(row=2, column=0, padx=10, pady=10, sticky='w')

    def create_advanced_audio_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text='Advanced Audio')
        # Add widgets for advanced audio properties configuration
        ttk.Label(frame, text="Sample Rate:").grid(row=0, column=0, padx=10, pady=5)
        self.sample_rate_entry = ttk.Entry(frame)
        self.sample_rate_entry.grid(row=0, column=1, padx=10, pady=5)
        self.sample_rate_entry.insert(0, self.CL.get_advanced_audio_options('sample_rate'))
        ttk.Label(frame, text="Audio Channels:").grid(row=1, column=0, padx=10, pady=5)
        audio_channels_entry = ttk.Entry(frame)
        audio_channels_entry.grid(row=1, column=1, padx=10, pady=5)
        audio_channels_entry.insert(0, self.CL.get_advanced_audio_options('audio_channels'))
        ttk.Label(frame, text="Chunk Size:").grid(row=2, column=0, padx=10, pady=5)
        chunk_size_entry = ttk.Entry(frame)
        chunk_size_entry.grid(row=2, column=1, padx=10, pady=5)
        chunk_size_entry.insert(0, self.CL.get_advanced_audio_options('chunk_size'))
        ttk.Label(frame, text="Audio Delay:").grid(row=3, column=0, padx=10, pady=5)
        audio_delay_entry = ttk.Entry(frame)
        audio_delay_entry.grid(row=3, column=1, padx=10, pady=5)
        audio_delay_entry.insert(0, self.CL.get_advanced_audio_options('audio_delay'))

    def create_advanced_video_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text='Advanced Video')
        # Add widgets for advanced video properties configuration
        ttk.Label(frame, text="Video Delay:").grid(row=0, column=0, padx=10, pady=5)
        video_delay_entry = ttk.Entry(frame)
        video_delay_entry.grid(row=0, column=1, padx=10, pady=5)
        video_delay_entry.insert(0, self.CL.get_advanced_video_options('video_delay'))

if __name__ == "__main__":
    app = ConfigUI()
    app.mainloop()
