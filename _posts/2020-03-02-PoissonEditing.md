---
layout: post
title: Poisson Editing
thumbnail-img: /assets/images/thumbnail-img/poisson.jpg
cover-img: /assets/images/cover-img/CG.png
comments: true
gh-repo: Chaphlagical/USTC_CG
gh-badge: [star, fork, follow]
tags: [CG, Image Process, Qt]
comments: true
---

Implement of Poisson Image Editing Algorithm from Siggraph 2003 paper.

## Feature

* Poisson Image Editing Algorithm
* Scan Line Algorithm
* Solving Large Sparse Matrix using Eigen
* Realtime displayment

## Development Environment

* **IDE**: Microsoft Visual Studio 2019 community
* **Build**: CMake 3.16.3
* **GUI Platform**: Qt 5.14.1
* **other 3rd Party Library**: Eigen 3.3.7, OpenCV 4.2.0

## Algorithm Introduction

Assume we have two images:

![girl](D:\USTC_CG\Homeworks\3_PoissonImageEditing\report\Figures\girl.jpg)

![sea](D:\USTC_CG\Homeworks\3_PoissonImageEditing\report\Figures\sea.jpg)

Now we want to merge two images and make sure it look more natural, that's what Poisson Image Editing will do.

### Poisson Image Editing

The basic idea of Poisson Image Editing Algorithm is to make the boundary value of the pasted image the same as the new background image while maintaining the internal gradient of the original image as much as possible to achieve a seamless pasting effect. Mathematically speaking, for original image $f(x,y)$, new background $f^*(x,y)$ and new image $v(x,y)$ embedded with the new background are equivalent to the solution optimization problem:

$$
\min\limits_f \iint _\Omega |\nabla f-\nabla \boldsymbol v |^2 \ \ \mathrm{with}\ f|_{\partial \Omega}=f^*|_{\partial \Omega}
$$

Using calculus of variations we can get Poisson equation with Dirichlet boundary conditions

$$
\Delta f= \Delta \boldsymbol v\ \mathrm{over}\ \Omega \ \ \mathrm{with}\ f|_{\partial \Omega}=f^*|_{\partial \Omega}
$$

Take two images as examples, set area need to be copied in image I as $S$. Define $N_p$ as each pixel $p$ in $S$ connecting the neighborhood in four directions, and let $<p,q>$ be a pixel pair satisfying $q\in N_p$. The boundary $\Omega$ is defined as $\partial \Omega =\{p\in S\setminus \Omega: N_p \cap \Omega \neq \emptyset \}$, let $f_p$ be the pixel value $f$ at $p$, our goal is to solve the pixel value set $f\mid_\Omega =\{f_p,p\in \Omega\}$ 

Using the basic principles of the Poisson Image Editing algorithm, the above problem can be transformed into an optimization problem:

$$
\min\limits_{f|_\Omega}\sum\limits_{<p,q>\cap \Omega\neq \emptyset}(f_p-f_q-v_{pq})^2,\mathrm{with}\ f_p=f_p^*,\mathrm{for}\ \mathrm{all}p\in \partial\Omega
$$

Solving linear equation:

$$
\mathrm{for}\ \mathrm{all}\ p\in \Omega,\ \mid N_p\mid f_p-\sum\limits_{q\in N_p\cap \Omega} f_q=\sum\limits_{q\in N_p\cap \partial \Omega}f_p^*+\sum\limits_{q\in N_p}v_{pq}
$$

As for the selection of gradient field $\boldsymbol{v}(\boldsymbol{x})$, the paper has given two different methods. One is completely using the internal gradient of the foreground image, like this:

$$
\mathrm{for}\ \mathrm{all}\ <p,q>,v_{pq}=g_p-g_q
$$

Another is using Hybrid gradient:

$$
\mathrm{for}\ \mathrm{all}\ \boldsymbol{x}\in \Omega,\ \boldsymbol{v}(\boldsymbol{x})=\begin{cases}

\nabla f^*(\boldsymbol{x})&\mathrm{if}\ \mid\nabla f^*(\boldsymbol{x})\mid>\mid\nabla g(\boldsymbol{x})\mid,\\

\nabla g(\boldsymbol{x})&\mathrm{otherwise}

\end{cases}
$$

### Scan Line Algorithm

I learn about ordered edge table method from [https://blog.csdn.net/xiaowei\_cqu/article/details/7712451](https://blog.csdn.net/xiaowei\_cqu/article/details/7712451) 



![class](D:\USTC_CG\Homeworks\3_PoissonImageEditing\report\Figures\class.png)