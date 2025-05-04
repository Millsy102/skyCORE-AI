# **skyCORE-AI Cloud Sync & Agent Config**

skyCORE-AI supports optional cloud config and agent settings via:

- `skycore_cloud.json`
- AI agent routing context
- Webhook push/pull

---

## **☁️ Cloud Config Storage**

skyCORE-AI stores persistent settings in:

```
config/skycore_cloud.json
```

Example contents:
```
{
  "sync_enabled": true,
  "webhook": "https://your-endpoint.com/webhook",
  "preferred_agent": "SkyDev",
  "overlays_enabled": true
}
```

---

## **🔄 Webhook Sync**

You can push your config to the cloud using:

- Settings tab → **"Push to Cloud"**
- AI chat → `sync config` or `push config now`

skyCORE-AI sends `twitch.json` or other payloads via POST.

---

## **🧠 Agent Routing**

skyCORE-AI uses agent names for context-aware responses.

In chat:
- Set agent: `SkyDev`, `StreamBot`, `Companion`
- Typed in the `ChatTab` via the **Agent Routing** box

Agents affect:
- Plugin selection
- Prompt interpretation
- Overlay rendering logic

---

## **🔌 Plugin Use**

Plugins can store config here too:

```
from src.cloud_config_store import CloudConfigStore
store = CloudConfigStore()
store.set("plugin_setting", "value")
```

---

## **💾 Local vs Cloud**

You can use cloud config for:
- Syncing your settings across machines
- Remote agent config updates
- Backup/recovery

Your `cloud.json` is stored safely in `config/` and only syncs when triggered.

---

skyCORE-AI gives you power to script, store, and sync everything you do — from one cockpit.