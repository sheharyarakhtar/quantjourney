import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error

def generate_sample_data():
    """Generate sample time series data with multiple periodic components."""
    np.random.seed(42)
    t = np.linspace(0, 100, 1000)
    signal = np.sin(0.1 * t) + 0.5 * np.sin(0.3 * t) + 0.2 * np.random.randn(len(t))
    return t, signal

def split_data(t, signal, train_ratio=0.8):
    """Split data into train and test sets."""
    train_size = int(len(signal) * train_ratio)
    train_signal = signal[:train_size]
    test_signal = signal[train_size:]
    train_t = t[:train_size]
    test_t = t[train_size:]
    return train_t, test_t, train_signal, test_signal

def perform_fft(signal, t, N_components=10):
    """Perform FFT and keep strongest frequency components."""
    N = len(signal)
    yf = np.fft.fft(signal)
    xf = np.fft.fftfreq(N, d=t[1]-t[0])
    
    # Keep only the strongest frequency components
    sorted_indices = np.argsort(np.abs(yf))[::-1]  # Sort by magnitude, descending
    filtered_yf = np.zeros_like(yf)
    filtered_yf[sorted_indices[:N_components]] = yf[sorted_indices[:N_components]]
    
    return filtered_yf, sorted_indices, N

def predict_future(t, filtered_yf, sorted_indices, N_train, N_components):
    """Predict future values using learned frequency components."""
    N = len(t)
    yf_new = np.zeros(N, dtype=complex)
    
    # Copy the learned frequency components
    for i in range(N_components):
        idx = sorted_indices[i]
        # Handle both positive and negative frequencies
        if idx < N_train//2:
            # Positive frequency
            yf_new[idx] = filtered_yf[idx]
            # Negative frequency (mirror image)
            if idx > 0:  # Skip DC component (idx=0)
                yf_new[N-idx] = filtered_yf[N_train-idx]
    
    # Inverse FFT to get predictions
    return np.fft.ifft(yf_new).real

def plot_results(train_t, train_signal, train_reconstructed, 
                test_t, test_signal, test_predictions):
    """Plot the results of the Fourier Transform prediction."""
    plt.figure(figsize=(15, 6))
    plt.plot(train_t, train_signal, label='Training Data', alpha=0.5)
    plt.plot(train_t, train_reconstructed, label='Training Reconstruction', linestyle='--')
    plt.plot(test_t, test_signal, label='Test Data', alpha=0.5)
    plt.plot(test_t, test_predictions, label='Test Predictions', linestyle='--')
    plt.title('Fourier Transform-based Time Series Prediction')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    # Generate or load your data here
    t, signal = generate_sample_data()
    
    # Split data
    train_t, test_t, train_signal, test_signal = split_data(t, signal)
    
    # Perform FFT on training data
    filtered_yf, sorted_indices, N = perform_fft(train_signal, train_t)
    
    # Reconstruct training signal
    train_reconstructed = np.fft.ifft(filtered_yf).real
    
    # Make predictions for test set
    test_predictions = predict_future(test_t, filtered_yf, sorted_indices, N, N_components=10)
    
    # Calculate error metrics
    mse = mean_squared_error(test_signal, test_predictions)
    mae = mean_absolute_error(test_signal, test_predictions)
    
    print(f"Mean Squared Error: {mse:.4f}")
    print(f"Mean Absolute Error: {mae:.4f}")
    
    # Plot results
    plot_results(train_t, train_signal, train_reconstructed,
                test_t, test_signal, test_predictions)

if __name__ == "__main__":
    main() 