---
layout: post
title: UE5 Prediction I
subtitle: Overview
thumbnail-img: /assets/images/thumbnail-img/resource.jpg
cover-img: /assets/images/cover-img/resource.jpg
comments: true
tags: [CG] [Game Engine]
readtime: true
---

<iframe src="//player.bilibili.com/player.html?aid=498190004&bvid=BV1BK411W75W&cid=190794216&page=1" scrolling="no" border="no" frameborder="no" framespacing="0" width="640" height="430" allowfullscreen="true"> </iframe>

Demo中展示了很多东西，涵盖游戏引擎的方方面面：声音系统、物理系统、光照系统……但其中最让人惊艳的还是开头Brian和Jerome所说的两大难题解决方案：Lumen和Nanite，后续我也将具体调研这两个方向。

接下来先简单讲讲Lumen和Nanite所实现的功能的对次世代游戏开发的意义

## Lumen：全局动态光照系统

初中物理光学部分我们就了解到，生物的视觉成像原理是物体的反射光通过晶状体折射成像于视网膜上，再由视觉神经感知传给大脑，从而使生物能够看见物体。在图形学中的光照渲染也是利用类似的道理，由于现实情况的光照极其复杂，在进行计算机渲染时常常会进行一系列的简化。光照模型通常分为两种：局部光照模型和全局光照模型。

局部光照模型是对自然界的光照进行大量简化得到的，主要包括三个项：环境光、漫反射和镜面反射，且不考虑光线多次反射的现象，如下图：

![](https://chaphlagical.github.io/assets/images/assets-img/ue5_overview.assets/image-20200913070744719.png){: .mx-auto.d-block :}

其中，光强$I=k_aI_a+K_dI_d\pmb l\cdot\pmb n+k_sl_s(\pmb v\cdot\pmb r)^\alpha$

* $\pmb n$，$\pmb l$，$\pmb v$，$\pmb r$分别为法向、入射光方向的反向、反射点到视点的向量方向、反射光方向

* $K_aI_a$：环境光项，模拟多次反射后的效果的近似，为常值
* $K_dI_d\pmb l\cdot\pmb n$：漫反射项，模拟粗糙表面，光向各个方向均匀地反射，从视点看，反射光的比例正比于入射光的竖直分量 
* $k_sl_s(\pmb v\cdot\pmb r)^\alpha$：镜面反射项，模拟在镜面反射方向附近的聚集光现象，$\alpha$的取值可近似模拟出金属和非金属材料的效果

一个简单的Phong局部光照效果如下：

![image-20200913073823778](https://chaphlagical.github.io/assets/images/assets-img/ue5_overview.assets/image-20200913073823778.png){: .mx-auto.d-block :}

除了Phong模型，也可以使用高度简化的PBR渲染方法，如：

![image-20200913080753908](https://chaphlagical.github.io/assets/images/assets-img/ue5_overview.assets/image-20200913080753908.png){: .mx-auto.d-block :}

尽管简化PBR局部光照模型也能得到还可以的效果，但依旧存在很多局限性，如阴影、遮挡、反射、透射等效果无法直接生成。

前面讲到的局部光照模型基本都是围绕光源——着色点——视点进行简化计算的，期间不涉及光线的多次反射，而现实情况中，进入我们眼睛的光往往是光源经过无数次反射折射后的结果

![](https://chaphlagical.github.io/assets/images/assets-img/ue5_overview.assets/image-20200913074928872.png){: .mx-auto.d-block :}

为实现真实感渲染效果，我们也需要将多次反射的光线纳入考虑，这种光线称之为间接光，而局部光照模型中的一次反射光称为直接光，我们的最终结果即为直接光+间接光，来看一组基于光线追踪的全局光照渲染的分解过程：

光源直接光渲染：

![img](https://chaphlagical.github.io/assets/images/assets-img/ue5_overview.assets/area_dir.png){: .mx-auto.d-block :}

光源间接光渲染：

![img](https://chaphlagical.github.io/assets/images/assets-img/ue5_overview.assets/area_indir.png){: .mx-auto.d-block :}

环境直接光渲染：

![img](https://chaphlagical.github.io/assets/images/assets-img/ue5_overview.assets/env_dir.png){: .mx-auto.d-block :}

环境间接光渲染：

![img](https://chaphlagical.github.io/assets/images/assets-img/ue5_overview.assets/env_indir.png){: .mx-auto.d-block :}

最终渲染结果：

![img](https://chaphlagical.github.io/assets/images/assets-img/ue5_overview.assets/1024spp.png){: .mx-auto.d-block :}

现在目前的诸多全局光照方法的核心是如何更好更快更准确地求解渲染方程：
$$
L(\pmb x,\pmb \omega)=L_e(\pmb x,\pmb \omega)+L_r(\pmb x,\pmb \omega)\int_{\Omega_{\pmb x}}L_i(\pmb x,\pmb \omega_i)f_r(\pmb x,\pmb \omega_i\leftrightarrow \pmb \omega)\cos\theta_i\mathrm d\omega_i
$$
即出射光=散射光+反射光，而出射光也将作为入射光打到另外一个物体，参与又一个渲染方程的计算，直到光线射入我们的视点，此时便可计算出该光线对应的像素着色

由于光线和场景的复杂性，计算间接光的开销比直接光大得多，在离线渲染中，常常使用光线追踪等算法进行全局光照渲染。但在游戏中由于存在实时要求，也有一些方法对间接光进行简化。游戏中的全局光照通常分为两种：静态全局光照和动态全局光照

静态全局光照通过离线渲染方法对固定光源、固定场景的全局光照进行计算，将最终的计算结果保存在一张贴图中（如下图），这步称为光照贴图的烘培。有了光照贴图之后就很简单了，可以在游戏中直接采样贴图得到全局光照信息。但这种方法要求光源和场景不能改变，一旦发生变化即要重新烘培，故适用范围有限。

![img](https://chaphlagical.github.io/assets/images/assets-img/ue5_overview.assets/v2-ce3d6d9930e4deba6cdf929c3cbc020a_1440w.jpg){: .mx-auto.d-block :}

动态全局光照方法无需事先烘培光照贴图，能够在游戏运行过程中实时渲染出全局光照，这在当前依旧是实时渲染界的研究热点，在有限硬件条件下渲染出高质量的画面。业界主流有硬件支持实时光线追踪、体素锥体追踪、辐射度算法等方法。而UE5作为跨平台的游戏引擎，需要兼容不同的设备类型，自然不大可能有光追硬件的依赖，因此各大大佬也在猜测Lumen的核心和体素锥体追踪算法比较接近，作为一个刚入门的新手，也只能举手赞成，之后可能将细讲体素锥体追踪算法。

## Nanite： 虚拟化几何体系统

一开始Nanite的着实秀的我头皮发麻，每帧数十亿三角形面片数，光是数据吞吐和存储就很难了，不过视频里提到的虚拟化也意味着虽然Nanite是直接导入高模就可以进行渲染，但不意味着每一帧都会把这些高模全部渲染出来，具体细节下一篇文将讨论，这里就简单介绍一下目前游戏界主流的对几何模型的处理方法。

首先有必要了解一下渲染管线方面的东西，下图是OpenGL的一个可编程渲染管线：

![img](https://chaphlagical.github.io/assets/images/assets-img/ue5_overview.assets/pipeline.png){: .mx-auto.d-block :}

这便是一个完整光栅化渲染的过程，模型顶点数、三角面片数越多，这个过程中所需的计算量、存储量越大，帧率越低。为在保证视觉效果的前提下尽可能减少数据量，游戏中常常使用一种叫多细节层次模型的方法（LOD： Level of Detail）

![](https://chaphlagical.github.io/assets/images/assets-img/ue5_overview.assets/timg){: .mx-auto.d-block :}

利用高模创建出一系列低模，计算视点到模型的距离，切换模型LOD。当视点离模型较远的时候使用低模，当视点离模型较近时使用高模，但这种方法的缺点在于高模与低模之间的切换往往不是连续的，有时会很明显地感觉到模型由模糊变清晰的过程，同时也增加了美工工作人员的工作量

![img](https://chaphlagical.github.io/assets/images/assets-img/ue5_overview.assets/v2-0323e0db3986e136f7f8a8a6a4bac3cd_720w.jpg){: .mx-auto.d-block :}

Nanite的意义在于可以无需手动创建LOD，大大减少了美工人员的工作量，而且在Demo中也展示了非常好的效果。它所用的技术很有可能是基于计算共形几何的Geometry Image方法和Tessellation，后续将详细讨论

当然，UE5的项目在很早的时候就开始了，与其说是技术创新，事实上更多的是前沿技术的集成，所以虽然Epic官方暂未公布UE5技术细节，其核心实现也离不开近几年提出的理论和方法，在调研拼凑自己的猜测的同时，也是十分期待官方细节发布！

