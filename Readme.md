## 打乱+半透明混合：一种R6直播审核绕过方法

本项目旨在提供一种思路来绕过R6直播审核。

本项目提供了一些用于OBS studio的滤镜，用于将游戏的源画面切碎成小块，然后进行随机打乱，从而让审核者根本不可能从直播画面中看懂在播什么游戏。

### 介绍视频

https://www.bilibili.com/video/BV1au4y1m7GH/

<a href="https://ibb.co/JQbgRWd"><img src="https://i.ibb.co/JQbgRWd/image-20230721225632304.png" alt="image-20230721225632304" border="0" /></a>



### 运行python代码来生成用于打乱画面的UV映射贴图

这部分是本方案的精髓所在。运行gen_random_uv_tex.py中的python代码，将会生成两张贴图。贴图的每个像素储存一个UV坐标。R与G通道储存U坐标，B与A通道储存V坐标，这样UV坐标的精度可以达到16位。

打乱过程的伪代码如下：

```
获取输出像素颜色（屏幕空间uv）：
	新的uv = 采样uv映射贴图（屏幕空间uv）
	返回 采样原始输入（新的uv）
```

python代码生成的两张UV映射贴图是互逆的。所以用另一张贴图就可以实现打乱的逆向操作。

这段python脚本需要依赖`pillow`库和`numpy`库。需要安装依赖才能运行。

如果你不熟悉python，也可以直接使用我生成好的贴图，你可以在`tex_example/` 文件夹中找到。

python脚本中，有几个常量也许需要根据实际情况取值`width`与`height`影响生成的贴图的宽度和高度，这其实不太重要（大概），大点小点应该都行。

`cell_size`用于设置每个马赛克的大小。设置成8意味着每个马赛克的大小是8x8。这个常量的取值**很重要**，取值越小，马赛克越小，图像会被打乱得更彻底。但是图像打乱得越彻底，越不容易压缩，这可能造成额外得比特率开销。如果图像在推流过程中因为压缩而变得模糊，尝试增大该值。

### 使用OBS滤镜来进行直播

obs-shaderfilter插件使得自定义滤镜变得简单。它可以加载HLSL着色器作为滤镜。

你可以在`shader/`文件夹内找到着色器代码，然后通过obs-shaderfilter插件加载着色器。

[点击前往obs-shaderfilter插件项目](https://github.com/Oncorporation/obs-shaderfilter/)

提示：勾选Load shader text from file选项，可以从文件加载HLSL代码。

本项目提供的着色器一览：

- `uv_map.frag` 用于打乱和逆打乱。
  - 参数uv_map应该选择python代码生成的uv映射贴图。打乱和逆打乱应该分别选择成对的贴图。
- `alpha_blend.frag`用于叠加半透明图层。
  - 参数other image 应该选择用于叠加的图片
  - 参数alpha指定不透明度
- `reverse_alpha_blend.frag`是叠加半透明图层的逆运算
  - 参数other image应该设置为与`alpha_blend.frag`相同的图片
  - 参数alpha应该设置为与`alpha_blend.frag`相同的值

### 使用客户端观看直播

未完成，有空再写，欢迎PR。

