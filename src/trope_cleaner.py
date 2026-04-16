import sys
import os

show_name = sys.argv[1]

to_remove = [
    '\nAdvertisement:\nTired of seeing ads? Subscribe!\n',
    'This example contains a TRIVIA entry. It should be moved to the TRIVIA tab.',
    'This example contains a YMMV entry. It should be moved to the YMMV tab.',
    'From the books...',
    'From the books!'
]
flagged_line_starts = [
    'Adapt',
    'Age Lift',
    'Ascended',
    'Demoted',
    '    '
]

with os.scandir(f'TV_Tropes_data/{show_name}') as entries:
    for entry in entries:
        if entry.is_file():
            with open(entry.path, 'r') as file:
                content = file.read()

            for text in to_remove:
                content = content.replace(text, '')

            for start in flagged_line_starts:
                content = content.replace(f'\n{start}', f'\nxxxx{start}')

            with open(entry.path, 'w') as file:
                file.write(content)