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
  - However, seam carving tends to warp the original objects if the width and height are too constrained; hence, it will be hard to perform a 1-to-1 template match.
- Therefore, we will perform eye tests on a variety of images; natural images, manmade objects, etc. through both a strong height constraint, or width constraint. We will make a mental note of which objects we hope to see after the seam carving, and see if they are still in the image with minimal warping after the algorithm.

### Resources

https://en.wikipedia.org/wiki/Seam_carving
https://cs.brown.edu/courses/cs129/results/proj3/taox/


### Group Contributions
