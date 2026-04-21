import sys
from pathlib import Path

show_name = sys.argv[1]
character_names = sys.argv[2]

folder_path = Path(f'data/TV_Tropes/{show_name.replace(' ', '_')}')
file_names = character_names.replace(' ', '_').split('\n')

folder_path.mkdir()
for name in file_names:
    file_path = folder_path / (name + '.txt')
    file_path.touch()