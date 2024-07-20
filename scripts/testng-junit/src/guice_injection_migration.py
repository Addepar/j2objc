import os
import sys
import re


def migration_injection(content):
    # Add import statements
    new_imports = [
        "import org.junit.jupiter.api.Test;",
        "import com.addepar.infra.library.testing.extention.GuiceInjectionExtension;",
    ]
    if "org.junit.jupiter.api.extension.ExtendWith" not in content:
        new_imports.append("import org.junit.jupiter.api.extension.ExtendWith;")
    content_new = re.sub(
        "import org.junit.jupiter.api.Test;",
        "\n".join(new_imports),
        content,
    )

    # Remove @SuppressWarnings("EmptyCatchBlock")
    content_new = re.sub(
        r"  @SuppressWarnings\(\"EmptyCatchBlock\"\)\s*\n", "", content_new
    )

    content_new = re.sub(
        r"try {\n\s*injector\.injectMembers\(this\);\n\s*} catch \(RuntimeException e\) {\n\s*}",
        "injector.injectMembers(this);",
        content_new,
    )

    # Add @ExtendWith(GuiceInjectionExtension.class)
    new_lines = []
    content_iter = iter(content_new.split("\n"))
    for line in content_iter:
        if "public class" in line or "public final class" in line:
            left_spaces = " " * (len(line) - len(line.lstrip()))
            new_lines.append(left_spaces + "@ExtendWith(GuiceInjectionExtension.class)")
        new_lines.append(line)
    content_new = "\n".join(new_lines)

    return content_new


def migrate_tests(test_dir):
    test_files = []
    for path, directory, files in os.walk(test_dir):
        # print("p", path)
        # print("f", files)
        for file in files:
            if file.endswith(".java"):
                test_files.append(os.path.join(path, file))

    for file_name in test_files:
        # print("f ", file_name)
        with open(file_name, "r") as f:
            content = f.read()
            if (
                "@BeforeAll" in content
                and "injector.injectMembers" in content
                and not "GuiceInjectionExtension" in content
            ):
                print("Converting ", file_name)
                content_new = migration_injection(content)
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
