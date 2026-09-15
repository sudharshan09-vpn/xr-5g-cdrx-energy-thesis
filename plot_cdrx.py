import pandas as pd
import matplotlib.pyplot as plt

def plot_power_profile(csv_file, output_image):
    print(f"Loading C-DRX power data from {csv_file}...")
    
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: {csv_file} not found. Did the simulation run properly?")
        return

    # Create the figure
    plt.figure(figsize=(12, 6))
    
    # Use a 'step' plot to accurately represent instantaneous state changes
    plt.step(df['Time_s'], df['Current_mA'], where='post', color='#005293', linewidth=1.5, label='UE Current Draw')
    
    # Add reference lines for the Active and Idle states
    plt.axhline(y=313.0, color='red', linestyle='--', alpha=0.6, label='Active State (313 mA)')
    plt.axhline(y=11.4, color='green', linestyle='--', alpha=0.6, label='Idle State (11.4 mA)')
    
    # ==========================================
    # THE CRITICAL FIX: ZOOM IN
    # Limit the view to a 200-millisecond window
    # ==========================================
    plt.xlim(2.0, 2.2) 
    
    # Formatting for thesis publication
    plt.title('5G SA C-DRX Dynamic Power Profile for XR Traffic', fontsize=14, fontweight='bold')
    plt.xlabel('Simulation Time (Seconds)', fontsize=12)
    plt.ylabel('Current Draw (mA)', fontsize=12)
    
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(loc='center right')
    plt.tight_layout()
    
    # Save the high-res image
    plt.savefig(output_image, dpi=300)
    print(f"Graph successfully generated and saved to {output_image}!")

if __name__ == "__main__":
    plot_power_profile('parsed_power_data.csv', 'cdrx_power_profile.png')
