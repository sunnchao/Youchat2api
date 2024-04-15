# Youchat2api
大二非计科第一次尝试逆向哈哈~


使用方法

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
![image](https://github.com/leezhuuu/Youchat2api/assets/69389053/78e96c05-1511-4be7-8b02-1d2d47e53522)




以下是chatgpt版本
---

## Youchat2api 设置指南

### 简介
本指南提供逆向工程Youchat2api的分步骤方法，祝您探索愉快！

### 准备工作
- **浏览器插件安装**：首先安装浏览器插件。本指南使用的插件可在[此处](https://github.com/leezhuuu/Youchat2api/assets/69389053/afbf1f99-3ab1-4946-86c7-9d6778b15c48)找到。

### 操作步骤

1. **登录**：访问 you.com 并登录您的账户。

2. **导出Cookie**：
   - 激活已安装的插件，并以JSON格式导出Cookie。此步骤的视觉指南可以在[这里](https://github.com/leezhuuu/Youchat2api/assets/69389053/94e743af-18a6-42b0-8a32-cd83fd9564bf)查看。

3. **编辑导出的文件**：
   - 使用记事本或其他简单文本编辑器打开导出的文件。
   - 将JSON内容复制粘贴进编辑器。此步骤的操作说明可在[此处](https://github.com/leezhuuu/Youchat2api/assets/69389053/ab3ee97b-9632-408d-87ee-df287c5d8136)找到。

4. **运行 `autocookie`**：
   - 执行`autocookie`脚本。这将在当前目录下自动生成一个`cookie.json`文件。

5. **启动API**：
   - 运行`you`脚本以启动API。API将在您的本地机器上的`http://127.0.0.1:2222/v1/chat/completions`地址可用。
   - 此过程的视觉指导可在[这里](https://github.com/leezhuuu/Youchat2api/assets/69389053/bf43bff4-18ae-4696-82cc-e23d245064d6)查看。

### 注意
API设置完成后，熟悉此类系统的用户应该知道接下来该做什么！

---
