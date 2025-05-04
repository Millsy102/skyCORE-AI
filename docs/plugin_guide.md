# **🧩 Plugin Guide — skyCORE-AI OS**

All plugins MUST follow the Golden Rule:

> **Use AI wherever possible — even in the scripts.**

## **🔌 Plugin Structure**

```
plugins/
  ai_gf/
    ai_gf.py
    panel.py
    requirements.txt
    plugin.json
```

## **✅ Required Hooks**

```
use_model("gpt-4")
smart_selector.infer_best("generate")
```

### **🧠 `plugin.json` (Optional)**

```
{
  "name": "ai_gf",
  "version": "1.0.0",
  "author": "YourName",
  "description": "A girlfriend simulation using AI models.",
  "entry": "ai_gf.py"
}
```

---

## **⚙️ AI Usage Checklist**

- ✅ Uses `use_model()` or `infer_best()`  
- ✅ Leverages local/remote LLMs  
- ✅ Can run prompts, generate responses  
- ✅ Integrates with HuggingFace or custom endpoints

---

## **📥 Uploading to Community**

- Pastebin: raw `.py` or `.zip`  
- GitHub: link to `plugin_name/` folder  
- Share on Discord for validation