import pandas as pd

def translate_congestionzone(market, congestionzone):
    
    return congestionzone.strip() if congestionzone else None

def get_weatherzone(market, dc, congestionzone, zip_code, state, load_profile=None) -> str:
    try:
        map_df = pd.read_csv('mapping_weatherzone.csv', dtype=str)
        print("map df is ",map_df.head())
        config_df = pd.read_csv('config_weatherzone.csv', dtype=str)
        print("config df is ", config_df.head())

        v_zip = zip_code.strip()[:5]
        v_congestionzone = translate_congestionzone(market, congestionzone)
        print(v_zip, v_congestionzone)

        merged_df = pd.merge(
            map_df,
            config_df,
            on=['market', 'dc','map_value'],
            # left_on=['market', 'congestionzone'],
            # right_on=['market', 'congestionzone'],
            how='inner'
        )
        print("merged df is ", merged_df.head())

        filtered = merged_df[
            (merged_df['market'] == market) &
            (merged_df['dc'] == dc) &
            ((merged_df['congestionzone'].isna()) | (merged_df['congestionzone'] == v_congestionzone)) &
            ((merged_df['zip'].isna()) | (merged_df['zip'].str[:5] == v_zip)) &
            ((merged_df['state'].isna()) | (merged_df['state'] == state)) &
            ((merged_df['load_profile'].isna()) | (merged_df['load_profile'] == load_profile))
        ]

        top_match = filtered.sort_values(by='rank_value').head(1)

        if not top_match.empty:
            return top_match.iloc[0]['weatherzone']
        else:
            return None

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def main():
    market = 'ERCOT'
    dc = 'TNP'
    congestionzone = 'hi'
    zip_code = '76433'
    state = 'NORTH'
    load_profile = 'sasa'

    result = get_weatherzone(market, dc, congestionzone, zip_code, state, load_profile)

    if result:
        print(f"Weatherzone: {result}")
    else:
        print("No matching weather zone found.")

if __name__ == '__main__':
    main()
