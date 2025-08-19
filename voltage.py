import pandas as pd

def translate_voltage(market: str, dc: str, voltage: str) -> str:
    v_voltage = None

    if voltage is not None:
        try:
            df = pd.read_csv('translate_voltage.csv')  
            print(df.head()) 
            sql = df[
                (df['market'] == market) &
                (df['dc'] == dc) &
                (df['old_voltage'] == voltage)
            ]

            if not sql.empty:
                v_voltage = sql.iloc[0]['new_voltage']
            else:
                v_voltage = voltage
        except Exception as e:
            print(f"Error translating voltage: {e}")
            return None

    return v_voltage
if __name__ == "__main__":
    print(translate_voltage('PJM', 'PP', '23000 VOLT DELTA'))