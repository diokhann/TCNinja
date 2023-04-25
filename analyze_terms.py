import argparse
import json
import sys

import openai
import requests
from bs4 import BeautifulSoup


def read_config():
    with open("config.json", "r") as file:
        config = json.load(file)
    return config["OPENAI_API_KEY"], config["DEFAULT_MODEL"]


OPENAI_API_KEY, DEFAULT_MODEL = read_config()
openai.api_key = OPENAI_API_KEY


def read_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content


def get_web_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.get_text()
    return content


def analyze(content, prompt_template):
    content_chunks = split_content(content, 4096 - 100)  # reserve 100 tokens for the prompt and other messages
    results = []

    for chunk in content_chunks:
        prompt = f"{prompt_template}\n\n{chunk}"

        print(f"Sending the following query to OpenAI API:\n{prompt}\n")

        completion = openai.ChatCompletion.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system",
                 "content": "Analyze the given terms and conditions, summarize them, highlight illegal statements, "
                            "and identify disadvantages to the user."},
                {"role": "user", "content": chunk}
            ]
        )

        output = completion.choices[0].message.content.strip()
        results.append(output)

    return "\n\n---\n\n".join(results)


def split_content(content, max_length):
    tokens = content.split(" ")
    chunks = []
    current_chunk = []

    for token in tokens:
        if len(" ".join(current_chunk)) + len(token) + 1 > max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

        current_chunk.append(token)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def main():
    parser = argparse.ArgumentParser(description="Analyze terms and conditions using OpenAI API.")
    parser.add_argument("--file", type=str, help="Path to the text file containing terms and conditions.")
    parser.add_argument("--url", type=str, help="URL of the webpage containing terms and conditions.")
    args = parser.parse_args()

    if not args.file and not args.url:
        print("You must provide either a file path or a URL.")
        sys.exit(1)

    prompt_template = "You are a world class lawyer, an expert in civil and financial law. You are going to analyse " \
                      "the below Terms and Conditions and assess them. Please respond in following format: Summary: (" \
                      "list all disadvantages to the user, legal liability, legal loopholes and illegal statements " \
                      "in a simple, understandable form); Suggestion: (based on the analysis, suggest what is the " \
                      "level of risk for a user agreeing to these terms and conditions). The text:"

    if args.file:
        content = read_file(args.file)
    else:
        content = get_web_content(args.url)

    output = analyze(content, prompt_template)

    print("Analysis result:")
    print(output)

    with open("output.txt", "w") as file:
        file.write(output)
    print("\nSaved output to 'output.txt'")


if __name__ == "__main__":
    main()
