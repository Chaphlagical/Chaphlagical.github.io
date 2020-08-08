---
layout: post
title: Image Warping
thumbnail-img: /assets/images/thumbnail-img/imagewarping.jpg
cover-img: /assets/images/cover-img/CG.png
comments: true
gh-repo: Chaphlagical/USTC_CG
gh-badge: [star, fork, follow]
tags: [CG, Qt]
comments: true
---

Implement of Image Warping Algorithm from paper "*Image warping with scattered data interpolation*" and "*Image warping using few anchor points and radial functions*"

## Feature

* Inverse distance-weighted interpolation method (IDW)
* Radial basis functions interpolation method (RBF)
* Fix white crack

## Development Environment

* **IDE**: Microsoft Visual Studio 2019 community
* **Build**: CMake 3.16.3
* **GUI Platform**: Qt 5.14.1
* **other 3rd Party Library**: Eigen 3.3.7, ANN 1.1.2

## Algorithm Introduction

### Fundamental

* **Input**: $n$ pairs of points $(\boldsymbol{p_i},\boldsymbol{q_i}),i=1,2,\cdots,n$ , $p_i\in \mathbb{R}^2$ are source control points，$q_i\in \mathbb{R}^2$ are target control points
* **target**: Find a mapping $f:\mathbb{R}^2\rightarrow\mathbb{R}^2$ that satisfied $f(\boldsymbol{p_i})=\boldsymbol{q_i},i=1,2,\cdots,n$

### Inverse distance-weighted interpolation methods(IDW)

IDW Algorithm is based given control points and control point pairs' displacement vectors. Calculate the inverse distance weighted influence of the control point on the surrounding pixels to realize the displacement of each pixel of the image.

Select $n$ pairs of control points $(\boldsymbol{p_i},\boldsymbol{q_i}),i=1,2,\cdots,n$, target mapping $f:\mathbb{R}^2\rightarrow \mathbb{R}^2$ can be represented as:

$$
f(\boldsymbol{p})=\sum^n_{i=1}\omega_i(\boldsymbol{p})f_i(\boldsymbol{p})
$$

Weight $w_i(\boldsymbol{p})$ satisfied：

$$
w_i(\boldsymbol{p})=\frac{\sigma_i(\boldsymbol{p})}{\sum\limits^n_{j=1} \sigma_j(\boldsymbol{p})}
$$

$\sigma_i(\boldsymbol{p})$ represents $i$ -th control point pairs' inverse distance weighted influence on pixel, you can set: 

$$
\sigma_i(\boldsymbol{p})=\frac{1}{\|\boldsymbol{p}-\boldsymbol{p_i} \|^\mu} (\mu>1)
$$

or you can set as locally bounded weight：

$$
\sigma_i(\boldsymbol{p})=[\frac{(R_i-d(\boldsymbol{p},\boldsymbol{p_i}))}{R_id(\boldsymbol{p},\boldsymbol{p_i})}]^\mu
$$

$f_i$ is linear function, satisfied：

$$
f_i(\boldsymbol{p})=\boldsymbol{q_i}+\boldsymbol{T_i}(\boldsymbol{p}-\boldsymbol{p_i})
$$

$\boldsymbol{T_i} $ is a second-order matrix

$$
\boldsymbol{T_i}=\begin{bmatrix}

t_{11}^{(i)}&t_{12}^{(i)}\\

t_{21}^{(i)}&t_{22}^{(i)}

\end{bmatrix}
$$

To determine the matrix $T$, we just need to solve optimization problem：

$$
\min\limits_{\boldsymbol{T_i}} E_i(\boldsymbol{T_i})=\sum\limits^n_{j=1,j\neq i}\sigma_i(\boldsymbol{p_j})\|\boldsymbol{q_j}-f_i(\boldsymbol{p_j})\|^2
$$

Get derivation of every elements of $T$ and set to zero, we have:

$$
\boldsymbol{T}\sum\limits^n_{j=1,j\neq i}\sigma_i(\boldsymbol{p_j})\boldsymbol{\Delta p}\boldsymbol{\Delta p}^T =\sum\limits^n_{j=1,j\neq i}\sigma_i(\boldsymbol{p_j})\boldsymbol{\Delta q}\boldsymbol{\Delta p}^T
$$

And $\boldsymbol{\Delta p}=(\boldsymbol{p_j}-\boldsymbol{p_i}\ \boldsymbol{0})$，$\boldsymbol{\Delta q}=(\boldsymbol{q_j}-\boldsymbol{q_i}\ \boldsymbol{0})$，when $\sum\limits^n_{j=1,j\neq i}\sigma_i(\boldsymbol{p_j})\boldsymbol{\Delta p}\boldsymbol{\Delta p}^T$ is Non-singular, we have

$$
\boldsymbol{T}= (\sum\limits^n_{j=1,j\neq i}\sigma_i(\boldsymbol{p_j})\boldsymbol{\Delta q}\boldsymbol{\Delta p}^T)(\sum\limits^n_{j=1,j\neq i}\sigma_i(\boldsymbol{p_j})\boldsymbol{\Delta p}\boldsymbol{\Delta p}^T)^{-1}
$$

$\boldsymbol{T_i}(i=1,2,\cdots,n)$，at this time, we also determine mapping $f$

### Radial basis functions interpolation method(RBF)

Select $n$ pairs of control points $(\boldsymbol{p_i},\boldsymbol{q_i}),i=1,2,\cdots,n$, target mapping $f:\mathbb{R}^2\rightarrow \mathbb{R}^2$ can be represented as:

$$
f(\boldsymbol{p})=\sum\limits_{i=1}^n\alpha_i g_i(\|\boldsymbol{p}-\boldsymbol{p_i}\|)+\boldsymbol{A}\boldsymbol{p}+\boldsymbol{B}
$$

$g_i$ is radial basis function，we can usually use Hardy multi-quadrics or Gaussian function. For calculation convenience, here we use Hardy multi-quadrics：

$$
\begin{aligned}

g_i(d) & =(d+r_i)^{\pm\frac{1}{2}}\\

r_i & =\mathop{\min}\limits_{j\neq i} d(\boldsymbol{p_i},\boldsymbol{p_j})

\end{aligned}
$$

As for linear portion $\boldsymbol{A}\boldsymbol{p}+\boldsymbol{B}$, we just simply use $\boldsymbol{A}=\boldsymbol{I}$ and $\boldsymbol{B}=\boldsymbol{0}$

## Architecture

![2](https://chaphlagical.github.io/assets/images/assets-img/ImageWarping/2.png){: .mx-auto.d-block :}

## Demo

| Origin                                                       | demo1                                                        | demo2                                                        |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![dog](https://chaphlagical.github.io/assets/images/assets-img/ImageWarping/dog.jpg){: .mx-auto.d-block :} | ![dog1](https://chaphlagical.github.io/assets/images/assets-img/ImageWarping/dog1.jpg){: .mx-auto.d-block :} | ![dog2](https://chaphlagical.github.io/assets/images/assets-img/ImageWarping/dog2.bmp){: .mx-auto.d-block :} |
| ![1](https://chaphlagical.github.io/assets/images/assets-img/ImageWarping/1.jpg){: .mx-auto.d-block :} | ![2](https://chaphlagical.github.io/assets/images/assets-img/ImageWarping/2.bmp){: .mx-auto.d-block :} | ![3](https://chaphlagical.github.io/assets/images/assets-img/ImageWarping/3.jpg){: .mx-auto.d-block :} |
| ![tag](https://chaphlagical.github.io/assets/images/assets-img/ImageWarping/tag.png){: .mx-auto.d-block :} | ![RBF_mu=0_5_nofix](https://chaphlagical.github.io/assets/images/assets-img/ImageWarping/RBF_mu=0_5_nofix.jpg){: .mx-auto.d-block :} | ![RBF_mu=0_5_fix](https://chaphlagical.github.io/assets/images/assets-img/ImageWarping/RBF_mu=0_5_fix.jpg){: .mx-auto.d-block :} |

<video width="100%" height="100%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/ImageWarping/demo.mp4" type="video/mp4">
      </video>

## Resource

**Project**: [https://github.com/Chaphlagical/USTC_CG/tree/master/Homeworks/2_ImageWarping](https://github.com/Chaphlagical/USTC_CG/tree/master/Homeworks/2_ImageWarping)

## Reference

*[1] Detlef Ruprecht and Heinrich Muller. Image warping with scattered data interpolation. IEEE Computer Graphics and Applications,15(2):37–43, 1995*  

*[2] Nur Arad and Daniel Reisfeld. Image warping using few anchor points and radial functions. In Computer graphics forum, volume 14, pages 35–46. Wiley Online Library, 1995.*