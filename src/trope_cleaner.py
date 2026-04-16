import sys

file_name = sys.argv[1]
to_remove = [
    '\nAdvertisement:\nTired of seeing ads? Subscribe!\n',
    'This example contains a TRIVIA entry. It should be moved to the TRIVIA tab.',
    'This example contains a YMMV entry. It should be moved to the YMMV tab.',
    'From the books...',
    'From the books!'
]

with open(f'TV_Tropes_data/{file_name}.txt', 'r') as file:
    content = file.read()

if len(content) > 0:
    for text in to_remove:
        content = content.replace(text, '')

    with open(f'TV_Tropes_data/{file_name}.txt', 'w') as file:
        file.write(content)
else:
    print('file not found')