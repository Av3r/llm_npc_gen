import json
import os
import re


def extract_json(text):
    try:
        start = text.index('{')
        end = text.rindex('}') + 1
        return text[start:end]
    except ValueError:
        return text

def load_used_names(path="data/names_generated.json"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                names = json.load(f)
                if isinstance(names, list):
                    return set(names)
            except json.JSONDecodeError:
                pass
    return set()

def save_used_names(names_set, path="data/names_generated.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(list(names_set), f, ensure_ascii=False, indent=2)

def generate_unique_name(client, story_text: str, used_names_path="data/names_generated.json") -> str:
    used_names = load_used_names(used_names_path)
    used_names_list_str = ', '.join(f'"{name}"' for name in used_names) if used_names else "none"

    prompt = f"""Based on the fantasy world described below, generate a unique and lore-appropriate character name.
Avoid generating any of the following already used names: {used_names_list_str}.
Return only the name, no extra text.

Story:
{story_text}

Name:"""

    for _ in range(10):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=10,
        )
        name = response.choices[0].message.content.strip()
        if name and name not in used_names:
            used_names.add(name)
            save_used_names(used_names, used_names_path)
            return name

    fallback_name = f"NPC_{len(used_names)+1}"
    used_names.add(fallback_name)
    save_used_names(used_names, used_names_path)
    return fallback_name

def generate_npc_attributes(client, story_text: str, name: str, profession_hint: str = None) -> dict:
    prompt_intro = f"Generate JSON character attributes (profession, faction, personality_traits) consistent with the story for the character named {name}."
    if profession_hint:
        prompt_intro = f"For a character with the profession '{profession_hint}', " + prompt_intro

    prompt = f"""{prompt_intro}

Story:
{story_text}

Return only JSON with keys: name, profession, personality_traits (list of strings).
Do not add any extra text."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=150,
    )

    content = response.choices[0].message.content.strip()

    content_clean = re.sub(r"^``````$", "", content, flags=re.DOTALL).strip()

    json_fragment = extract_json(content_clean)

    print("DEBUG - raw model response for NPC attributes:", content)

    try:
        json_data = json.loads(json_fragment)
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        json_data = {"name": name}

    return json_data