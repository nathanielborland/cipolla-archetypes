import pandas as pd
from pathlib import Path

chars_df = pd.read_csv('data/rated_characters.csv')
arch_raw_A = pd.read_csv('data/archetypes/data_raw_A.txt', sep=' ').to_numpy()
arch_svd_U = pd.read_csv('data/archetypes/data_archetype_space_U.txt', sep=' ').to_numpy()
archetype_space = arch_svd_U.T @ arch_raw_A

def build_characters_table():
    archetype_characters = pd.read_csv('data/archetypes/data_characters.tsv', sep='\t')
    rated_character_names = []
    tropes_path = Path('data/TV_Tropes')
    for story in tropes_path.glob('*'):
        for character in story.glob('*'):
            rated_character_names.append(character.name[:-4].replace('_', ' '))
    rated_characters = archetype_characters[archetype_characters['character'].isin(rated_character_names)]
    rated_characters['story'] = rated_characters['character/story'].str.split('/').str[-1]
    rated_characters = rated_characters.drop(['character in latex', 'character/story in latex', 'character/story', 'card url'], axis=1)
    
    rated_characters['average_self_help'] = None
    rated_characters['average_other_help'] = None
    rated_characters['num_actions'] = None
    rated_characters['fool_hero'] = None
    rated_characters['angel_demon'] = None
    for _, row in rated_characters.iterrows():
        act_df = get_character_actions(row['character'])
        most_common_actor = act_df['Actor'].mode()[0]
        act_df = act_df[act_df['Actor'].str.contains(most_common_actor)]
        raw_averages = act_df[['Self-impact score (S)', 'Other-impact score (O)']].to_numpy().mean(axis=0)
        averages = (raw_averages-50)/50
        
        rated_characters.loc[rated_characters['character'] == row['character'], 'average_self_help'] = averages[0]
        rated_characters.loc[rated_characters['character'] == row['character'], 'average_other_help'] = averages[1]
        rated_characters.loc[rated_characters['character'] == row['character'], 'num_actions'] = act_df.shape[0]
        
        archetypes = get_character_archetypes(row['character'])
        rated_characters.loc[rated_characters['character'] == row['character'], 'fool_hero'] = archetypes[0]
        rated_characters.loc[rated_characters['character'] == row['character'], 'angel_demon'] = archetypes[1]
    
    rated_characters.to_csv('data/rated_characters.csv', index=False)

def build_normalized_characters_table():
    archetype_characters = pd.read_csv('data/archetypes/data_characters.tsv', sep='\t')
    character_rows = []
    output_path = Path('data/TV_Tropes')
    for story in output_path.glob('*'):
        max_story_help_magnitude = 0
        story_character_actions = {}
        for character in story.glob('*'):
            char_name = character.name[:-4].replace('_', ' ')
            act_df = get_character_actions(char_name)
            act_df = act_df[act_df['Actor'].str.contains(act_df['Actor'].mode()[0])]
            raw_scores = act_df[['Self-impact score (S)', 'Other-impact score (O)']]
            scores = (raw_scores-50)/50
            story_character_actions[char_name] = scores
            max_story_help_magnitude = max(max_story_help_magnitude, scores.abs().max().max())
        
        story_name = story.name.replace('_', ' ')
        for character_name, actions in story_character_actions.items():
            if max_story_help_magnitude != 0:
                actions = actions * (1/max_story_help_magnitude)
            avg_helpfulness = actions.to_numpy().mean(axis=0)
            character_index = archetype_characters[archetype_characters['character'] == character_name]['index'].values[0]
            num_actions = actions.shape[0]

            archetypes = get_character_archetypes(character_name)
            fool_hero = archetypes[0]
            angel_demon = archetypes[1]

            character_rows.append({
                'index': character_index,
                'character': character_name,
                'story': story_name,
                'average_self_help': avg_helpfulness[0],
                'average_other_help': avg_helpfulness[1],
                'num_actions': num_actions,
                'fool_hero': fool_hero,
                'angel_demon': angel_demon
            })
    
    pd.DataFrame(character_rows).to_csv('data/normalized_rated_characters.csv', index=False)

def get_character_actions(name:str):
    return pd.read_csv(f'output/TV_Tropes/{chars_df.loc[chars_df['character'] == name, 'story'].values[0].replace(' ', '_')}/{name.replace(' ', '_')}.tsv', sep='\t')

def get_character_traits(name:str):
    return arch_raw_A[:,chars_df.loc[chars_df['character'] == name, 'index']-1].reshape(-1)

def get_character_archetypes(name:str):
    return archetype_space[:,chars_df.loc[chars_df['character'] == name, 'index']-1].reshape(-1)/6