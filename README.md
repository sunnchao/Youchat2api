# Youchat2api
大二非计科第一次尝试逆向哈哈~

注意，当前版本需要桌面环境

## 使用方法

先在浏览器安装一个插件，我用的是这个 [cookie-editor](https://microsoftedge.microsoft.com/addons/detail/cookieeditor/neaplmfkghagebokkhpjpoebhdledlfi?hl=zh-CN)

![image](https://github.com/leezhuuu/Youchat2api/assets/69389053/afbf1f99-3ab1-4946-86c7-9d6778b15c48)

登录 you.com

打开插件，导出cookie为json

![image](https://github.com/leezhuuu/Youchat2api/assets/69389053/94e743af-18a6-42b0-8a32-cd83fd9564bf)

打开这个文件“precookie.json”，用记事本就能打开，将json粘贴进去

![image](https://github.com/leezhuuu/Youchat2api/assets/69389053/ab3ee97b-9632-408d-87ee-df287c5d8136)

运行“autocookie”，会在当前目录下自动创建cookie.json

运行“you”，现在在你的电脑上的2222端口开放了一个api接口，http://127.0.0.1:2222/v1/chat/completions

![image](https://github.com/leezhuuu/Youchat2api/assets/69389053/bf43bff4-18ae-4696-82cc-e23d245064d6)

剩下的懂得都懂🤭

这里附一个我的oneapi重定向规则

```json
{
  "claude-3-haiku": "claude_3_haiku",
  "claude-3-opus": "claude_3_opus",
  "claude-3-sonnet": "claude_3_sonnet",
  "claude-3-haiku-20240307": "claude_3_haiku",
  "claude-3-opus-20240229": "claude_3_opus",
  "claude-3-sonnet-20240229": "claude_3_sonnet",
  "claude-2": "claude_2",
  "claude_2.0": "claude_2",
  "gpt-4":"gpt_4",
  "gpt-4-1106-preview": "gpt_4_turbo",
  "gpt-4-0125-preview": "gpt_4_turbo",
  "gpt-4-turbo-preview": "gpt_4_turbo",
  "gemini-pro": "gemini_pro",
  "gemini-1.5-pro": "gemini_1.5_pro",
  "DBRX-Instruct": "databricks_dbrx_instruct",
  "Command R": "command_r",
  "Command R+": "command_r_plus",
  "Zephyr": "zephyr"
}
```
