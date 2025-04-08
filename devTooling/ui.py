import tkinter as tk
from tkinter import ttk
import scanPhidgets
import scanAudio
import scanWebcams
import scanMonitors
import scanSampleRates
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import configuration_loader_v2 as configuration_loader

class ConfigUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Configuration UI")
        self.geometry("600x400")
        self.config_path = configuration_loader.get_config_path()
        self.CL = configuration_loader.ConfigurationLoader(self.config_path)
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
        self.phidget1_serial_entry = ttk.Entry(frame)
        self.phidget1_serial_entry.grid(row=1, column=1, padx=10, pady=5)
        self.phidget1_serial_entry.insert(0, self.CL.get_config_value('phidgets', ['phidget_1', 'serial_number']))
        #Phidget 1 Channels #s
        ttk.Label(frame, text="Active Digital Channels:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.phidget1_channels_entry = ttk.Entry(frame)
        self.phidget1_channels_entry.grid(row=2, column=1, padx=10, pady=5)
        self.phidget1_channels_entry.insert(0, ','.join(map(str, self.CL.get_config_value('phidgets', ['phidget_1', 'active_channels']))))
        ttk.Label(frame, text="(eg. 1,3,4)").grid(row=2, column=2, padx=10, pady=5, sticky='w')
        
        ttk.Label(frame, text="").grid(row=3, column=2, padx=10, pady=5, sticky='w')

        #Phidget 2 Serial #
        ttk.Label(frame, text="Phidget 2").grid(row=4, column=0, padx=10, pady=5, sticky='w')
        ttk.Label(frame, text="Serial Number:").grid(row=5, column=0, padx=10, pady=5, sticky='e')
        self.phidget2_serial_entry = ttk.Entry(frame)
        self.phidget2_serial_entry.grid(row=5, column=1, padx=10, pady=5)
        self.phidget2_serial_entry.insert(0, self.CL.get_config_value('phidgets', ['phidget_2', 'serial_number']))
        #Phidget 2 Channels #s
        ttk.Label(frame, text="Active Digital Channels:").grid(row=6, column=0, padx=10, pady=5, sticky='e')
        self.phidget2_channels_entry = ttk.Entry(frame)
        self.phidget2_channels_entry.grid(row=6, column=1, padx=10, pady=5)
        self.phidget2_channels_entry.insert(0, ','.join(map(str, self.CL.get_config_value('phidgets', ['phidget_2', 'active_channels']))))
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
        
        save_btn = ttk.Button(frame, text="Save", command=self.save_phidget_config)
        save_btn.grid(row=7, column=2, padx=10, pady=10, sticky='w')

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
        
    def save_phidget_config(self):
        ph1_serial = self.phidget1_serial_entry.get()
        if not self.CL.set_config_value('phidgets', ['phidget_1', 'serial_number'], ph1_serial):
            print("Failed to save Phidget 1 serial number.")
        else:
            print("Phidget 1 serial number saved successfully.")
            
        ph1_channels = self.phidget1_channels_entry.get()
        if (configuration_loader.is_valid_int_list_string(ph1_channels)):
            ph1_list = configuration_loader.string_to_int_list(ph1_channels)
            if not self.CL.set_config_value('phidgets', ['phidget_1', 'active_channels'], ph1_list):
                print("Failed to save Phidget 1 channels.")
            else:
                print("Phidget 1 channels saved successfully.")
        else:
            print("Phidget 1 invalid channels string.")
                
        ph2_serial = self.phidget2_serial_entry.get()
        if not self.CL.set_config_value('phidgets', ['phidget_2', 'serial_number'], ph2_serial):
            print("Failed to save Phidget 2 serial number.")
        else:
            print("Phidget 2 serial number saved successfully.")
            
        ph2_channels = self.phidget2_channels_entry.get()
        if (configuration_loader.is_valid_int_list_string(ph2_channels)):
            ph2_list = configuration_loader.string_to_int_list(ph2_channels)
            if not self.CL.set_config_value('phidgets', ['phidget_2', 'active_channels'], ph2_list):
                print("Failed to save Phidget 2 channels.")
            else:
                print("Phidget 2 channels saved successfully.")
        else:
            print("Phidget 2 invalid channels string.")
        
        

    def create_microphones_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text='Microphones')
        # Add widgets for microphones configuration
        ttk.Label(frame, text="Microphone 1 Serial Number:").grid(row=0, column=0, padx=10, pady=5)
        self.mic1_entry = ttk.Entry(frame)
        self.mic1_entry.grid(row=0, column=1, padx=10, pady=5)
        self.mic1_entry.insert(0, self.CL.get_config_value('microphones', ['microphone_1', 'serial_number']))
        ttk.Label(frame, text="Microphone 2 Serial Number:").grid(row=1, column=0, padx=10, pady=5)
        self.mic2_entry = ttk.Entry(frame)
        self.mic2_entry.grid(row=1, column=1, padx=10, pady=5)
        self.mic2_entry.insert(0, self.CL.get_config_value('microphones', ['microphone_2', 'serial_number']))

        # Add buttons below the existing widgets
        list_button = ttk.Button(frame, text="Scan Audio", command=self.scan_audio_devices)
        list_button.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        
        # Save Button
        save_btn = ttk.Button(frame, text="Save", command=self.save_microphone_config)
        save_btn.grid(row=2, column=1, padx=10, pady=10, sticky='w')

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
            
    def save_microphone_config(self):
        mic_1_serial = self.mic1_entry.get()
        if not self.CL.set_config_value('microphones', ['microphone_1', 'serial_number'], mic_1_serial):
            print("Failed to save Microphone 1 serial.")
        else:
            print("Microphone 1 serial saved successfully.")
        
        mic_2_index = self.mic2_entry.get()
        if not self.CL.set_config_value('microphones', ['microphone_2', 'index'], mic_2_index):
            print("Failed to save Microphone 2 index.")
        else:
            print("Microphone 2 index saved successfully.")

    def create_speakers_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text='Speakers')
        # Add widgets for speakers configuration
        ttk.Label(frame, text="Speaker 1 Device Name:").grid(row=0, column=0, padx=10, pady=5)
        self.speaker1_entry = ttk.Entry(frame)
        self.speaker1_entry.grid(row=0, column=1, padx=10, pady=5)
        self.speaker1_entry.insert(0, self.CL.get_config_value('speakers', ['speaker_1', 'device_name']))
        speaker1_play_button = ttk.Button(frame, text="Play Sound", command=lambda: scanAudio.play_test_tone(int(self.speaker1_entry.get()), int(self.sample_rate_entry.get())))
        speaker1_play_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')

        ttk.Label(frame, text="Speaker 2 Device Name:").grid(row=1, column=0, padx=10, pady=5)
        self.speaker2_entry = ttk.Entry(frame)
        self.speaker2_entry.grid(row=1, column=1, padx=10, pady=5)
        self.speaker2_entry.insert(0, self.CL.get_config_value('speakers', ['speaker_2', 'device_name']))
        speaker1_play_button = ttk.Button(frame, text="Play Sound", command=lambda: scanAudio.play_test_tone(int(self.speaker2_entry.get()), int(self.sample_rate_entry.get())))
        speaker1_play_button.grid(row=1, column=2, padx=10, pady=10, sticky='e')

        # Add buttons below the existing widgets
        list_button = ttk.Button(frame, text="Scan Audio", command=self.scan_speaker_audio_devices)
        list_button.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        
        # Save Button
        save_btn = ttk.Button(frame, text="Save", command=self.save_speaker_config)
        save_btn.grid(row=2, column=1, padx=10, pady=10, sticky='w')

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

    def save_speaker_config(self):
        spk1_serial = self.speaker1_entry.get()
        if not self.CL.set_config_value('speakers', ['speaker_1', 'serial_number'], spk1_serial):
            print("Failed to save Speaker 1 serial number.")
        else:
            print("Speaker 1 serial number saved successfully.")
            
        spk2_serial = self.speaker2_entry.get()
        if not self.CL.set_config_value('speakers', ['speaker_2', 'serial_number'], spk2_serial):
            print("Failed to save Speaker 2 index.")
        else:
            print("Speaker 2 index saved successfully.")


    def create_webcams_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text='Webcams')
        # Add widgets for webcams configuration
        ttk.Label(frame, text="Webcam 1 serial number:").grid(row=0, column=0, padx=10, pady=5)
        self.webcam1_entry = ttk.Entry(frame)
        self.webcam1_entry.grid(row=0, column=1, padx=10, pady=5)
        self.webcam1_entry.insert(0, self.CL.get_config_value('webcams', ['webcam_1', 'serial_number']))
        ttk.Label(frame, text="Webcam 2 serial number:").grid(row=1, column=0, padx=10, pady=5)
        self.webcam2_entry = ttk.Entry(frame)
        self.webcam2_entry.grid(row=1, column=1, padx=10, pady=5)
        self.webcam2_entry.insert(0, self.CL.get_config_value('webcams', ['webcam_2', 'serial_number']))

        # Add buttons below the existing widgets
        list_button = ttk.Button(frame, text="Identify Webcam", command=scanWebcams.identify_webcams)
        list_button.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        
        # Save Button
        save_btn = ttk.Button(frame, text="Save", command=self.save_webcam_config)
        save_btn.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    def save_webcam_config(self):
        web1_serial = self.webcam1_entry.get()
        if not self.CL.set_config_value('webcams', ['webcam_1', 'serial_number'], web1_serial):
            print("Failed to save Webcam 1 serial numebr.")
        else:
            print("Webcam 1 serial number saved successfully.")
            
        web2_serial = self.webcam2_entry.get()
        if not self.CL.set_config_value('webcams', ['webcam_2', 'serial_number'], web2_serial):
            print("Failed to save Webcam 2 serial number.")
        else:
            print("Webcam 2 serial number saved successfully.")

    def create_monitors_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text='Monitors')
        # Add widgets for monitors configuration
        ttk.Label(frame, text="Monitor 1 Index:").grid(row=0, column=0, padx=10, pady=5)
        self.monitor1_entry = ttk.Entry(frame)
        self.monitor1_entry.grid(row=0, column=1, padx=10, pady=5)
        self.monitor1_entry.insert(0, self.CL.get_config_value('monitors', ['monitor_1', 'index']))
        ttk.Label(frame, text="Monitor 2 Index:").grid(row=1, column=0, padx=10, pady=5)
        self.monitor2_entry = ttk.Entry(frame)
        self.monitor2_entry.grid(row=1, column=1, padx=10, pady=5)
        self.monitor2_entry.insert(0, self.CL.get_config_value('monitors', ['monitor_2', 'index']))

        # Add buttons below the existing widgets
        list_button = ttk.Button(frame, text="Identify Monitors", command=scanMonitors.scan_monitor_windows)
        list_button.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        
        # Save Button
        save_btn = ttk.Button(frame, text="Save", command=self.save_monitor_config)
        save_btn.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
    def save_monitor_config(self):
        mon1_index = self.monitor1_entry.get()
        if not self.CL.set_config_value('monitors', ['monitor_1', 'index'], mon1_index):
            print("Failed to save Monitor 1 index.")
        else:
            print("Monitor 1 index saved successfully.")
            
        mon2_index = self.monitor2_entry.get()
        if not self.CL.set_config_value('monitors', ['monitor_2', 'index'], mon2_index):
            print("Failed to save Monitor 2 index.")
        else:
            print("Monitor 2 index saved successfully.")

    def create_advanced_audio_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text='Advanced Audio')
        # Add widgets for advanced audio properties configuration
        ttk.Label(frame, text="Sample Rate (Default 48000):").grid(row=0, column=0, padx=1, pady=5, sticky='e')
        self.sample_rate_entry = ttk.Entry(frame)
        self.sample_rate_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.sample_rate_entry.insert(0, self.CL.get_config_value('advanced_audio_properties', ['sample_rate']))

        # Add buttons below the existing widgets
        sample_rate_scan_btn = ttk.Button(frame, text="Scan Sample Rates", command=self.scan_sample_rate)
        sample_rate_scan_btn.grid(row=0, column=2, padx=1, pady=10, sticky='e')

        ttk.Label(frame, text="Audio Channels:").grid(row=1, column=0, padx=1, pady=5, sticky='e')
        self.audio_channels_entry = ttk.Entry(frame)
        self.audio_channels_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.audio_channels_entry.insert(0, self.CL.get_config_value('advanced_audio_properties', ['audio_channels']))
        self.audio_channels_entry.config(state='readonly')
        ttk.Label(frame, text="Chunk Size:").grid(row=2, column=0, padx=1, pady=5, sticky='e')
        self.chunk_size_entry = ttk.Entry(frame)
        self.chunk_size_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.chunk_size_entry.insert(0, self.CL.get_config_value('advanced_audio_properties', ['chunk_size']))
        self.chunk_size_entry.config(state='readonly')
        ttk.Label(frame, text="Audio Delay:").grid(row=3, column=0, padx=1, pady=5, sticky='e')
        self.audio_delay_entry = ttk.Entry(frame)
        self.audio_delay_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.audio_delay_entry.insert(0, self.CL.get_config_value('advanced_audio_properties', ['audio_delay']))
        ttk.Label(frame, text="(Milliseconds)").grid(row=3, column=2, padx=1, pady=5, sticky='w')
        
        #Save Button
        save_btn = ttk.Button(frame, text="Save", command=self.save_audio_config)
        save_btn.grid(row=1, column=2, padx=1, pady=10)

        # Add a scrollable listbox to display the audio devices
        self.sample_rates_listbox = tk.Listbox(frame, height=10, width=50)
        self.sample_rates_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.sample_rates_listbox.yview)
        scrollbar.grid(row=4, column=2, sticky='ns')
        self.sample_rates_listbox.config(yscrollcommand=scrollbar.set)

    def scan_sample_rate(self):
        # Clear previous output
        self.sample_rates_listbox.delete(0, tk.END)

        # Fetch and display the list of supported sample rates
        devices = scanSampleRates.list_supported_sample_rates()
        for device in devices:
            self.sample_rates_listbox.insert(tk.END, f"Device {device['device_number']}: {device['device_info']['name']}")
            for rate in device['supported_sample_rates']:
                self.sample_rates_listbox.insert(tk.END, f"  Supported sample rate: {rate}")
                
    def save_audio_config(self):
        sample_rate = self.sample_rate_entry.get()
        if not self.CL.set_config_value('advanced_audio_properties', ['sample_rate'], sample_rate):
            print("Failed to save Sample Rate.")
        else:
            print("Sample Rate saved successfully.")
            
        audio_channels = self.audio_channels_entry.get()
        if not self.CL.set_config_value('advanced_audio_properties', ['audio_channels'], audio_channels):
            print("Failed to save Audio Channels.")
        else:
            print("Audio Channels saved successfully.")
            
        chunk_size = self.chunk_size_entry.get()
        if not self.CL.set_config_value('advanced_audio_properties', ['chunk_size'], chunk_size):
            print("Failed to save Chunk Size.")
        else:
            print("Chunk Size saved successfully.")
            
        audio_delay = self.audio_delay_entry.get()
        if not self.CL.set_config_value('advanced_audio_properties', ['audio_delay'], audio_delay):
            print("Failed to save Audio Delay.")
        else:
            print("Audio Delay saved successfully.")
      

    def create_advanced_video_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text='Advanced Video')
        # Add widgets for advanced video properties configuration
        ttk.Label(frame, text="Video Delay:").grid(row=0, column=0, padx=10, pady=5)
        self.video_delay_entry = ttk.Entry(frame)
        self.video_delay_entry.grid(row=0, column=1, padx=10, pady=5)
        self.video_delay_entry.insert(0, self.CL.get_config_value('advanced_video_properties', ['video_delay']))
        ttk.Label(frame, text="(Milliseconds)").grid(row=0, column=2, padx=10, pady=5, sticky='w')
        #Save Button
        save_btn = ttk.Button(frame, text="Save", command=self.save_video_config)
        save_btn.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        
    def save_video_config(self):
        video_delay = self.video_delay_entry.get()
        if not self.CL.set_config_value('advanced_video_properties', ['video_delay'], video_delay):
            print("Failed to save Video Delay.")
        else:
            print("Video Delay saved successfully.")

if __name__ == "__main__":
    app = ConfigUI()
    app.mainloop()
