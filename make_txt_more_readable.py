import re
import sys

replacements = {
    r'\b(\d{1,2}:)*\d{2}\b': '',   # time
    r'\n+'              : ' ',     # new line
    r'\s+'              : ' ',     # white space
    r'\.\s+'            : '.\n\n'  # phrase separator
    }

def combine_sentences(input_text, sentences_per_group=5):
    sentences = re.split(r'\n\n', input_text)

    grouped_sentences = [sentences[i:i + sentences_per_group] for i in range(0, len(sentences), sentences_per_group)]

    result_text = '\n\n'.join([' '.join(group) for group in grouped_sentences])

    return result_text

def to_md(input_text):
    return  "# Text\n\n" + input_text

def to_md_code(input_text):
    sentences = re.split(r'\n\n', input_text)

    result_text = "# Text\n\n```text\n" + '\n```\n\n```text\n'.join(sentences) + "\n```\n"

    return result_text

def filename_to_md(input_text):
    return re.sub(r'txt', r'md', input_text)

def filename_to_more_readable(input_text):
    filename_split_beg = input_text.split('.\\', 1)
    filename_split_end = filename_split_beg[-1].rsplit('.', 1)
    filename_split_end[0] = re.sub(r'txt', r'more readable txt', filename_split_end[0])
    filename_split_beg[-1] = ' more readable.'.join(filename_split_end)
    return '.\\'.join(filename_split_beg)


def process_file(input_filename, output_filename, replacements):
    try:
        with open(input_filename, 'r', encoding='utf-8') as input_file:
            output_text = input_file.read()

            for pattern, replacement in replacements.items():
                output_text = re.sub(pattern, replacement, output_text)

        output_text = to_md(combine_sentences(output_text.strip(r'\s')))

        with open(output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write(output_text)

        print(f"The substitutions were performed successfully. The result is written to the file: \"{output_filename}\"")

    except FileNotFoundError:
        print(f"Error: File \"{input_filename}\" not found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py input_filename")
        sys.exit(1)

    input_filename = sys.argv[1]

    output_filename = filename_to_md(input_filename)

    if output_filename == input_filename:
        output_filename = "temp"

    process_file(input_filename, output_filename, replacements)