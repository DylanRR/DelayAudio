import subprocess
import re

def list_phidgets():
    try:
        # Run the lsusb command and capture the output
        result = subprocess.run(['lsusb', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Check for errors
        if result.returncode != 0:
            print(f"Error running lsusb: {result.stderr}")
            return
        
        # Filter the output for lines containing "Phidgets Inc."
        phidget_lines = result.stdout.split('\n')
        
        # Extract and print serial numbers
        serial_numbers = []
        capture_next = False
        for line in phidget_lines:
            if 'Phidgets Inc.' in line:
                capture_next = True
            elif capture_next and 'iSerial' in line:
                match = re.search(r'iSerial\s+\d+\s+(\d+)', line)
                if match:
                    serial_numbers.append(match.group(1))
                capture_next = False
        
        # Print the found serial numbers with additional text
        if serial_numbers:
            print("Found Phidget Serial Numbers:")
            for idx, serial in enumerate(serial_numbers, start=1):
                print(f"Phidget {idx}: {serial}")
        else:
            print("No Phidget devices found.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    list_phidgets()