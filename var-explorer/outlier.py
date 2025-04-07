import pandas as pd

def load_csv_file(filename):
    try:
        return pd.read_csv(filename, sep=';')
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        exit(1)
    except Exception as e:
        print(f"Error loading file: {e}")
        exit(1)

def find_outlier_pairs(df):
    relevant_columns = ['Symbol', 'BidPrice', 'AskPrice', 'VaR_1_Lot', 'SectorName', 'IndustryName']
    df_filtered = df[relevant_columns].copy()  # Create a copy of the filtered DataFrame
    
    # Calculate average price
    df_filtered['AveragePrice'] = (df_filtered['BidPrice'] + df_filtered['AskPrice']) / 2
    
    outlier_pairs = []
    max_price = df_filtered['AveragePrice'].max()
    current_threshold = 0
    
    while current_threshold <= max_price:
        threshold_df = df_filtered[(df_filtered['AveragePrice'] >= current_threshold) & (df_filtered['AveragePrice'] < current_threshold + 10)]
        
        if not threshold_df.empty:
            var_mean = threshold_df['VaR_1_Lot'].mean()
            var_std = threshold_df['VaR_1_Lot'].std()
            
            for index, row in threshold_df.iterrows():
                if (row['VaR_1_Lot'] < var_mean - 0.5 * var_std): # Loosened the parameters
                    outlier_pairs.append((row['IndustryName'], row['Symbol']))
        
        current_threshold += 10
        
    return outlier_pairs

def main():
    filename = input("Enter the CSV file name: ")
    
    df = load_csv_file(filename)
    outlier_pairs = find_outlier_pairs(df)
    
    if outlier_pairs:
        print('Outlier pairs:')
        for pair in outlier_pairs:
            print(f'Industry: {pair[0]}, Symbol: {pair[1]}')
    else:
        print("No outlier pairs found.")

if __name__ == "__main__":
    main()

