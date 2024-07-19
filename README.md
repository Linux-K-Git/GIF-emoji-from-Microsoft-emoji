![1](https://github.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/blob/master/assets/images/banner.gif)
# 将微软3D动态emoji转换为GIF格式以方便在各种地方使用的项目 as Animated Fluent Emojis
# Project to convert Microsoft 3D animated emoji to GIF format for easy use in various places as Animated Fluent Emojis

Microsoft Teams (3D Animated) to GIF
as Animated Fluent Emojis

![showcase 5](https://github.com/user-attachments/assets/fe3a7413-8368-45e9-a08a-0c5832a70b6d)

这是一个使用微软Teams Emoji在2021年的世界表情符号日 (World Emoji Day) 推出了其全新的3D流畅设计Emoji表情符号集。这个集合中包含了超过800种的emoji表情动画设计，甚至包含了Unicode没有的表情符号，例如 emo、Cool Monkey、双性恋旗帜等
This is a use of Microsoft Teams Emoji has launched its new 3D Fluid Design Emoji Emoji collection on World Emoji Day (WED) 2021. The collection includes more than 800 animated emoji designs, and even includes emoji that are not available in Unicode, such as emo, Cool Monkey, bisexual flag, and more!

Microsoft Teams (3D Animated) 
参考链接：

Reference Links:

https://emojipedia.org/microsoft-teams

https://www.emojiall.com/zh-hans/platform-microsoftteams

该项目使用Python 3.X代码实现从微软开源表情中读取前端生成的流畅动画录制为GIF格式动图
The project uses Python 3.X code to achieve from the Microsoft open source expression to read the front-end generated smooth animation recorded as a GIF format motion graphics

可从以下项目中的demo里选择表情复制link并下载转换为可自定义大小、帧率、批量下载、代理下载为GIF格式动图
You can select emoji from the following project demo to copy link and download to convert to customizable size, frame rate, batch download, proxy download as GIF format animated graphics

![showcase 1](https://github.com/user-attachments/assets/c9737d11-ea9c-4541-b3a4-3cee2a486e2f)

适用的项目链接：

Applicable project links:
    
https://github.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis
    
https://animated-fluent-emoji.vercel.app/

---

使用教程：

1.确保自己的python版本≥3.8

2.`pip install requests pillow numpy`

3.`python XXX.py`

4.在终端粘贴link/在代码同一目录下创建url.txt写入需要下载的url，url格式必须包含src=xxxxxxx,详见1-6版本代码注释

---

Use the tutorial:

1. Make sure you have python version ≥ 3.8.

2. `pip install requests pillow numpy`

3. `python XXX.py`

4. In the terminal paste link / in the same directory as the code to create url.txt write the url need to download, the url format must contain src = xxxxxxxx, see version 1-6 of the code notes

---

## 如果你仍然觉得之前的流程难以复现，那么可以前去Releases页面下载最新的已经转换好的常用GIF，包含两种分辨率256\*256和64\*64的30fps 488个 GIF动图
If you still find the previous process difficult to reproduce, then you can go to the Releases page to download the latest converted common GIFs, including two resolutions 256\*256 and 64\*64 30fps 488 GIFS animations.

![QQ_1721285704856](https://github.com/user-attachments/assets/d988173c-e26e-46de-a3bd-bccaa8d3096b)

### 如果你认为这种办法得到的图像质量仍不够高，那么可以看下面我使用的另一种方法，在之前我考虑到一个一个下载仍然比较繁琐，还容易出现错误（如果你自信你的网络很靠谱，当我没说），那么我如果使用程序算法来直接实现将APNG图片直接转换为GIF格式呢？也就是源代码中的 `APNG2GIF.py` 文件实现了这一点，但是，令人意外的事情发生了，微软给出的图片动画中并没有完全一致的按照统一规范的逻辑进行绘制，在某些表情中出现了一些特殊效果如闪烁等,导致这个转换算法也没法处理所有的图片，出现了个别几个图的透明度处理不正常的情况（虽然连十个都没有）
If you think that this approach is still not enough to get high quality images, then you can see below the other method I use, before I consider one by one download is still cumbersome, but also prone to errors (if you are confident that your network is very reliable, when I did not say), so if I use the program algorithms to directly implement the APNG image directly into the GIF format? That is, the source code in the `APNG2GIF.py` file to achieve this, but, surprising things happen, Microsoft gives the picture animation is not completely consistent in accordance with the unified specification of the logic of the drawing, in some of the expression of some special effects such as blinking, etc., resulting in the conversion algorithm can not deal with all of the picture, there are a few individual pictures of the transparency of the processing is not normal (although even ten). There are a few cases where the transparency of a few pictures is not normal (although there are not even ten).

`APNG2GIF.py`,这是一个使用python代码实现APNG转换位GIF图像格式的快速解决脚本，调用几乎所有的CPU线程资源在短时间内迅速转换，而不需要之前方法一个一个下载录制，但也不是完美的

当然，这只是一个简单的示例，如果你希望每一个图片都能很好的转换，那么可以去参考如：APNG to GIF、FFMPEG、APNGToGifConverter等转换工具或在线网站，它们有着更为成熟的转换能力，由于版权问题我不能将他们的链接写在我的项目里，但是你可以通过搜索引擎找到它们。
Of course, this is just a simple example, if you want every image can be converted well, then you can refer to conversion tools or online websites such as “ APNG to GIF, FFMPEG, APNGToGifConverter……”, which have more mature conversion ability, due to the copyright issue I can't write their links in my project, but you can find them through search engines.

### 关于图像质量下降的原因是GIF的色深只有8位，即只有2的8次幂，也就是256种颜色，这远达不到我们对“足够好看”图片的色彩的需要。而微软开源出的动画里使用的APNG格式支持24位真彩色和8位透明度，这也是为什么转成GIF会失真的原因。所以无论是录制还是转换均会出现一定程度的色彩丢失。The reason for the loss of image quality is that the color depth of a GIF is only 8 bits, i.e., only 2 to the 8th power, i.e., 256 colors, which is far less than what we need for a “good-looking” image. The APNG format used in Microsoft's open-source animation supports 24-bit true color and 8-bit transparency, which is why it will be distorted when converted to GIF. So both recording and conversion will have some degree of color loss.

#### 如其他有问题或疑问请提交issue，开发者会尽可能及时回复你的需求。
If you have another problems or questions, please submit an issue and the developers will try to respond to your request in a timely manner.

#### 如果引用该项目的人能给它一颗星，我将不胜感激。
I'd appreciate it if the person who cited the item would give it a star, please.

版权所有 2024 Linux-K

Copyright 2024 Linux-K
