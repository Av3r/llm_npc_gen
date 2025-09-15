
def ask_question(client, story_text: str, question: str) -> str:
    prompt = f"""Below is the description of the fantasy game world. Based only on this, answer the question.

Story:
{story_text}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()