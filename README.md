# abl.util

This is a grab-bag of little functions that have been useful at one time or another.

Many of them can probably be found in other libraries.

This project should probably have a better focus, and a more specific name, to reflect that focus.

## Set up a Working Environment

To set up your working environment, run:

```bash
pip install -e '.[test]'
```

## Release a New Version

You can build a new version by running:

```bash
python -m build
```

When developing on your branch, running the build will create tarballs with versions like:

```text
3.6.dev1+g13691ed.d20250211
```

To release a new official version, follow these steps:

1. Ensure all tests pass.
2. Make a pull request, get it reviewed, and merge it back to `master`.
3. Checkout `master` and pull the latest changes.
4. Check existing tags with:

```bash
git tag
```

5. Tag the new version:

```bash
git tag <your_new_version_number>
```

6. Push the tags:

```bash
git push --tags
```

Now when you run build the version number will be whatever you specified.

⚠️ Running `git push --tags` is crucial. If you don't, nobody else will be able to figure out where your version came from, version numbers will get weird, and we will be sad.
