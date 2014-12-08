# abl.util

This is a grab-bag of little functions that have been useful at one time or another.

Many of them can probably be found in other libraries.

This project should probably have a better focus, and a more specific name, to reflect that focus.

## Release a new version

abl.util uses versioneer to manage version numbers.

When you are developing on your branch, running sdist will create
tarballs with versions like:

    2.2.15-3-g123456

When you actually want a new real, actual, numbered version, do this:

* Make sure all tests pass
* Make a pull request, get it reviewed, and merged back to master
* checkout master and pull so you are looking at the HEAD of master
* check which tags already exist with `git tag`
* `git tag <your_new_version_number>`
* `git push --tags`

Now when you run sdist the version number will be whatever you
specified.

**Running `git push --tags` is super important. If you don't, nobody
else will be able to figure out where your version came from,
version numbers will get weird, and we will be sad.**

Finally:

* Change version in `requirements.txt` in affected packages

## License

abl.util is distributed under the MIT license (see LICENSE).
