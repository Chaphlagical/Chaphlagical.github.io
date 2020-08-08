---
layout: post
title: Mass Spring
thumbnail-img: /assets/images/thumbnail-img/massSpring.png
cover-img: /assets/images/cover-img/CG.png
comments: true
gh-repo: Chaphlagical/USTC_CG
gh-badge: [star, fork, follow]
tags: [CG, Physics Simulation]
comments: true
---

Mass spring system Implicit Euler method and acceleration method.

## Feature

* Mass Spring System Implicit Euler Method Simulation
* Mass Spring  System Simulation Acceleration Method

## Development Environment

* **IDE**: Microsoft Visual Studio 2019 community
* **Build**: CMake 3.16.3
* **GUI Platform**: Qt 5.14.1
* **other 3rd Party Library**: Eigen 3.3.7, Assimp 5.0.1, tinyxml2 8.0.0

## Algorithm Introduction

### Mass Spring Model

A spring-mass point system is a graph composed of nodes and edges between nodes, or you can say, a grid. Each vertex of the grid graph is regarded as a mass point, and each edge is regarded as a spring. The grid can be a two-dimensional grid to simulate objects such as cloth and paper; it can also be a three-dimensional volume grid to simulate solid objects.

### Implicit Euler Method

Knowing the information of the first $n$ frame, we suppose the displacement is $\boldsymbol x$, the speed is $\boldsymbol v$, and the time step is $h$. Now let's calculate the information of the frame $n+1$

The $n+1$th frame information and the $n$ th frame information satisfy the following relationship:
$$
\begin{aligned}

\boldsymbol x_{n+1}&=\boldsymbol x_n+h\boldsymbol v_{n+1}\\

\boldsymbol v_{n+1}&=\boldsymbol v_n+h\boldsymbol M^{-1}(\boldsymbol f_{int}(t_{n+1})+\boldsymbol f_{ext})

\end{aligned}
$$
Set
$$
\boldsymbol y=\boldsymbol x_n+h\boldsymbol v_n+h^2\boldsymbol M^{-1}\boldsymbol f_{ext}
$$
Then the original problem transformed into solving the equaiton about $\pmb x$
$$
\boldsymbol g(\boldsymbol x)=\boldsymbol M(\boldsymbol x-\boldsymbol y)-h^2\boldsymbol f_{int}(\boldsymbol x)=0
$$
Using Newton's method to solve the equation, the main iterative steps:
$$
\boldsymbol x^{(k+1)}=\boldsymbol x^{(k)}-(\nabla \boldsymbol g(\boldsymbol x^{(k)}))^{-1}\boldsymbol g(\boldsymbol x^{(k)})
$$
Inital value can use $\boldsymbol x^{(0)}=\boldsymbol y$

After iteration, we can get displacement $\pmb x$, then update the speed: $\boldsymbol v_{n+1}=(\boldsymbol x_{n+1}-\boldsymbol x_n)/h$

### About Elastic Derivation

For single spring (the endpoint is $\boldsymbol x_1$, $\boldsymbol x_2$), the stiffness coefficient is $k$, the original length is $l$, there are:
$$
\begin{aligned}

\boldsymbol f_1(\boldsymbol x_1,\boldsymbol x_2)&=k(||\boldsymbol x_1-\boldsymbol x_2||-l)\frac{\boldsymbol x_2-\boldsymbol x_1}{||\boldsymbol x_1-\boldsymbol x_2||}\\

\boldsymbol f_2(\boldsymbol x_1,\boldsymbol x_2)&=-\boldsymbol f_1(\boldsymbol x_1,\boldsymbol x_2)

\end{aligned}
$$
For
$$
\boldsymbol h(\boldsymbol x)=k(||\boldsymbol x||-l)\frac{-\boldsymbol x}{||\boldsymbol x||}
$$
Get derivation, 
$$
\frac{ d \boldsymbol h}{d \boldsymbol x} = k(\frac{l}{||\boldsymbol x||}-1)\boldsymbol I-kl||\boldsymbol x||^{-3}\boldsymbol x \boldsymbol x^T
$$
Substituting the elastic formula into:
$$
\frac{\partial \boldsymbol f_1}{\partial \boldsymbol x_1} =\frac{\partial \boldsymbol h(\boldsymbol x_1-\boldsymbol x_2)}{\partial \boldsymbol x_1}=k(\frac{l}{||\boldsymbol r||}-1)\boldsymbol I-kl||\boldsymbol r||^{-3}\boldsymbol r \boldsymbol r^T
$$

$$
\frac{\partial \boldsymbol f_1}{\partial \boldsymbol x_2}=-\frac{\partial \boldsymbol f_1}{\partial \boldsymbol x_1},

\frac{\partial \boldsymbol f_2}{\partial \boldsymbol x_1}=-\frac{\partial \boldsymbol f_1}{\partial \boldsymbol x_1},

\frac{\partial \boldsymbol f_2}{\partial \boldsymbol x_2}=\frac{\partial \boldsymbol f_1}{\partial \boldsymbol x_1}
$$

And $\boldsymbol r=\boldsymbol x_1-\boldsymbol x_2$，$\boldsymbol I$ is unit matrix

### Acceleration Method

The elastic potential energy of the spring can be described as a minimization problem:
$$
\frac{1}{2}k(\|\boldsymbol p_1-\boldsymbol p_2\|-r)^2=\frac{1}{2}k\min\limits_{\|\boldsymbol d\|=r}\|\boldsymbol p_1-\boldsymbol p_2-\boldsymbol d\|^2
$$
The original problem can be transformed into:
$$
\boldsymbol x_{n+1}=\min\limits_{x,\boldsymbol d\in \boldsymbol U}\frac{1}{2} \boldsymbol x^T(\boldsymbol M+h^2\boldsymbol L)\boldsymbol x-h^2\boldsymbol x^T\boldsymbol J\boldsymbol d-\boldsymbol x^T\boldsymbol M\boldsymbol y
$$
And $\boldsymbol U=\{\boldsymbol d=(\boldsymbol d_1,\boldsymbol d_2,\cdots,\boldsymbol d_s),\boldsymbol d_s\in R^3,\|\boldsymbol d_i\|=l_i\}$ ($l_i$ is the original length of the $i$ spring)

Matrix  $\boldsymbol L\in R^{3m\times 3m}$，$\boldsymbol J\in R^{3m\times 3s}$ is defined as:
$$
\begin{aligned}

\boldsymbol L=\left(\sum\limits_{i=1}^sk_i\boldsymbol A_i\boldsymbol A_i^T\right)\otimes\boldsymbol I_3,

\boldsymbol J=\left(\sum\limits_{i=1}^sk_i\boldsymbol A_i\boldsymbol S_i^T\right)\otimes \boldsymbol I_3

\end{aligned}
$$
$\boldsymbol A_i$ is the correlation vector of the $i$ th spring (for example, the index of the end points of the $i$ th spring are $i_1$ and $i_2$, then $\boldsymbol A_{i,i_1}=1$, $ \boldsymbol A_{i,i_2}=-1$, the remaining elements are 0), $\boldsymbol S_i$ is the indicator matrix of the $i$th spring, $S_{i,j}=\delta_{i,j} $

Thus, the solution of the optimization problem can be obtained by iterative optimization of $\boldsymbol x$, $\boldsymbol d$:
$$
\begin{aligned}

&\mathrm{optimize}\ \boldsymbol x:(\boldsymbol M+h^2\boldsymbol L)\boldsymbol x=h^2\boldsymbol J\boldsymbol d+\boldsymbol M\boldsymbol y\\

&\mathrm{optimize}\ \boldsymbol d:\boldsymbol d_i=l_i\frac{\boldsymbol p_{i_1}-\boldsymbol p_{i_2}}{\|\boldsymbol p_{i_1}-\boldsymbol p_{i_2}\|}

\end{aligned}
$$
Repeat iteration until convergence.

### Handling Displacement constraint

List the coordinates of all $n$ mass points as a column vector $x\in R^{3n}$, and list all $m$ free mass point coordinates (unconstrained coordinates) as a column vector $x_f\in R^{3m}$, then the relationship between the them:
$$
\begin{aligned}

\boldsymbol x_f&=\boldsymbol K\boldsymbol x,\\ \boldsymbol x&=\boldsymbol K^T\boldsymbol x_f+\boldsymbol b\

\end{aligned}
$$
$\boldsymbol K\in R^{3m\times 3n}$ is the sparse matrix obtained by deleting the corresponding row of the constraint coordinate number in the unit matrix, and $\boldsymbol b$ is the vector related to the constraint displacement, calculated as $\boldsymbol b =\boldsymbol x-\boldsymbol K^T\boldsymbol K\boldsymbol x$, if the constraint is a fixed mass point, $\boldsymbol b$ is a constant. From this, we transform the original optimization problem of $\boldsymbol x$ into an optimization problem of $\boldsymbol x_f$: the solution equation in Euler's implicit method is:
$$
\begin{aligned}

\boldsymbol g_1(\boldsymbol x_f) &= \boldsymbol K(\boldsymbol M(\boldsymbol x-\boldsymbol y) -h^2\boldsymbol f_{int}(\boldsymbol x)) = 0,\\

\nabla_{\boldsymbol x_f} \boldsymbol g_1(\boldsymbol x_f) &= \boldsymbol K\nabla_{\boldsymbol x} \boldsymbol g(\boldsymbol x)\boldsymbol K^T,\\

\end{aligned}
$$
The iterative step of $\boldsymbol x$ in the optimization problem of the acceleration method is transformed into solving the equation about $x_f$:
$$
\boldsymbol K(\boldsymbol M+h^2\boldsymbol L)\boldsymbol K^T\boldsymbol x_f=\boldsymbol K(h^2\boldsymbol J \boldsymbol d+ \boldsymbol M \boldsymbol y-(\boldsymbol M+h^2\boldsymbol L)\boldsymbol b)
$$

## Demo

### Cloth

<video width="100%" height="100%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/MassSpring/demo1.mp4" type="video/mp4">
      </video>

<video width="100%" height="100%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/MassSpring/demo7.mp4" type="video/mp4">
      </video>
### Face

<video width="100%" height="100%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/MassSpring/demo3.mp4" type="video/mp4">
      </video>
### Triangle

<video width="100%" height="100%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/MassSpring/demo5.mp4" type="video/mp4">
      </video>
### Cube

<video width="100%" height="100%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/MassSpring/demo2.mp4" type="video/mp4">
      </video>

<video width="100%" height="100%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/MassSpring/demo6.mp4" type="video/mp4">
      </video>