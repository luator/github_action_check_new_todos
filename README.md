# GitHub Action "Check New TODOs"

Parses between two given git revisions for `TODO`s (or any other label) that
were added or modified in the diff.

To be used as a check for pull requests.  The idea is that this check does not
trigger on already existing `TODO`s but only those that are newly added.


## Inputs

### `label`

The label that is searched for.  Default: `TODO`.

### `base_ref`

The base commit used for the diff.  Default: `origin/master`.

### `head_ref`

The head commit used for the diff.  Default: `HEAD`.


## Example usage

Example workflow checking for "FIXME" in pull requests.

    on: pull_request

    jobs:
      fixmes:
        name: FIXME check
        runs-on: ubuntu-latest
        steps:
        - uses: actions/checkout@v2
        - run: git fetch origin ${GITHUB_BASE_REF}
        - name: Check for FIXMEs
          uses: luator/github_action_check_new_todos@master
          with:
              label: FIXME
              base_ref: origin/${{ github.base_ref }}

Note that `actions/checkout` only fetches the feature branch of the pull
request, not the target branch.  To be able to get the diff, the target branch
(given by `${GITHUB_BASE_REF}`/`github.base_ref`) needs to be fetched
explicitly.
