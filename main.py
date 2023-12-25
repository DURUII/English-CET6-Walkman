import os
import re


def rename_files(path):
    mapping = {'一': '1', '二': '2', '三': '3'}
    for filename in os.listdir(path):
        if '考试' in filename:
            new_name = filename.replace('考试', '')
            os.rename(os.path.join(path, filename), os.path.join(path, new_name))

        if '第' not in filename:
            new_name = filename.replace('（', '（第').replace('）', '套）')
            for key, value in mapping.items():
                new_name = new_name.replace(key, value)
            os.rename(os.path.join(path, filename), os.path.join(path, new_name))


def process_file(input_path, output_path):
    for filename in os.listdir(input_path):
        if filename.endswith('.lrc'):
            with open(os.path.join(input_path, filename), encoding='GB18030') as fin, \
                    open(os.path.join(output_path, filename[:-4] + '.txt'), 'w') as fout:
                for line in fin:
                    line = re.sub(r'^.{10}', '', line).strip()
                    line = re.sub(r'<ch>.*', '', line)
                    if re.match(r'(Section|Conversation|Passage|Recording)', line):
                        fout.write('\n\n' + line + '\n')
                    elif re.match(r'(M:|W:)', line):
                        fout.write('\n' + line)
                    elif re.match(r'(College English Test Band Six|Directions)', line):
                        fout.write(line)
                    else:
                        prefix = '' if line.startswith(' ') else ' '
                        fout.write(prefix + line)


for path in ['./input/lrc', './input/mp3']:
    rename_files(path)

os.makedirs('./output', exist_ok=True)
process_file('./input/lrc', './output')
