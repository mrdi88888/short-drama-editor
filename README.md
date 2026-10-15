# short-drama-editor

一个最小可运行的 AI 短剧自动剪辑项目基础版。

当前版本使用 Python 调用本机 ffmpeg 完成一次基础剪辑：

1. 读取输入目录中的视频素材；
2. 按文件名排序；
3. 每个素材截取前几秒（默认 5 秒）；
4. 统一为 30 FPS、H.264、MP4；
5. 按排序结果拼接为一个输出视频。

## 环境要求

- Python 3.9+
- ffmpeg（命令行可直接执行 ffmpeg -version）

Python 依赖写在 requirements.txt 中。本版本只使用 Python 标准库，不需要安装第三方包。

## 使用

把素材放入 素材 目录，然后运行：

~~~bash
python short_drama_editor.py 素材 -o output.mp4
~~~

每个素材截取前 5 秒。可以调整时长：

~~~bash
python short_drama_editor.py 素材 --seconds 8 -o output.mp4
~~~

默认输出无声音，以避免不同素材音频格式导致拼接失败。如果需要保留音频：

~~~bash
python short_drama_editor.py 素材 --seconds 5 --keep-audio -o output.mp4
~~~

也可以查看命令帮助：

~~~bash
python short_drama_editor.py --help
~~~

支持的输入格式：.mp4、.mov、.m4v、.avi、.mkv、.webm。

## 目录

~~~text
.
├── short_drama_editor.py
├── requirements.txt
└── README.md
~~~

这是规则剪辑的最小基础版本，后续可以在此基础上加入镜头检测、语音转文字、字幕和 AI 选段。
