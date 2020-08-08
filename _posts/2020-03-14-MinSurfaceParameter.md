---
layout: post
title: Minimal Surface & Mesh Parameterization
thumbnail-img: /assets/images/thumbnail-img/minsurf.png
cover-img: /assets/images/cover-img/CG.png
comments: true
gh-repo: Chaphlagical/USTC_CG
gh-badge: [star, fork, follow]
tags: [CG, Geometry]
comments: true
---

Minimal surface and mesh parameterization

## Feature

* Half-Edge Data Structure
* Minimal Surface
* Mesh Parameterization

## Development Environment

* **IDE**: Microsoft Visual Studio 2019 community
* **Build**: CMake 3.16.3
* **GUI Platform**: Qt 5.14.1
* **other 3rd Party Library**: Eigen 3.3.7, Assimp 5.0.1, tinyxml2 8.0.0

## Algorithm Introduction

### Minimal Surface

**Definition**: A surface with a mean curvature of 0 everywhere

**Algorithm**:

A surface with a mean curvature of 0 everywhere, then

$$
H(v_i)=0,\forall i
$$

![1](https://chaphlagical.github.io/assets/images/assets-img/MinSurf/1.jpg){: .mx-auto.d-block :}

As the figure shown, we have

$$
\lim\limits_{len(y)\rightarrow 0}\frac{1}{len(\gamma)}\int_{v\in \gamma}(v_i-v)ds=H(v_i)\boldsymbol{n}_i
$$

Differential coordinates:

$$
\delta_i=v_i-\frac{1}{d_i}\sum\limits_{v\in N(i)} v =\frac{1}{d_i}\sum\limits_{v\in N(i)} (v_i-v)=0
$$

Fixed boundary points, the vertex coordinates of the smallest plane can be obtained by solving sparse equations.

### Mesh Parameterization

Map the grid boundary to a convex polygon (such as a unit circle, a square), and generate the barycenter coordinates of the domain point $N(i)$ for each internal point $(\lambda_{i1},\lambda_{i2},\cdots,\lambda_{id_i})$, using barycenter coordinates we have:

$$
v_i-\sum\limits_{j\in N(i)}\lambda_{ij}v_j=0,i=1,\cdots,n
$$

$n$ is the number of internal points. By solving the sparse equations, the parameterized coordinates of the surface can be obtained. For different methods of obtaining the center of barycenter coordinates, the parametric grids obtained are also different. Using the parameterized texture coordinates to connect the texture image to realize texture mapping, as shown in the following figure, the texture mapping effect of different center of barycenter coordinates is also different:

![begin](https://chaphlagical.github.io/assets/images/assets-img/MinSurf/Figures\begin.png){: .mx-auto.d-block :}

#### Uniform

Uniform center of barycenter coordinates, only consider the degree of the internal point without considering the relationship with its neighboring points, that is, take the center of barycenter coordinates:

$$
\lambda_{ij}=\frac{1}{d_i},d_i=|N(i)|,j\in N(i)
$$

Each adjacent point has the same weight.

#### Cotangent

Cotangent center of barycenter coordinates, considering the positional relationship between internal points and adjacent points. As shown in the figure below, set the adjacent points connected by an internal point $v$ to be $v_{i-1}$, $v_i$, $v_{i+1}$, let $\beta_{i-1}=\angle{vv_{i-1}v_i}$ and $\gamma_i=\angle{vv_{i+1}v_i}$

![2](https://chaphlagical.github.io/assets/images/assets-img/MinSurf/2.png){: .mx-auto.d-block :}

Barycenter coordinates can be represented as:

$$
\lambda_j=\frac{w_j}{\sum\limits_{j\in N(v)}w_j}
$$

$$
w_j=\cot(\beta_{i-1})+\cot(\gamma_i),j\in N(v)
$$

## Demo

### Circle Boundary & Cotangent Weight

|                       Original Surface                       |                        Original Mesh                         |                      Parameterize Mesh                       |                           Texture                            |
| :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
| ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/ball.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/ball_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/ball_circle_cotangent_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/ball_circle_cotangent.png){: .mx-auto.d-block :} |
| ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/bunny.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/bunny_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/bunny_circle_cotangent_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/bunny_circle_cotangent.png){: .mx-auto.d-block :} |
| ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/cat.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/cat_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/cat_circle_cotangent_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/cat_circle_cotangent.png){: .mx-auto.d-block :} |
| ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/david.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/david_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/david_circle_cotangent_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/david_circle_cotangent.png){: .mx-auto.d-block :} |
| ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/face.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/face_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/face_circle_cotangent_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/face_circle_cotangent.png){: .mx-auto.d-block :} |

### Circle Boundary & Uniform Weight

|                       Original Surface                       |                        Original Mesh                         |                      Parameterize Mesh                       |                           Texture                            |
| :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
| ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/ball.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/ball_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/ball_circle_uniform_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/ball_circle_uniform.png){: .mx-auto.d-block :} |
| ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/bunny.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/bunny_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/bunny_circle_uniform_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/bunny_circle_uniform.png){: .mx-auto.d-block :} |
| ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/cat.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/cat_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/cat_circle_uniform_mesh.png){: .mx-auto.d-block :}{: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/cat_circle_uniform.png){: .mx-auto.d-block :}{: .mx-auto.d-block :} |
| ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/david.png){: .mx-auto.d-block :}{: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/david_mesh.png){: .mx-auto.d-block :}{: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/david_circle_uniform_mesh.png){: .mx-auto.d-block :}{: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/david_circle_uniform.png){: .mx-auto.d-block :}{: .mx-auto.d-block :} |
| ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/face.png){: .mx-auto.d-block :}{: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/face_mesh.png){: .mx-auto.d-block :}{: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/face_circle_uniform_mesh.png){: .mx-auto.d-block :}{: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/face_circle_uniform.png){: .mx-auto.d-block :}{: .mx-auto.d-block :} |

### Square Boundary & Cotangent Weight

|                       Original Surface                       |                        Original Mesh                         |                      Parameterize Mesh                       |                           Texture                            |
| :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
| ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/ball.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/ball_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/ball_square_cotangent_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/ball_square_cotangent.png){: .mx-auto.d-block :} |
| ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/bunny.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/bunny_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/bunny_square_cotangent_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/bunny_square_cotangent.png){: .mx-auto.d-block :} |
| ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/cat.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/cat_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/cat_square_cotangent_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/cat_square_cotangent.png){: .mx-auto.d-block :} |
| ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/david.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/david_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/david_square_cotangent_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/david_square_cotangent.png){: .mx-auto.d-block :} |
| ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/face.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/face_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/face_square_cotangent_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/face_square_cotangent.png){: .mx-auto.d-block :} |

### Square Boundary & Uniform Weight

|                       Original Surface                       |                        Original Mesh                         |                      Parameterize Mesh                       |                           Texture                            |
| :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
| ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/ball.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/ball_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/ball_square_uniform_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/ball_square_uniform.png){: .mx-auto.d-block :} |
| ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/bunny.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/bunny_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/bunny_square_uniform_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/bunny_square_uniform.png){: .mx-auto.d-block :} |
| ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/cat.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/cat_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/cat_square_uniform_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/cat_square_uniform.png){: .mx-auto.d-block :} |
| ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/david.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/david_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/david_square_uniform_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/david_square_uniform.png){: .mx-auto.d-block :} |
| ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/face.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/face_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/face_square_uniform_mesh.png){: .mx-auto.d-block :} | ![](https://chaphlagical.github.io/assets/images/assets-img/Minsurf/face_square_uniform.png){: .mx-auto.d-block :} |

## Demo Video

<video width="100%" height="100%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/images/videos/MinSurf/demo.mp4" type="video/mp4">
      </video>

## Resource

**Project**: [https://github.com/Chaphlagical/USTC_CG/tree/master/Homeworks/4_MinSurfMeshPara](https://github.com/Chaphlagical/USTC_CG/tree/master/Homeworks/4_MinSurfMeshPara) 