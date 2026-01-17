# Git Branching & Merging Example

The purpose of this assignment is to give you additional practice working with Git branches.

Git branches allow us to have parallel histories, versions of files that we haven't yet decided we'd like to be part of our work's history.

TODO: explanation or use old notes?

## Part 1. Introduction

`pay_gap.py` is a small program that analyzes pay equality using the provided `earnings.csv`.

If you run the program you'll see a table of the top gender pay gaps represented in the data.

You can also run `uv run pytest` to check that the program is returning the
expected results.

The program uses the built-in `csv` module, where many might prefer `pandas` or `polars`. The code is clear enough, but we're curious about performance.

Let's write a small performance test using Python's built-in `timeit` module:

```
# perftest.py
import timeit
from pay_gap import get_top_pay_disparities


if __name__ == "__main__":
    number = 100
    
    elapsed = timeit.timeit(
        lambda: get_top_pay_disparities(10),
        number=number
    )
    
    avg_time = elapsed / number
    
    print(f"Total time:   {elapsed:.4f} seconds")
    print(f"Average time: {avg_time:.4f} seconds")
    print(f"Per call:     {avg_time * 1000:.2f} ms")
```

Add the above to a file named `perftest.py`, and run it with `uv run python perftest.py`.

Take note of the output, we'll want to remember these numbers in the next step.

## Part 2. Exploring the Git History

TODO: how to visualize?

Let's visualize the graph using: `git log --graph --oneline`

Our history begins at the bottom, with the most recent commit on top:

- `` documentation for part 2
- `9f49e22` documentation for part 1
- `3dcc3d9` initial commit"

This is the history of our current branch, `main`.

Type `git branch` to see a list of branches, you'll see that there are two others: `pandas` and `polars`.

To see the entire history, let's add `--all` to our `git log`

`git log --graph --oneline --all`

```
TODO: final  
```

Here we see that there are commits that split off the main trunk:

- `92b25a5` **(polars)** polars implementation
- `de76c5e` add polars to project

The `(polars)` indicates where the head of the branch currently sits.

## Part 3. Perfomance Testing Pandas

- `git switch -c <branchname>` - creates a new branch
- `git switch <branchname>` - switches to an existing branch

Let's use `git switch` to move over to the latest commit on the `pandas` branch.

Take a look at `pay_gap.py` and you'll notice that it now uses `pandas` instead of `csv`.

To see the difference between this and the main branch, you can run `git diff main pay_gap.py`, you'll see that the entire function was rewritten, while the beginning & end of the file are the same.

Once you've done that, run `uv run pytest` to ensure that the code works.

**It shouldn't!**

`pandas` is not yet installed, `uv add pandas`, and then run `uv run pytest` again.

The same tests are passing with different code, now let's test performance!

`uv run python perftest.py` won't work, because `perftest.py` isn't in our directory any more!

We didn't lose any work though, `perftest.py` is still sitting back on your `main` branch.

If we want to bring in the latest changes from `main` we need to do a `git merge`.

`git merge main` will ask `git` to bring over all commits from `main` to the current branch.

This command should say (TODO), a fast-forward merge means that it could apply the commits directly.

Now we can run `uv run python perftest.py`!

Note these numbers and compare them to the numbers from before.
You should see a modest speed improvement over `csv`. `pandas` more efficient internal data structures that give it a speed advantage over equivaent python code in most cases.

Before proceeding, you'll want to make another commit on this branch for the changes you made to `pyproject.toml` and `uv.lock` when installing pandas.

What does your graph look like now?

`git log --graph --oneline --all`

## Part 4. Merging to main

Happy that we saw a speedup, we see no reason not to merge the `pandas` branch back into main.

To do that, you'll need to `git switch` back to main and `git merge` the `pandas` branch into it.

TODO: output

## Part 5. `polars`

Polars is a newer dataframe library which is faster & has an API that is reminiscent of SQL that many people prefer.

We already have an implementation on the `polars` branch. Let's follow a similar process:

1. `git switch polars` to switch to the branch, look at `pay_gap.py` to confirm it now uses `polars`.
2. `uv run pytest` to ensure it works.
3. Before we can run the performance tests we need to bring over `perftest.py` again. This time however, the merge is going to be more complicated.

In Part 4, the only differences between the destination & source branch was the `perftest.py`, but now `main` has changed!

When we try to merge the branches we are notified that there are TODO conflicts.

TODO: conflict resolution

Now that we've resolved the conflicts, we can run `uv run python perftest.py`, and we should see that things are indeed far faster!

## Part 6. Merge to `main`

Now that we're convinced that `polars` is the right call for this work, we want to merge things back to main.

Let's take a second to consider the state of `main`.

`git log --graph --oneline --all`

TODO: example

You may be concerned that this will cause a lot of merge conflicts. Because `git` can see the merge history, it sees that we've already merge `main` into `polars`, so instead of forcing us to do the same thing again in the opposite direction, if we merge the latest `polars` onto `main` it will keep the changes we made.

`git switch main`

`git merge polars`

## Final Step. Cleaning Up

`git branch` will still show the old branches, which we no longer want.

To delete a merged branch use `git branch -d <branchname>`.

This will only delete branches that have been merged, giving an error if not. (This can be overriden with `-D` instead, but be careful when deleting unmerged work!)

## Post-Merge Checklist

After merging it is a good idea to ensure that you didn't break anything:

- run your tests (you have tests right?)
- run your linter (`uv run ruff check` / `uv run ruff format`)
- delete the work branch

## Note About Data

earnings.csv is a copy of 'Monthly employment earnings' downloaded from <https://ilostat.ilo.org/data/> on January 13th 2026.

There are methodological differences between how countries collect this data that one should seriously consider in making head-to-head comparisons between different countries.

The example code in this assignment would merely be a starting point, helping to analyze trends and tease out potential anomalies & outliers in the data for further evaluation.

This is a good reminder that a real analysis requires more than simple manipulation of numbers, but taking time to carefully understand the nuances of your data and how it was collected.
