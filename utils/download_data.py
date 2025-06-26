import pandas as pd
import time
import os

def download_and_create_csv():
    # Example data - replace this with your actual data downloading logic
    data = []
    for i in range(5):  # Example loop
        # Simulate data download
        time.sleep(1)
        data.append({
            'id': i,
            'value': i * 2,
            'timestamp': pd.Timestamp.now()
        })
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, 'data.csv')
    df.to_csv(csv_path, index=False)
    print(f"CSV file created at: {csv_path}")

if __name__ == "__main__":
    download_and_create_csv() 