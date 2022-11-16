from pathlib import Path
import sys


IGNORE_LINE_CHARS = ['\\', '%']

def wrap_line(line, wrap_length=75):
    lines_wrapped = []
    start_i = 0
    end_i = wrap_length
    while len(line) - start_i > wrap_length:
        end_i = start_i + wrap_length
        exact_length = line[start_i : end_i]
        end_i = start_i + exact_length.rfind(' ')
        wrapped_at_space = line[start_i : end_i]
        lines_wrapped.append(wrapped_at_space)
        start_i = end_i + 1
    lines_wrapped.append(line[start_i :])
    return lines_wrapped

def wrap_lines_in_file(file_path, new_file_path, wrap_length=75):
    """Wrap lines of a file to a certain length. File must end with a newline
    character/two blank lines to capture last paragraph.

    Parameters
    ----------
    file_path : str or Path
        File for which lines will be wrapped.
    new_file_path : str or Path
        Path to save new file with wrapped lines.
    wrap_length : int
        Length at which lines will be wrapped.
    """
    file_path = Path(file_path)
    new_file_path = Path(new_file_path)
    with (
        open(file_path, 'r', encoding='utf-8', errors='ignore') as f,
        # open(file_path_wrap, 'a', encoding='utf-8', errors='ignore') as f_wrap
    ):
        prev_line = ''
        full_lines = []
        lines = f.readlines()
        print()
        print('Original file:')
        print(file_path.resolve())
        print(f'{len(lines)} lines')
        for line in lines:
            if line[0] in IGNORE_LINE_CHARS:
                if prev_line != '':
                    full_lines.append(prev_line[:-1])
                full_lines.append(line[:-1])
                prev_line = ''
            elif len(line) > 1:
                # If line starts with space, slice the line to exclude space.
                if line[0] == ' ':
                    line = line[1:]
                # If line ends with space (before newline char),
                # slice the line to exclude space and add newline back on.
                elif line[-2] == ' ':
                    line = line[:-2] + '\n'
                # Add current line (replacing newline character with space)
                prev_line = prev_line + line[:-1] + ' '
            elif len(line) == 1:
                # Append line with previous line without space at end
                full_lines.append(prev_line[:-1])
                prev_line = ''
    print()
    print(f'Number of collected lines before wrapping: {len(full_lines)}')
    # Remove contents of file (if existing) before appending wrapped lines
    if new_file_path.exists():
        open(new_file_path, 'w', encoding='utf-8', errors='ignore').close()
    # Open new file and iterate through full lines to wrap into sublines
    with open(
        new_file_path, 'a', encoding='utf-8', errors='ignore'
    ) as f_wrap:
        for full_line in full_lines:
            sublines = wrap_line(full_line, wrap_length=wrap_length)
            for subline in sublines:
                # Write full line without space at end of line
                f_wrap.write(subline + '\n')
            if subline[0] not in IGNORE_LINE_CHARS:
                f_wrap.write('\n')
    # Open file again to read number of final lines
    with open(
        new_file_path, 'r', encoding='utf-8', errors='ignore'
    ) as f_wrap:
        print()
        print('Wrapped file:')
        print(new_file_path.resolve())
        lines = f_wrap.readlines()
        print(f'{len(lines)} lines')

def handle_args(args):
    try:
        if args[0] == '-i':
            if len(args) == 2:
                input_path = Path(args[1])
                new_file = (
                        f'{input_path.parent}/'
                        f'{input_path.stem}-wrapped{input_path.suffix}')
            elif len(args) == 4 and args[2] == '-o':
                if args[3] == 'overwrite':
                    new_file = args[1]
                else:
                    new_file = args[3]
            else:
                print('Error: An option must be passed with each flag.')
                print('An option must be specified with each flag.')
                print('Only flags "-i" and "-o" supported.')
        else:
            print('Error: Input passed without flag.')
            print(
                    'Specify input file with "-i"'
                    ' and output filename suffix with "-o"')
    except IndexError:
        print('Input file must be passed after "-i" flag.')
    finally:
        wrap_lines_in_file(args[1], new_file)

if __name__ == '__main__':
    # wrap_lines_in_file(sys.argv[-1])
    handle_args(sys.argv[1:])

