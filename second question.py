import numpy as np
import pandas as pd

df = pd.read_excel("Summer Camp Task Data.xlsx", engine='openpyxl')

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

load_post_df = df.loc[df['action'] == "load_post_page"].copy()
click_post_df = df.loc[df['action'] == 'click_post'].copy()

print("Dark Query Percent:")

load_post_length = load_post_df.tokens.str.count(',|]')
load_post_length = load_post_length.reset_index(drop=True)
load_post_length = load_post_length.loc[load_post_length < 10]
print(len(load_post_length) / len(load_post_df))

print("Query Bounce Rate:")

load_source = load_post_df['source_event_id'].unique().tolist()
click_source = click_post_df['source_event_id'].unique().tolist()

# print(len(load_source) > len(click_source)) # Q1: load QUERIES should be more than CLICK queries but they are not.

print(len(set(load_source) - set(click_source)) / len(load_source))

load_post_df = load_post_df.sort_values(by=['source_event_id', 'post_page_offset'])
click_post_df = click_post_df.sort_values(by=['source_event_id'])
# print(load_post_df) # Q1:  Some device_ids are NaN
source_id_group_load = load_post_df.groupby('source_event_id', as_index=False).count()[['source_event_id', 'action']]
source_id_group_click = click_post_df.groupby('source_event_id', as_index=False).count()[['source_event_id', 'action']]
join = pd.merge(source_id_group_load, source_id_group_click, how="outer", on=["source_event_id"])
join['action_y'] = join['action_y'].fillna(0)
join['action_x'] = join['action_x'].fillna(0)
join['divide'] = join['action_y'] / (join['action_x'] * 24)
print('Rate of clicks per advertisement is:')
print(
    join[['source_event_id', 'divide']])  # Q1: inf means there are some clicks who does not have query which is strange
