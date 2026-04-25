# Simple Free Bio Generator (No API Required)

import os

def generate_bio(name, role, skills):
    short_bio = f"{name} is a {role} with skills in {skills}. Passionate about delivering high-quality work and continuously learning new technologies."

    long_bio = f"""{name} is an experienced {role} specializing in {skills}. 
With a strong commitment to excellence, {name} has worked on various projects demonstrating problem-solving abilities and technical expertise. 
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
    print("=== Professional Bio Generator (Free Version) ===\n")

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