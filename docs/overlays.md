# **skyCORE-AI Overlays**

skyCORE-AI features a real-time, auto-refreshing overlay system for streamers and users who need live dashboards.

---

## **📺 How It Works**

skyCORE-AI generates and updates a JSON file (`overlay.json`) every 3 seconds using:

- `OverlayAutoRefresher` — updates overlay.json
- HTML/JS frontends — read from overlay.json
- OBS browser sources — render panels in-stream

---

## **🔄 Auto Refresh Loop**

```
from src.overlay_refresh_util import OverlayAutoRefresher
refresher = OverlayAutoRefresher()
refresher.start()
```

This writes:
```
{
  "kills": 5,
  "deaths": 2,
  "status": "LIVE",
  "last_updated": 1710000000
}
```

---

## **🎨 Built-in Panels**

Open:
```
overlays/panel.html
```

This displays:
- Live kill/death stats
- Agent/Twitch status
- Auto-refresh every 3 seconds
- Theme switcher (dark, light, neon)

---

## **📦 OBS Integration**

1. Open OBS
2. Add a **Browser Source**
3. Set URL to:

```
http://localhost:3000/overlays/panel.html
```

Or open the file directly with:
```
file:///absolute/path/to/overlays/panel.html
```

Optional: run a local server:
```
python -m http.server 3000
```

---

## **💬 AI Overlay Control**

Say:
- `show killfeed`
- `add leaderboard to overlay`
- `hide twitch status`

The AI routes these via `overlay_intent_router.py`

---

## **✨ Create Your Own**

Want to design a new overlay?

1. Create a new `overlays/yourfile.html`
2. Load and parse `overlay.json` every 3 seconds
3. Add your styles and visual blocks

You can also use `panel.js`, `panel.css`, or integrate React/Vue if needed.

---

skyCORE-AI overlays are simple, readable, extendable — and 100% OBS ready.