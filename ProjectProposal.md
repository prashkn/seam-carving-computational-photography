# Project Proposal - Seam Carving

Authors: Trisha Menon (tmenon3) & Prashant Naganaboyina (pkn3)

---

### Motivation

We chose to work on implementing seam carving as we have often ran into the problem where we want to crop an image, but keep all the important information, such as people and objects. Seam carving seems to be a very interesting way to solve this problem.
We hope to build on our knowledge of graphs, and learn more about seam carving's energy functions. More specifically, how we can traverse through pixels and define the "importance of pixels".

### Milestones

| Week   | Milestone                                                                                                                            |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| Week 1 | Implementing the energy function                                                                                                     |
| Week 2 | Creating an accumulated cost matrix                                                                                                  |
| Week 3 | Finding seams from left to right and top to bottom to remove, based on "importance"                                                  |
| Week 4 | Final enhancement on algorithm; test algorithm and make adjustments                                                                  |
| Week 5 | Implement website, to allow users to upload their own image, define a custom width and height, and download the newly produced image |

We plan to meet twice a week to work on this project. On weeks where code can be created in parallel, we plan to meet once a week to just update each other and what we have done and what we have left to do.

### Evaluations

- Creating test cases for this algorithm will be quite hard; we initially thought of creating masks to cover objects in the image we wish to preserve after the seam carving algorithm is done, and test, through template matching, if the objects are still present after seam carving.
  - However, seam carving can slightly warp the original objects if the width and height are too constrained; hence, it will be hard to perform a 1-to-1 template match.
- Therefore, we will perform eye tests on a variety of images; natural images, manmade objects, etc. through both a strong height constraint, or width constraint. We will make a mental note of which objects we hope to see after the seam carving, and see if they are still in the image with minimal warping after the algorithm.

### Resources

There are no equipment or data we need to complete this project; we just need to run our seam carving algorithm on images. However, here are some resources to help us implement the algorithm:

https://perso.crans.org/frenoy/matlab2012/seamcarving.pdf

https://cs.brown.edu/courses/cs129/results/proj3/taox/

https://avikdas.com/2019/05/14/real-world-dynamic-programming-seam-carving.html

https://courses.cs.washington.edu/courses/cse373/20wi/homework/seamcarving/#seam-carving-algorithm

https://sandipanweb.wordpress.com/2017/10/14/seam-carving-using-dynamic-programming-to-implement-context-aware-image-resizing-in-python/

### Group Contributions

We identify 4 distinct parts to this project:

1. Setting up the seam carving algorithm (creating the energy mapping, creating a cost matrix, etc.)
2. Determining the "minimum importance" seam each time and removing accordingly
3. Testing & tuning
4. Creating the website

We plan to do all of these parts together, with a split of ownership over these 4 parts. So, Prashant will take ownership over part 2 and part 4, while Trisha will take ownership over part 1 and part 3. As mentioned before, we will still help each other on all parts, as we are both genuinely interested in this algorithm and developing/applying it.

Edit:

- We removed the website aspect of this project after our proposal was made. We did this because we were able to make our jupyter notebook interactive enough, and wanted to focus our time on the actual seam carving algorithm rather than the UI. We got this approved: https://campuswire.com/c/G59BF2AA8/feed/620
