import yaml
import json
from api.gpt_client import load_api_key, instruction
from openai import OpenAI


def format_data(source_code, target_code):
    return {
        "messages": [
            {"role": "system", "content": instruction},
            {"role": "user", "content": source_code},
            {"role": "assistant", "content": target_code}
        ]
    }


def save_error_case(save_file, bad_prompt):
    error_message = 'Please load valid Python code.'
    error_case = format_data(bad_prompt, error_message)
    json.dump(error_case, save_file)
    save_file.write('\n')


def save_training_error_cases(file_path):
    with open(file_path, 'a') as file:
        save_error_case(file, 'Hi')
        save_error_case(file, '')
        save_error_case(file, 'asdfdsfsdfdsfsdaf')
        save_error_case(file, '#include <string>')
        save_error_case(file, 'who are you')
        save_error_case(file, 'buy bitcoin')
        save_error_case(file, 'System.out.println(\"This is java code\")')
        save_error_case(file, '<html><\html>')


def save_validation_error_cases(file_path):
    with open(file_path, 'a') as file:
        save_error_case(file, 'Validation')
        save_error_case(file, 'rubbish')
        save_error_case(file, 'asdfdsdsfsfsfsdfsdfsdfsdfsdsfsdaf')
        save_error_case(file, '#include <efcd>')
        save_error_case(file, 'who am i')
        save_error_case(file, 'buy litcoint')
        save_error_case(file, 'System.out.println(\"Hi\")')
        save_error_case(file, '<html>afsfasdffas<\html>')


def save_code(code_pairs, file_path):
    with open(file_path, 'w') as file:
        for index, (python_code, csharp_code) in enumerate(code_pairs):
            formatted_python_to_csharp = format_data(python_code, csharp_code)
            json.dump(formatted_python_to_csharp, file)
            file.write('\n')


def extract_code(file_path):
    code_pairs = []
    try:
        with open(file_path, 'r') as file:
            loaded_pairs = yaml.safe_load(file)

            for pair in loaded_pairs:
                python_code = pair.get('python', 'Python code not found')
                csharp_code = pair.get('csharp', 'C# code not found')

                code_pairs.append((python_code, csharp_code))
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML file: {exc}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return code_pairs


def fine_tune():
    api_key = load_api_key()
    client = OpenAI(api_key=api_key)

    training_file = client.files.create(
      file=open(training_data, "rb"),
      purpose="fine-tune"
    )

    validation_file = client.files.create(
      file=open(validation_data, "rb"),
      purpose="fine-tune"
    )

    client.fine_tuning.jobs.create(
      training_file=training_file.id,
      validation_file=validation_file.id,
      model="gpt-3.5-turbo"
    )


training_code = 'data/training_code.yaml'
training_data = 'data/training_data.jsonl'

validation_code = 'data/validation_code.yaml'
validation_data = 'data/validation_data.jsonl'

training_pairs = extract_code(training_code)
validation_pairs = extract_code(validation_code)

#save_code(training_pairs, training_data)
#save_training_error_cases(training_data)
#save_code(validation_pairs, validation_data)
#save_validation_error_cases(validation_data)

save_code(validation_pairs, training_data)

fine_tune()

