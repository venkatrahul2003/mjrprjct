import serial
import numpy as np
from scipy.stats import zscore
import time

# Open serial connection to Arduino
ser = serial.Serial('/dev/cu.usbserial-10', 115200)  # Change 'COM3' to the appropriate port

# Initialize variables
heart_rates = []

def calculate_stress(heart_rates):
    # Remove outliers using z-score method
    heart_rates_zscore = zscore(heart_rates)
    threshold = 3
    heart_rates_filtered = [heart_rates[i] for i in range(len(heart_rates)) if abs(heart_rates_zscore[i]) < threshold]

    # Calculate HRV-based stress level (example calculation)
    hrv_stress = np.std(heart_rates_filtered)  # Example: using standard deviation as stress indicator

    return hrv_stress

try:
    start_time = time.time()
    while True:
        # Read heart rate data from Arduino
        heart_rate_str = ser.readline().decode().strip()
        heart_rate = int(heart_rate_str)
        print (heart_rate)
        
        # Append heart rate to list
        heart_rates.append(heart_rate)

        # Check if 30 seconds have elapsed
        if time.time() - start_time >= 30:
            # Process heart rate data and calculate stress level
            stress_level = calculate_stress(heart_rates)
            pecent = ((stress_level-0.5)/3.25)*100
            print("Stress level:", stress_level, pecent)
            time.sleep(2)
            # Reset variables for next calculation
            heart_rates = []
            start_time = time.time()  # Reset timer

except KeyboardInterrupt:
    ser.close()  # Close serial connection on keyboard interrupt
