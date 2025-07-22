import pandas as pd

# Prompt user for input CSV file name
input_file = input("Enter the input CSV file name (including .csv extension): ")

try:
    # Read the CSV file with semicolon delimiter and specify encoding
    df = pd.read_csv(input_file, sep=';', encoding='latin1')
    
    # Filter for TradeMode == 3
    filtered_df = df[df['TradeMode'] == 3]
    
    # Check if any records were found
    if filtered_df.empty:
        print("No symbols found with TradeMode = 3 (Close Only)")
    else:
        # Print symbols with TradeMode 3
        print("Trade Mode 'Close Only' detected on the following symbols:")
        for symbol in filtered_df['Symbol']:
            print(symbol)
        
        # Export filtered results to a new CSV file
        output_file = 'filtered_trademode_3.csv'
        filtered_df.to_csv(output_file, sep=';', index=False, encoding='utf-8')
        print(f"\nFiltered symbols exported to {output_file}")
        
except FileNotFoundError:
    print(f"Error: The file '{input_file}' was not found.")
except UnicodeDecodeError as e:
    print(f"Encoding error: {str(e)}. Try a different encoding (e.g., 'cp1252' or 'utf-16').")
except Exception as e:
    print(f"An error occurred: {str(e)}")
