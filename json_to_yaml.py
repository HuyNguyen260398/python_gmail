import json
import os
import sys
import yaml

def main():
    # Checking there is a file name
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        # Open the file
        if os.path.exists(json_file):
            with open(json_file, 'r') as source_file:
                source_content = json.load(source_file)
        else:
            print(f'ERROR: {json_file} not found')
            exit(1)
    # No file, no usage
    else:
        print('Usage: json_to_yaml.py <source_file.json> [target_file.yaml]')

    # Processing the conversion
    output = yaml.dump(source_content)
    yaml_file = sys.argv[2]

    # If no target file send to stdout
    if (len(sys.argv) < 3):
        print(output)
    # If the target file already exists, exit
    elif os.path.exists(yaml_file):
        print(f'ERROR: {yaml_file} already exists')
        exit(1)
    # Otherwise write to the specified file
    else:
        with open(yaml_file, 'w') as target_file:
            target_file.write(output)

if __name__ == '__main__':
    main()