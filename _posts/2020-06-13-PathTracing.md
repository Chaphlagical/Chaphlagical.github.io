---
layout: post
title: Path Tracing
subtitle: USTC CG Course 2020
thumbnail-img: /assets/images/thumbnail-img/pathtracing.png
cover-img: /assets/images/cover-img/CG.png
comments: true
gh-repo: Chaphlagical/USTC_CG
gh-badge: [star, fork, follow]
tags: [CG, Rendering]
readtime: true
---

Basic Path Tracing

## Feature

* Path Tracing Rendering

## Development Environment

* **IDE**: Microsoft Visual Studio 2019 community
* **Build**: CMake 3.16.3

## Algorithm Introduction

### Rendering Equation

$$
L_o(\pmb{p},\pmb{\omega}_o)=L_e(\pmb{p},\pmb{\pmb{\omega}_o})+\int_{\mathcal{H}^2(\pmb{n}(\pmb{p}))} f_r(\pmb{p},\pmb{\omega}_i,\pmb{\omega}_o)L_i(\pmb{p},\pmb{\omega}_i)\cos\theta_{\pmb{\omega}_i,\pmb{n}(\pmb{p})}\mathbb{d}\pmb{\omega}_i
$$

* $L_o$ is inciden tradiance
* $\pmb{p}$ is rendering point
* $\pmb{\omega}_i$ is incident direction
* $\pmb{\omega}_o$ is exit direction
* $L_e$ is lighting radiance
* $\pmb{n}(\pmb{p})$ 
* ${\mathcal{H}^2(\pmb{n}(\pmb{p}))} $ is the hemisphere of normal $\pmb{n}(\pmb{p})$ 
* $f_r$ is the Bidirectional Reflectance Distribution Function (BRDF)
* $L_i$ is exit radiance
* $\theta_{\pmb{\omega}_i,\pmb{n}(\pmb{p})}$ is the angle between $\pmb{\omega}_i$ and $\pmb{n}(\pmb{p})$ 

Set

$$
\int_{\pmb{p},\pmb{\omega}_o,\pmb{\omega}_i}L=\int_{\mathcal{H}^2(\pmb{n}(\pmb{p}))} f_r(\pmb{p},\pmb{\omega}_i,\pmb{\omega}_o)L\cos\theta_{\pmb{\omega}_i,\pmb{n}(\pmb{p})}\mathbb{d}\pmb{\omega}_i.
$$

Then

$$
L_o(\pmb{p},\pmb{\omega}_o)=L_e(\pmb{p},\pmb{\pmb{\omega}_o})+\int_{\pmb{p},\pmb{\omega}_o,\pmb{\omega}_i}L_i(\pmb{p},\pmb{\omega}_i)
$$

The reflection equation will be

$$
L_r(\pmb{p},\pmb{\omega}_o)=\int_{\pmb{p},\pmb{\omega}_o,\pmb{\omega}_i}L_i(\pmb{p},\pmb{\omega}_i)
$$

As for $L_i$

$$
L_i(\pmb{p},\pmb{\omega}_i)=L_o(\mathop{raytrace}(\pmb{p},\pmb{\omega_i}),-\pmb{\omega_i})
$$

$raytrace$ is intersection function of ray and scene

Set $\mathop{raytrace}(\pmb{p},\pmb{\omega}_i)$ to be $\pmb{p}^\prime$, we have

$$
L_i(\pmb{p},\pmb{\omega}_i)=L_o(\pmb{p}^\prime,-\pmb{\omega_i})
$$

Recursively,

$$
L_o(\pmb{p},\pmb{\omega}_o)=L_e(\pmb{p},\pmb{\pmb{\omega}_o})+\int_{\pmb{p},\pmb{\omega}_o,\pmb{\omega}_i}L_o(\pmb{p}^\prime,-\pmb{\omega_i})
$$

Expand $L_r$

$$
\begin{aligned}
L_r(\pmb{p},\pmb{\omega}_o)
&=\int_{\pmb{p},\pmb{\omega}_o,\pmb{\omega}_i}\left(L_e(\pmb{p}^\prime,-\pmb{\omega}_i)+L_r(\pmb{p}^\prime,-\pmb{\omega}_i)\right)\\
&=\int_{\pmb{p},\pmb{\omega}_o,\pmb{\omega}_i}L_e(\pmb{p}^\prime,-\pmb{\omega}_i)
+\int_{\pmb{p},\pmb{\omega}_o,\pmb{\omega}_i}L_r(\pmb{p}^\prime,-\pmb{\omega}_i)
\end{aligned}
$$

Define

* Direct Light

$$
L_{\text{dir}}(\pmb{p},\pmb{\omega}_o)=\int_{\pmb{p},\pmb{\omega}_o,\pmb{\omega}_i}L_e(\pmb{p}^\prime,-\pmb{\omega}_i)
$$

* Indirect Light

$$
L_{\text{indir}}(\pmb{p},\pmb{\omega}_o)=\int_{\pmb{p},\pmb{\omega}_o,\pmb{\omega}_i}L_r(\pmb{p}^\prime,-\pmb{\omega}_i)
$$

### Direct Light

$$
L_{\text{dir}}(\pmb{p},\pmb{\omega}_o)=\int_{\pmb{p},\pmb{\omega}_o,\pmb{\omega}_i}L_e(\pmb{p}^\prime,-\pmb{\omega}_i)
$$

 In the Integration, for most of the direction, $\pmb{\omega}_i$, (is not light source). Therefore, we directly integrate in the direction of the light source.

$\pmb{p}$,  $\pmb{\omega}_o$ and $\pmb{\omega}_i$ can be determined bt there points.

![xyz](https://chaphlagical.github.io/assets/images/assets-img/PathTracing/xyz.jpg){: .mx-auto.d-block :}

$\pmb{x}$ is $\pmb{p}$，$\pmb{y}$ is $\pmb{p}^\prime$ 

According to the geometry relationship, we know

$$
\mathbb{d}\pmb{\omega}_i=\frac{|\cos\theta_{\pmb{y},\pmb{x}}|}{\|\pmb{x}-\pmb{y}\|^2}\mathbb{d}A(\pmb{y})
$$

And $\theta_{\pmb{y},\pmb{x}}$ is the angle between $\pmb{x}-\pmb{y}$ and $\pmb{n}(\pmb{y})$ 

Introduce geometric transmission term (describe the transmission efficiency between two points)

$$
G(\pmb{x}\leftrightarrow\pmb{y})=V(\pmb{x}\leftrightarrow\pmb{y})\frac{|\cos\theta_{\pmb{x},\pmb{y}}||\cos\theta_{\pmb{y},\pmb{x}}|}{\|\pmb{x}-\pmb{y}\|^2}
$$

$V(\pmb{x}\leftrightarrow\pmb{y})$ is visibility function. When no block between $\pmb x$ and $\pmb y$, $V(\pmb{x}\leftrightarrow\pmb{y})=1$. Otherwise, $V(\pmb{x}\leftrightarrow\pmb{y})=0$

$G$ is symmetric function, $G(\pmb{x}\leftrightarrow\pmb{y})=G(\pmb{y}\leftrightarrow\pmb{x})$ 

Then,

$$
L_{\text{dir}}(\pmb{x}\to\pmb{z})=\int_A f_r(\pmb{y}\to \pmb{x}\to\pmb{z})L_e(\pmb{y}\to\pmb{x})G(\pmb{x}\leftrightarrow\pmb{y})\mathbb{d}A(\pmb{y})
$$

The integral domain $A$ is all the area in the scene, but only at the light source $L_e(\pmb{y}\to\pmb{x})\neq 0$

Set the number of light sources $N_e$, the light source set in the scene is $ [L_{e_i}]_{i=1}^{N_e} $ , and the corresponding area set is $ [A(L_{e_i})]_{i=1}^{N_e} $, it can be written as

$$
L_{\text{dir}}(\pmb{x}\to\pmb{z})=\sum_{i=1}^{N_e}\int_{A(L_{e_i})} f_r(\pmb{y}\to\pmb{x}\to\pmb{z})L_e(\pmb{y}\to\pmb{x})G(\pmb{x}\to\pmb{y})\mathbb{d}A(\pmb{y})
$$

### Indirect Light

Recursively,

$$
L_r(\pmb{p},\pmb{\omega}_o)=\int_{\pmb{p},\pmb{\omega}_o,\pmb{\omega}_i}L_e(\pmb{p}^\prime,-\pmb{\omega}_i)

+\int_{\pmb{p},\pmb{\omega}_o,\pmb{\omega}_i}L_r(\pmb{p}^\prime,-\pmb{\omega}_i)
$$

### Monte Carlo Integration and Importance Sampling

Calculate the integral by sampling, the variance has nothing to do with the dimension of the integral domain $D$

$X$ is a continuous random variable, $F$ is a random variable function: $F=g(X),X\sim p(x)$

Expectation of $F$: $E[F]=\int_Dg(x)p(x)dx$

Estimation of $F$: $F_N=\frac{1}{N}\sum\limits_{i=1}^Ng(x_i)\xrightarrow[]{N}E[Y]$

Relationship between $f$ and $g$: $g(x)=\frac{f(x)}{g(x)}$

Combine them: $\frac{1}{N}\sum\limits_{i=1}^N\frac{f(x_i)}{p(x_i)}\xrightarrow[]{N}\int_D f(x)dx$

Variance: $V[F_N]=\frac{1}{N}V\Big[\frac{f(x)}{p(x)}\Big]\sim O(\frac{1}{N})$

In order to reduce the error, in addition to increasing the number of samples, you can also reduce $V[\frac{f(x)}{p(x)}]$

**Importance Sampling**

If $p(x)=\frac{f(x)}{\int_D f(x)dx}$, then

$$
V\Big[\frac{f(x)}{p(x)}\Big]=V\Big[\frac{1}{\int_D f(x)dx}\Big]
$$

As long as the shapes of $p(x)$ and $f(x)$ are close, the variance will be smaller, such as $f(x)=g(x)h(x)$, $h(x)\approx c $, and the integral of $g(x)$ can be calculated, then $p(x)=\frac{g(x)}{\int_D g(x)dx}$

### Solving Rendering Equation

We need to calculate following integration

$$
L_r(\pmb{p},\pmb{\omega}_o)=L_{\text{dir}}+L_{\text{indir}}
$$

Using Monte Carlo Method can transform integration into sampling

$$
\begin{aligned}

L_{\text{dir}}(\pmb{x}\to\pmb{z})

&\approx\sum_{i=1}^{N_e}\sum_{j=1}^{N_i}\frac{f_r(\pmb{y}_i^{(j)}\to\pmb{x}\to\pmb{z})L_e(\pmb{y}_i^{(j)}\to\pmb{x})G(\pmb{x}\to\pmb{y}_i^{(j)})}{p(\pmb{y}_i^{(j)})}\\

L_{\text{indir}}(\pmb{p},\pmb{\omega}_o)

&\approx\sum_{k=1}^{N}\frac{f_r(\pmb{p},\pmb{\omega}_i^{(k)},\pmb{\omega}_o)L_r(\pmb{p}^{\prime(k)},-\pmb{\omega})\cos\theta_{\pmb{\omega}_i,\pmb{n}(\pmb{p})}}{p(\pmb{\omega}_i^{(k)})}

\end{aligned}
$$

$L_{\text{dir}}$ Sampling in each light source area

For $L_{\text{indir}}$ hemisphere sampling

The number of samples is all 1 ($N_i=1\quad(i=1,\dots,N_e)$, $N=1$)

### Environment Map Importance Sampling

![is_em](https://chaphlagical.github.io/assets/images/assets-img/PathTracing/is_em.jpg){: .mx-auto.d-block :}

**Alias Method**

*Operation*

the algorithm consults two tables, a probability table $U_i$ and an alias table $K_i$ (for $1 \leq i\leq n$). To generate a random outcome, a fair diсe is rolled to determine an index into the two tables. Based on the probability stored at that index, a biased coin is then flipped, and the outcome of the flip is used to choose between a result of $i$ and $K_i$.

More concretely, the algorithm operates as follows:

1. Generate a uniform random variate $0\leq x\leq 1$
2. Let $i = ⌊nx⌋ + 1$ and $y = nx + 1 − i$. (This makes $i$ uniformly distributed on $\{1, 2, \cdots , n\}$ and *y* uniformly distributed on $[0, 1)$.)
3. If $y < U_i$, return $i$. This is the biased coin flip.
4. Otherwise, return $K_i$.

*Table Generation*

The distribution may be padded with additional probabilities $p_i = 0$ to increase *n* to a convenient value, such as a power of two.

To generate the table, first initialize $U_i = np_i$. While doing this, divide the table entries into three categories:

- The “overfull” group, where $U_i > 1$,
- The “underfull” group, where $U_i < 1$ and $K_i$ has not been initialized, and
- The “exactly full” group, where $U_i = 1$ or $K_i$ *has* been initialized.

If $U_i = 1$, the corresponding value $K_i$ will never be consulted and is unimportant, but a value of $K_i = i$ is sensible.

As long as not all table entries are exactly full, repeat the following steps:

1. Arbitrarily choose an overfull entry $U_i > 1$ and an underfull entry $U_j < 1$. (If one of these exists, the other must, as well.)
2. Allocate the unused space in entry $j$ to outcome $i$, by setting $K_j = i$.
3. Remove the allocated space from entry $i$ by changing $U_i = U_i − (1 − U_j) = U_i + U_j − 1$.
4. Entry $j$ is now exactly full.
5. Assign entry $i$ to the appropriate category based on the new value of $U_i$.

After generating alias table, we can use discrete pixels. The probability relationship is

$$
\begin{aligned}

\int_{I}p_{\text{img}}(i,j)\mathrm{d}i\mathrm{d}j

&=\int_{\Theta}p_{\text{img}}(\theta,\phi)\left|\frac{\partial(i,j)}{\partial(\theta,\phi)}\right|\mathrm{d}\theta\mathrm{d}\phi\\

&=\int_{A}p_{\text{img}}(A)\left|\det J_A\Theta\right|\left|\frac{\partial(i,j)}{\partial(\theta,\phi)}\right|\mathrm{d}A\\

&=\int_{\Omega}p_{\text{img}}(\pmb{\omega}_i)\left|\frac{\mathrm{d}A}{\mathrm{d}\pmb{\omega}_i}\right|\left|\det J_A{\Theta}\right|\left|\frac{\partial(i,j)}{\partial(\theta,\phi)}\right|\mathrm{d}\pmb{\omega}_i\\

&=\int_{\Omega}p(\pmb{\omega}_i)\mathrm{d}\pmb{\omega}_i\\

\end{aligned}
$$

![dwi_dA](https://chaphlagical.github.io/assets/images/assets-img/PathTracing/dwi_dA.jpg){: .mx-auto.d-block :}

$$
\begin{aligned}

\left|\frac{\mathrm{d}\pmb{\omega}_i}{\mathrm{d}A}\right|&=\frac{|\cos\theta_o|}{\|\pmb{x}-\pmb{y}\|^2}=\frac{1}{R^2}\\

\left|\det J_A\Theta\right|&=\frac{1}{R^2\sin\theta}\\

\left|\frac{\partial(i,j)}{\partial(\theta,\phi)}\right|&=\frac{wh}{2\pi^2}

\end{aligned}
$$

We can get

$$
p(\pmb{\omega}_i)=\frac{wh}{2\pi^2\sin\theta}p_{\text{img}}(i,j)
$$

## Demo

### Area Direction Light

![](https://chaphlagical.github.io/assets/images/assets-img/PathTracing/area_dir.png){: .mx-auto.d-block :}

### Area Indirection Light

![](https://chaphlagical.github.io/assets/images/assets-img/PathTracing/area_indir.png){: .mx-auto.d-block :}

### Environment Direction Light

![](https://chaphlagical.github.io/assets/images/assets-img/PathTracing/env_dir.png){: .mx-auto.d-block :}

### Environment Indirection Light

![](https://chaphlagical.github.io/assets/images/assets-img/PathTracing/env_indir.png){: .mx-auto.d-block :}

### Final Rendering

#### 128 spp

![](https://chaphlagical.github.io/assets/images/assets-img/PathTracing/128spp.png){: .mx-auto.d-block :}

#### 1024 spp

![](https://chaphlagical.github.io/assets/images/assets-img/PathTracing/1024spp.png){: .mx-auto.d-block :}

### Other Rendering Result

![](https://chaphlagical.github.io/assets/images/assets-img/PathTracing/ball.png){: .mx-auto.d-block :}

![](https://chaphlagical.github.io/assets/images/assets-img/PathTracing/bunny.png){: .mx-auto.d-block :}

![](https://chaphlagical.github.io/assets/images/assets-img/PathTracing/bunny_dragon.png){: .mx-auto.d-block :}

![](https://chaphlagical.github.io/assets/images/assets-img/PathTracing/sea.png){: .mx-auto.d-block :}

![](https://chaphlagical.github.io/assets/images/assets-img/PathTracing/ryg.png){: .mx-auto.d-block :}

![](https://chaphlagical.github.io/assets/images/assets-img/PathTracing/snow.png){: .mx-auto.d-block :}

![](https://chaphlagical.github.io/assets/images/assets-img/PathTracing/objects.png){: .mx-auto.d-block :}

## Resource

**Project**: [https://github.com/Chaphlagical/USTC_CG/tree/master/Homeworks/9_PathTracing](https://github.com/Chaphlagical/USTC_CG/tree/master/Homeworks/9_PathTracing)

