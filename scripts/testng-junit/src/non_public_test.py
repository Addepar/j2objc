import os
import sys
import re

def find_tests(file_name, content):
    content_new = content
    new_lines = []
    content_iter = iter(content_new.split("\n"))
    for line in content_iter:
        if ("@Test" in line or "@ParameterizedTest" in line) and "@TestInstance" not in line:
            left_spaces = " " * (len(line) - len(line.lstrip()))
            # while line.startswith(left_spaces + "@") or line.startswith(left_spaces + "//"):
            while "void" not in line:
                new_lines.append(line)
                line = next(content_iter)
            # new_lines.append(line)
            # if "@ParameterizedTest" in line:
            #   line = next(content_iter)
            #   new_lines.append(line)
            # line = next(content_iter)

            if " public " not in line:
                print(f"{file_name}: \n \t {line}")
                if "private " in line:
                    line = line.replace("private ", "public ")
                elif "protected " in line:
                    line = line.replace("protected ", "public ")
                else:
                    line = left_spaces + "public " + line.strip()
            new_lines.append(line)
        else:
            new_lines.append(line)

    content_new = "\n".join(new_lines)

    return content_new

def migrate_tests(test_dir):
    test_files = []
    for path, directory, files in os.walk(test_dir):
        if directory == "buck_out":
            continue
        for file in files:
            if file.endswith(".java"):
                test_files.append(os.path.join(path, file))

    for file_name in test_files:
        with open(file_name, "r") as f:
            content = f.read()
            if "@Test" in content or "@ParameterizedTest" in content:
                print("Converting ", file_name)
                content_new = find_tests(file_name, content)
                if content_new != content:
                    print("Converting ", file_name)
                    with open(file_name, "w") as fn:
                        fn.write(content_new)

def main():
    if len(sys.argv) == 1:
        print("usage: {} <directory_to_migrate>".format(sys.argv[0]))
        sys.exit(1)

    test_dir = sys.argv[1]
    migrate_tests(test_dir)


if __name__ == "__main__":
    sys.exit(main())
