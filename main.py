import argparse
import json
from openai import OpenAI
from npc_gen.story_loader import load_story
from npc_gen.qna import ask_question
from npc_gen.npc_generator import generate_unique_name, generate_npc_attributes

OPENAI_API_KEY = ''

def interactive_mode(client, story_text):
    print("Interactive mode started. Enter commands or 'exit' to quit.")
    print("Available commands:")
    print(" story-understanding <question>")
    print(" generate-hero")
    print(" generate-details <name>\n")

    while True:
        try:
            user_input = input("> ").strip()
        except EOFError:
            print("\nExiting interactive mode.")
            break

        if user_input.lower() in ("exit"):
            break

        if user_input.startswith("story-understanding "):
            question = user_input[len("story-understanding "):].strip()
            if question:
                answer = ask_question(client, story_text, question)
                print("Answer:", answer)
            else:
                print("Provide a question after 'story-understanding'.")
        elif user_input == "generate-hero":
            name = generate_unique_name(client, story_text)
            print("Generated Hero Name:", name)
        elif user_input.startswith("generate-details "):
            name = user_input[len("generate-details "):].strip()
            if name:
                details = generate_npc_attributes(client, story_text, name)
                print("Character Details:")
                print(json.dumps({"name": name, **details}, indent=2, ensure_ascii=False))
            else:
                print("Provide a name after 'generate-details'.")
        else:
            print("Unknown command. Available commands:")
            print(" story-understanding <question>")
            print(" generate-hero")
            print(" generate-details <name>")
            print(" exit")

def parse_args():
    parser = argparse.ArgumentParser(description="NPC Generation System")
    parser.add_argument("--story-file", type=str, default="data/fantasy.md", help="Path to story file")
    parser.add_argument("--interactive", action="store_true", help="Start interactive mode")
    parser.add_argument("--story-understanding", type=str, help="Ask a question about the story")
    parser.add_argument("--generate-hero", action="store_true", help="Generate a unique hero name")
    parser.add_argument("--generate-details", type=str, metavar="NAME", help="Generate character details for given name")
    return parser.parse_args()

def main():

    args = parse_args()
    client = OpenAI(api_key=OPENAI_API_KEY)

    try:
        story_text = load_story(args.story_file)
        print(f"Story loaded from {args.story_file}")
    except FileNotFoundError:
        print(f"ERROR: Story file not found: {args.story_file}")
        return

    if args.interactive:
        interactive_mode(client, story_text)
    elif args.story_understanding:
        answer = ask_question(client, story_text, args.story_understanding)
        print("Answer:", answer)
    elif args.generate_hero:
        name = generate_unique_name(client, story_text)
        print("Generated Hero Name:", name)
    elif args.generate_details:
        details = generate_npc_attributes(client, story_text, args.generate_details)
        print("Character Details:")
        print(json.dumps({"name": args.generate_details, **details}, indent=2, ensure_ascii=False))
    else:
        print("Please provide --interactive or one of the following:")
        print(" --story-understanding \"Your question\"")
        print(" --generate-hero")
        print(" --generate-details NAME")
        print("Use --help for more info.")

if __name__ == "__main__":
    main()