# **⚙️ Developer Guide — skyCORE-AI OS**

## **🏗️ Repo Layout**

| Path | Purpose |
|------|---------|
`src/core/` | memory, logger, settings  
`src/ai/` | chat engine, model browser  
`src/runtime/` | loader, installer, sandbox  
`src/cloud/` | cloud switches  
`src/network/` | server.py, update logic  
`src/devtools/` | validation, test runners  
`ui/panels/` | All QWidget tab panels

## **🧠 SkyDev: Make Plugins Visually**

- Write your code using AI assistant  
- Customize UI visually in SkyDev IDE  
- Save → test → iterate

## **🔧 Dev Tips**

- Use `start_debug.py` for full console logs  
- Check `logs/runtime.log` on crash  
- All plugin exceptions are caught to log