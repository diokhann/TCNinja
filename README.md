# TCNinja
 A Python script analising Terms and Conditions



This Python script analyzes terms and conditions using OpenAI's GPT models. It takes a text file or a URL containing terms and conditions as input, and it provides a summary, highlights illegal statements, and identifies disadvantages to the user agreeing to these terms and conditions.

## Prerequisites

To run this script, you need:

1. Python 3.6 or later
2. The following Python libraries:
    - requests
    - beautifulsoup4
    - openai

You can install these libraries using pip:

```
pip install requests beautifulsoup4 openai
```

## Setup

1. Create a `config.json` file in the project root directory with the following format:

```json
{
    "OPENAI_API_KEY": "your_openai_api_key_here",
    "DEFAULT_MODEL": "gpt-3.5-turbo"
}
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

2. (Optional) If you want to use a different GPT model, change the value of the `DEFAULT_MODEL` field in the `config.json` file.

## Usage

To run the script, use one of the following commands:

- To analyze a text file:

```
python analyze_terms.py --file path/to/terms_and_conditions.txt
```

- To analyze a web page:

```
python analyze_terms.py --url=https://example.com/terms_and_conditions
```

The script will display the analysis result on the screen and save it to a file named `output.txt`.

## License

This project is licensed under the GNU General Public License v3.0.

## Contributions and Suggestions

Thank you for your interest in this project! I encourage collaboration and welcome any suggestions or improvements. Please feel free to submit issues or pull requests.

