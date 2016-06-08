#Image recognition algorithm test: step1.

1) Teach computer how to find a black frame on a graphic image:
* clear (sq.jpg)
* noisy (sq_noise.jpg)
* distorted (sq_dist.jpg)

2) Algorithm: blackshape_test.py (from openCV box)

3) Results: res_*.jpg

4) Conclusion: coloured noisy image (25%) is almost inreal to recognize. Still, only one shape is found, but it is just a mess. 

5) Further steps:
1. Find lowest noise threshold when a shape is still recognizeable.
2) Find out whether de-noising can work for noisy images.
3. Go to experiment 2 with graphic image.

##Experiment 2.
1) Teach computer how to find areas according to the colour.
2) Select the areas.
3) Define their colour.
