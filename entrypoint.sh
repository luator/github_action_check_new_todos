#!/bin/sh

label=$1
base_ref=$2
head_ref=$3

# copy the problem matcher to the workspace, so it is accessible outside of the
# container
# See: https://github.com/actions/toolkit/issues/205#issuecomment-557647948
cp /git-diff-todos-problem-matcher.json "${HOME}/"
echo "::add-matcher::${HOME}/git-diff-todos-problem-matcher.json"

echo "Parse diff ${base_ref}..${head_ref} for ${label}."
echo "-----------------------------------------------------------"

python3 /git-diff-todos.py --parsable-output -o ${base_ref} -n ${head_ref} -l ${label}
result=$?

exit ${result}
