
import os
from dotenv import load_dotenv
from tools.search import get_references

load_dotenv()

def generate_bio(name, role, skills):

    print("\n🔍 Fetching references from Tavily...")
    references = get_references(role + " " + skills)

    extra = ""
    if references:
        extra = references[0][:150]

    short_bio = f"{name} is a {role} with skills in {skills}. {extra}"

    long_bio = f"""{name} is an experienced {role} specializing in {skills}.
With a strong commitment to excellence, {name} has worked on various projects demonstrating problem-solving abilities and technical expertise.
{extra}
Always eager to learn and grow, {name} aims to contribute effectively to any team or organization."""

    return short_bio, long_bio


def save_to_file(name, short_bio, long_bio):
    os.makedirs("outputs", exist_ok=True)

    filename = f"outputs/{name.replace(' ', '_').lower()}_bio.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("SHORT BIO:\n")
        f.write(short_bio + "\n\n")
        f.write("LONG BIO:\n")
        f.write(long_bio)

    print(f"\n✅ File saved successfully: {filename}")


def main():
    print("=== Professional Bio Generator (Tavily Version) ===\n")

    name = input("Enter your name: ")
    role = input("Enter your role: ")
    skills = input("Enter your skills (comma separated): ")

    short_bio, long_bio = generate_bio(name, role, skills)

    print("\n--- SHORT BIO ---")
    print(short_bio)

    print("\n--- LONG BIO ---")
    print(long_bio)

    save_to_file(name, short_bio, long_bio)


if __name__ == "__main__":
    main()