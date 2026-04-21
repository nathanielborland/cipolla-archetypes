import openai
from pathlib import Path

with open('data/prompts/system_prompt.txt', 'r') as f:
    system_prompt = f.read()

with open('data/prompts/event_prompt.txt', 'r') as f:
    event_prompt = f.read()

def query_story(story_text: str, model="gpt-4.1"):
    prompt = f'{event_prompt}\n"""\n{story_text}\n"""'.strip()
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content.strip()

def query_all_stories(model="gpt-4.1"):
    tropes_path = Path('data/TV_Tropes')
    for story in tropes_path.glob('*'):
        Path(f"data/character_actions/{story.name}").mkdir(parents=True, exist_ok=True)
        for character in story.glob('*'):
            character_tropes = character.read_text()
            character_actions = query_story(character_tropes, model)
            Path(f"data/character_actions/{story.name}/{character.name}").write_text(character_actions)