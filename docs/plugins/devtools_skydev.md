# 🧩 Plugin: devtools_skydev

## Metadata
```yaml
name: DevTools for SkyDev
version: 1.0
author: skyCORE-AI
description: Plugin creator, linter, tester for SkyDev.
```

## UI Layout
```yaml
layout: vertical
fields:
  - name: Create Plugin
    type: button
    action: builder/plugin_maker.py
  - name: Lint Plugin
    type: button
    action: builder/plugin_linter.py
  - name: Test Plugin
    type: button
    action: builder/plugin_tester.py
```

## Main Logic
```
def run():
```