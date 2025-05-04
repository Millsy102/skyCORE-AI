# **🧩 skyCORE-AI Plugin Development**

Any valid Python project can become a skyCORE-AI plugin by following these guidelines:

## **🔽 Plugin Structure**

```
myplugin/
├── main.py           # Entry point, must contain functions
├── config.yaml       # Settings
├── ui.yaml           # Optional UI layout
├── test.py           # Optional plugin tests
```

## **📜 config.yaml**

```
name: MyPlugin
author: You
version: 1.0
description: A demo plugin.
```

## **🎨 ui.yaml Example**

```
fields:
  - type: text
    label: Username
  - type: checkbox
    label: Enable Feature
  - type: button
    label: Run
```

## **🚀 Load Plugin**

1. Zip your plugin folder.
2. Drop it into `/plugins_zips/`
3. skyCORE-AI will extract and register it.

## **🧠 Call It**

Use slash command in chat:
```
/plugin myplugin start
```