# AI_NPC
Project to showcase use of ai model in making dynamic and interactive AI NPC

Please make sure that modules from requirement.txt are installed
pip install -r requirements.txt

and insert you own model api key in model.py file
openai.api_key = "your-api-key-here"

https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key to get your openai api key

usage rate for gpt 3.5 turbo
$3 / 1M input tokens
$6 / 1M output tokens

A token is approximately 1 word. For example:

Sending a 50-word prompt and receiving a 100-word response = 150 tokens.
At the rates above, this would cost just $0.0009.
Testing should cost less than a dollar in most cases

to start
python main.py
