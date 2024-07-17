instruction = 'You are a Code Translator. ' \
              'If the user enters Python code, you translate it into C#.' \
              'You do not do anything else. ' \
              'You do not translate any code that is not Python.'


def load_api_key():
    with open('api/api_key.txt', 'r') as file:
        api_key = file.read().strip()
    return api_key


def query_chatgpt(client, prompt):
    completion = client.chat.completions.create(
      model="ft:gpt-3.5-turbo-0125:personal::93j7mabM",
      messages=[
        {"role": "system", "content": instruction},
        {"role": "user", "content": prompt}
      ]
    )

    return completion
