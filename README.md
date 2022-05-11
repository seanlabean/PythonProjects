This is a continuously morphing repository acting essentially as a time machine and clunky storage of my various Python projects. Most Projects here are half-baked consisting of momentary interests that I persued and dropped within a week. There are also projects that piqued my interest enough to become separate efforts unto themselves. I provide links to the separately maintained git repository for such projects.

## Astrophysics/
A few mini projects having to do with astrophysics.
  **Roche-Lobe-py.ipynb** - A quick calculator to determine the Roch Lobe of any mass. This was left over from an attempt to learn Julia. The sister JuliaProjects git repo can be found [here](https://github.com/seanlabean/JuliaProjects).
  **voronoi-mesh-scipy.ipynb** - This was the beginnings of a series of computational tests to determine whether it was possible to map a galactic simulation using a moving-mesh grid structure to our Torch computational framework that uses an adaptive mesh refinement structure. See the [AREPO-TORCH](https://github.com/seanlabean/AREPO-TORCH) repository for more details on this project. This jupyter notebook tests how to construct a binary tree and voronoi mesh grid from a set of data points. I also explored how to extract volume overlaps of voronoi cells and cubes.

## BrainFck/
I was interested in esoteric programming languages and so collected some resources to try and build my own Python interpreter of the esolang Brainfuck.

## DeepLearning/
I started combing throught the textbook *Deep Learning From Scratch* by Seth Weidman. I wanted to go through chapter by chapter and follow along with the given coding examples. I stopped soon after, but recently (as of May 2022) I've developed a much more robust background on DL and would like to try again here.

## FileManipulation/
This only contains a small jupyter notebook where I wrote down some of my thoughts and understandings pertaining to `pickle` objects in Python. I think I was looking into this because I wanted to pickle the tree data structures that I was building as part of my [AREPO-TORCH](https://github.com/seanlabean/AREPO-TORCH) data port. I also comment a bit on the `PROTOCOL` level which creates some issues when trying to mix pickles made with Python2.X with Python3.X.

## HackerRank/
[HackerRank](https://www.hackerrank.com/) is a website that pairs workers with potential employees. It also provides some coding interview practice problems. I thought I would start solving these as a means of practice. I stopped fairly early on as, at the time, it was still 2 years until I would be entering the job market and I since moved on to [leetcode](https://leetcode.com/) anyways.

## MachineLearning/
These are two projects I started to prove to myself I could build some sort of machine learning product. The first is a simple decision tree classifier model that determines whether an online article is "fake" or not. The second is the same style of linear regression applied to stock market prices, a classically foolish attempt to predict inherently stochastic market movement with a linear model. I now know so much more about machine learning, looking back at this attempt is certainly illuminating.

## MultiProc/
This is a test of Python's multiprocessing library. I needed to make hundreds of plots from very large data files that took non-trivial amounts of time to load and open. This is an example of a data-based implementation of parallel processing.

## SpeedTest/
I was having trouble with my internet speeds while working at home during the onset of the pandemic in 2020. My speeds were far too low for what I was paying for and I wanted to systematically record what the speeds were throughout the day for a week or so. That way during my phone call with my ISP I could drop some data on them and hopefully get my issue addressed. It worked!

## TaskBasedProcessing/
This is the skeleton of a much larger multiprocessing endeavor I went on that ultimately resulted in me creating a Python-based module that uses OpenMPI to parallelize jobs more efficiently than the native python multiprocessing library. A deeper explanation of this module an what it can be used for can be found in my [PythonOpenMPI repository](https://github.com/seanlabean/PythonOpenMPI).