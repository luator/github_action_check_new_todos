# GitHub Action "New TODOs"

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
        - uses: actions/checkout@v3
        - name: Check for FIXMEs
          uses: luator/github_action_check_new_todos@v2
          with:
              label: FIXME
              base_ref: origin/${{ github.base_ref }}
