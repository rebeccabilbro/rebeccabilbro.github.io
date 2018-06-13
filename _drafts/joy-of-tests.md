# Joy of Tests: A Gentle Introduction for Data Scientists

What the post will be about. My background is not software engineering, and I'm a late convert to testing. They seem somehow both mysterious and really tedious. I wonder if other YB contributors feel the same way -- it would be a shame for anyone to not contribute to Yellowbrick because they feel intimidated about testing, so I'm writing this post to serve as a bridge to anyone who finds themselves in the same boat.

## Why test?

Testing is not one of the tenets of data science. Many people enter data science by way of research. Research code generally doesn't have (or need) tests. Writing tests is a software engineering practice.

Tradeoffs between test-driven development and hypothesis-driven development.

### Unit testing, integration testing, functional testing

- unit tests: test whether a function or class method works as expected
- integration tests: test whether functions or classes interact with each other as expected
- functional tests: test the software end-to-end to measure how well it meets the specifications

## Why PyTest?

- what you get with unittests from the standard library
- PyTest basics
- why not Nose? Last year we discovered that [Nose wasn't being maintained anymore](https://pypi.org/project/nose/1.3.7/#history) and started converting all the tests to PyTest.

## Yellowbrick

What is Yellowbrick, what are are visualizers, what do they do.

Get the testing requirements - note that these differ from the `yellowbrick` package requirements. The Makefile uses the `pytest` runner and testing suite as well as the `coverage` library, so make sure you have those dependencies installed!

```bash
$ pip install -r tests/requirements.txt
```

Now run all the tests:

```bash
$ pytest tests
```

The test package mirrors the yellowbrick package in structure and also contains several helper methods and base functionality. To add a test to your visualizer, find the corresponding file to add the test case, or create a new test file in the same place you added your code.


### Getting started

The primary test should simply to test your visualizer from end to end and make sure that no exceptions occur.

Peculiarities about testing visualizers...

### Testing with a lot of data

Testing scikit-learn models with real data can consume a lot of memory!
About the `DatasetMixin` helper

Requires requests.py to fetch data from our Amazon S3 account.

### Image comparison tests

Visual tests are notoriously difficult to create — how do you test a visualization or figure?
About the `VisualTestCase` helper

For writing image-based comparison tests, we have adapted `matplotlib`’s image comparison test utility into an easy-to-use assert method: `self.assert_images_similar(visualizer)`

The main consideration is that you must specify the "baseline", or expected, image in the `tests/baseline_images/` folder structure.

For example, create your unittest located in `tests/test_regressor/test_myvisualizer.py` as follows:

```python
from tests.base import VisualTestCase
...
    def test_my_visualizer_output(self):
        ...
        visualizer = MyVisualizer()
        visualizer.fit(X)
        visualizer.poof()
        self.assert_images_similar(visualizer)
```

The first time this test is run, there will be no baseline image to compare against, so the test will fail. Copy the output images (in this case `tests/actual_images/test_regressor/test_myvisualizer/test_my_visualizer_output.png`) to the correct subdirectory of `baseline_images` tree in the source directory (in this case `tests/baseline_images/test_regressor/test_myvisualizer/test_my_visualizer_output.png`). Put this new file under source code revision control (with git add). When rerunning the tests, they should now pass.

We also have a helper script, `tests/images.py` to clean up and manage baseline images automatically. It is run using the `python -m` command to execute a module as main, and it takes as an argument the path to your test file. To copy the figures as above:

```bash
$ python -m tests.images tests/test_regressor/test_myvisualizer.py
```

This will move all related test images from `actual_images` to `baseline_images` on your behalf (note you’ll have had to run the tests at least once to generate the images). You can also clean up images from both actual and baseline as follows:

```bash
$ python -m tests.images -C tests/test_regressor/test_myvisualizer.py
```

This is useful particularly if you’re stuck trying to get an image comparison to work. For more information on the images helper script, use `python -m tests.images --help`.

### Testing Text

- There are currently three `PosTagVisualizer`, `FreqDistVisualizer`, `TSNEVisualizer`. Coverage for `TSNEVisualizer` is pretty good, but is currently minimal for the other two.

## Automated Testing

- Why? There are operating systems other than yours.
- Compare/contrast: Travis, CircleCi, Jenkins
- Helpful features & limitations to consider

## Testing with Mock, Tox, and Docker

## Other Readings
