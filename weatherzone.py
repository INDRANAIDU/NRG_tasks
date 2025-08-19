import pandas as pd

def translate_weatherzone(market: str, weatherzone: str) -> str:
    v_weatherzone = None

    if weatherzone is not None:
        try:
            df_weatherzone = pd.read_csv('weatherzone.csv')
            print(df_weatherzone.head())

            match = df_weatherzone[
             (df_weatherzone['market'] == market) &
                (df_weatherzone['weatherzone'] == weatherzone)
            ]

            if not match.empty:
                v_weatherzone = match.iloc[0]['weatherzone']
            else:
                 df_translate_weatherzone = pd.read_csv('translate_weatherzone.csv')
                 

                # If not found, try translate_weatherzone table
                 trans_match = df_translate_weatherzone[
                    (df_translate_weatherzone['market'] == market) &
                    (df_translate_weatherzone['old_weatherzone'] == weatherzone)
                ]
                 print(trans_match.head())

                 if not trans_match.empty:
                    v_weatherzone = trans_match.iloc[0]['new_weatherzone']
                 else:
                    v_weatherzone = weatherzone

        except Exception as e:
            print(f"Error translating weather zone: {e}")
            raise e

    return v_weatherzone

if __name__ == "__main__":
    print(translate_weatherzone('NEISO', 'ZRI'))
