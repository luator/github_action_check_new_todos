#!/usr/bin/python3
"""Parse git diff for added TODOs and print them nicely."""
import argparse
import collections
import re
import sys

import git  # pip install gitpython


def any_in(a, b):
    """Checks if 'a in b' is true for any element of a."""
    return any(x in b for x in a)


def main():
    arg_parser = argparse.ArgumentParser(description=__doc__)
    arg_parser.add_argument(
        "--repo",
        type=str,
        default=".",
        help="Path to the root of the git repository.  Default: '%(default)s'.",
    )
    arg_parser.add_argument(
        "--old",
        "-o",
        type=str,
        default="origin/master",
        help="Old commit.  Default: '%(default)s'",
    )
    arg_parser.add_argument(
        "--new",
        "-n",
        type=str,
        default="HEAD",
        help="New commit.  Default: '%(default)s'",
    )
    arg_parser.add_argument(
        "--label",
        "-l",
        type=str,
        nargs="+",
        default=("TODO", "FIXME"),
        help="List of labels that is searched for.  Default: %(default)s",
    )
    arg_parser.add_argument(
        "--parsable-output",
        action="store_true",
        help="Produce output that is easier to parse by another script.",
    )
    args = arg_parser.parse_args()

    repo = git.Repo(args.repo)
    commit = repo.commit(args.old)
    diff = commit.diff(args.new, create_patch=True)

    matches = collections.defaultdict(dict)

    for file_diff in diff:
        line_num = 0
        for b_line in file_diff.diff.splitlines():
            line = b_line.decode("utf-8")
            line_num += 1
            if line.startswith("+") and any_in(args.label, line):
                # remove the "+" and leading whitespaces
                line = line[1:].strip()

                matches[file_diff.b_path][line_num] = line
            elif line.startswith("@@"):
                # "@@ -199,8 +208,9 @@" --> 208
                # "---@@ -0,0 +1 @@" --> 1  // single line files
                match = re.search(r"@@ -\d+,\d+ \+(\d+)(,\d+)? @@", line)
                # Start with offset of -1 because the extracted number refers
                # to the line following this one.
                line_num = int(match.group(1)) - 1

    if args.parsable_output:
        for filename, lines in matches.items():
            for line_num, text in lines.items():
                print("%s:%d: %s" % (filename, line_num, text))
    else:
        for filename, lines in matches.items():
            print()
            print(filename)
            for line_num, text in lines.items():
                print("\t%d: %s" % (line_num, text))

    if matches:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
