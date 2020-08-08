---
layout: post
title: Taichi Simulation
thumbnail-img: /assets/images/thumbnail-img/taichi.png
cover-img: /assets/images/cover-img/CG.png
comments: true
gh-repo: Chaphlagical/USTC_CG
gh-badge: [star, fork, follow]
tags: [CG, Physics Simulation]
comments: true
---

Physics Simulation based on Taichi

## Feature

* Physics Simulation based on Taichi

## Development Environment

* **IDE**: Microsoft Visual Studio 2019 community
* **Build**: CMake 3.16.3
* **other 3rd Party Library**: Taichi

## Algorithm Introduction

### MLS-MPM Algorithm Pipeline

![process](D:\USTC_CG\Homeworks\7_SimulationTaichi\report\Figures\process.png)

### From Particle Interpolation to Grid Point

**Interpolation Function**

$$
N(x)=\begin{cases}

\frac{1}{2}|x|^3-x^2+\frac{2}{3}&0\leq |x|<1\\

-\frac{1}{6}|x|^3+x^2-2|x|+\frac{4}{3}&1\leq |x|<2\\

0&2\leq |x|

\end{cases}
$$

**B-Spline Function Properties**:

$$
\sum\limits_i w_{ip}=1
$$

$$
\sum\limits_i w_{ip}\boldsymbol x_i=\boldsymbol x_p
$$

**Computing Mass of Grid Point **:

Interpolation of Mass:

$$
m_i^n=\sum\limits_p w_{ip}^nm_p^0
$$

Conservation of Mass

$$
\sum\limits_i m_i^n=\sum\limits_i\sum\limits_p w_{ip}^nm_p^0=\sum\limits_p\left(\sum\limits_i w_{ip}^n\right)m_p^0=\sum\limits_p m_p^0
$$

**Computing Grid Point Speed**:

Interpolation of Momentum

$$
m_i^n \boldsymbol v_i^n=\sum\limits_p w_{ip}^nm_p^0(\boldsymbol v_p^n+\boldsymbol C_p^{n+1}(x_i^n-x_i^p))
$$

$$
\boldsymbol C_p=\boldsymbol B_p(\boldsymbol D_p)^{-1}
$$

$$
\boldsymbol B_p=\sum\limits_iw_{ip}\boldsymbol v_i(x_i-x_p)^T
$$

$$
\boldsymbol D_p=\sum\limits_i w_{ip}\boldsymbol v_i(x_i-x_p)(x_i-x_p)^T
$$

Computing Grid Point Speed

$$
\boldsymbol v_i^n=\frac{m_i^n\boldsymbol v_i^n}{m_i^n}
$$

### Update Information of Grid Point

**Grid Force Calculation**

$$
\boldsymbol f_i^n=-\frac{\partial \Psi^n}{\partial \boldsymbol x_i^n}=-\sum\limits_p N_i(x_p^n)V_p^0M_p^{-1}\frac{\partial \psi_p^n(F_p^n)}{\partial \boldsymbol x_i^n}(x_i^n-x_i^p)
$$

**Update Grid Point Speed**

$$
v_i^{n+1}=v_i^n+\frac{\boldsymbol f_i^n+\boldsymbol f^n_{iext}}{m_i^n}\Delta t
$$

**Handling Collision**

Only dealing with the grid points near the boundary

### From Grid Point Interpolation to Particles

**Speed of Particles**

Speed Interpolation:

$$
\boldsymbol v_p^{n+1}=\sum\limits_iw_{ip}^n\boldsymbol v_i^{n+1}
$$

### Update Particles Information

**Update Particles Position**

$$
\boldsymbol x_p^{n+1}=\boldsymbol x_p^n+\boldsymbol v_p^{n+1}\Delta t
$$

**Update Deformation Gradient**

$$
F_p^{n+1}=(I+\Delta t\boldsymbol C_p^{n+1})F_p^n
$$

## Demo

### Water Fountain

<video width="50%" height="50%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/Taichi/water_fountain.mp4" type="video/mp4">
      </video>
### Colorful Fountain

<video width="50%" height="50%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/Taichi/three_fountain.mp4" type="video/mp4">
      </video>

### Material Fountain

<video width="50%" height="50%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/Taichi/material_fountain.mp4" type="video/mp4">
      </video>

### Fountain vs Jelly Cube

<video width="50%" height="50%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/Taichi/fountain_vs_jelly_cube.mp4" type="video/mp4">
      </video>
### Jelly Horse

<video width="70%" height="70%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/Taichi/jelly_horse.mp4" type="video/mp4">
      </video>

### Different Young's Modulus for jelly

<video width="100%" height="100%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/Taichi/Jelly_E.mp4" type="video/mp4">
      </video>

### Different Young's Modulus for snow

<video width="100%" height="100%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/Taichi/different_E.mp4" type="video/mp4">
      </video>

### Different velocity

<video width="70%" height="70%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/Taichi/different_speed.mp4" type="video/mp4">
      </video>
### Different particals number

#### Jelly

<video width="70%" height="70%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/Taichi/jelly_partical_num.mp4" type="video/mp4">
      </video>
#### Snow

<video width="70%" height="70%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/Taichi/snow_partical_num.mp4" type="video/mp4">
      </video>

#### Fluid

<video width="70%" height="70%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/Taichi/fluid_partical_num.mp4" type="video/mp4">
      </video>

### Balls of different materials hitting

<video width="100%" height="100%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/Taichi/ball_hit.mp4" type="video/mp4">
      </video>

### Jelly ball hit other material

<video width="100%" height="100%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/Taichi/jelly_hit.mp4" type="video/mp4">
      </video>
### Different shapes hit fluid

<video width="70%" height="70%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/Taichi/shape_hit_fluid.mp4" type="video/mp4">
      </video>

### Demo1

<video width="100%" height="100%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/Taichi/blender_fluid.mp4" type="video/mp4">
      </video>

### Demo2

<video width="100%" height="100%" id="video" controls="" preload="none" poster="">
      <source id="mp4" src="https://chaphlagical.github.io/assets/videos/Taichi/blender_fluid2.mp4" type="video/mp4">
      </video>