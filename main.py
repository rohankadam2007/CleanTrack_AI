import os, json, base64, sqlite3, random, requests
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import anthropic
from langchain_anthropic import ChatAnthropic
from langchain.tools import tool
from langchain.agents import create_agent

MODEL = "claude-sonnet-5-5"
client = anthropic.Anthropic()
app = FastAPI()
DB = "cleantrack.db"

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

with db() as con:
    con.execute("""CREATE TABLE IF NOT EXISTS reports(
        id INTEGER PRIMARY KEY AUTOINCREMENT, lat REAL, lng REAL, note TEXT,
        waste_type TEXT, severity INTEGER, near_drain INTEGER, summary TEXT,
        created TEXT DEFAULT CURRENT_TIMESTAMP)""")

# ---------- Claude vision ----------
def analyze_image(data: bytes, media_type: str, note: str) -> dict:
    prompt = ('You analyze photos of waste in a neighborhood. Reply ONLY with JSON: '
              '{"waste_type": "plastic|food|mixed|construction|other", "severity": 1-5, '
              '"near_drain": true/false, "summary": "one short sentence"}. '
              f'Resident note: {note}')
    try:
        r = client.messages.create(
            model=MODEL, max_tokens=300,
            messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type,
                                             "data": base64.b64encode(data).decode()}},
                {"type": "text", "text": prompt}]}])
        text = r.content[0].text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print("vision error:", e)
        return {"waste_type": "mixed", "severity": 3, "near_drain": False,
                "summary": "Automatic analysis unavailable"}

# ---------- LangChain agent tools ----------
@tool
def get_area_reports(lat: float, lng: float) -> str:
    """Get waste reports within about 1 km of a location."""
    rows = db().execute(
        "SELECT waste_type, severity, near_drain, note, created FROM reports "
        "WHERE abs(lat-?)<0.01 AND abs(lng-?)<0.01 ORDER BY id DESC LIMIT 30",
        (lat, lng)).fetchall()
    return json.dumps([dict(r) for r in rows])

@tool
def check_rain_forecast(lat: float, lng: float) -> str:
    """Get rain forecast in mm for today and tomorrow at a location."""
    try:
        r = requests.get("https://api.open-meteo.com/v1/forecast",
                         params={"latitude": lat, "longitude": lng,
                                 "daily": "precipitation_sum", "forecast_days": 2,
                                 "timezone": "auto"}, timeout=10).json()
        return f"Rain in mm (today, tomorrow): {r['daily']['precipitation_sum']}"
    except Exception:
        return "Forecast unavailable"

SYSTEM = ("You are CleanTrack, an assistant for city waste management. Use your tools: "
          "first get_area_reports, then check_rain_forecast. Reply in under 80 words with: "
          "1) the main hotspot problem, 2) drain-blockage risk given the rain forecast, "
          "3) two concrete actions (for example an extra pickup or an extra bin).")

def fallback_insight() -> str:
    rows = db().execute("SELECT waste_type, severity, near_drain, note FROM reports LIMIT 40").fetchall()
    r = client.messages.create(
        model=MODEL, max_tokens=300,
        messages=[{"role": "user", "content": SYSTEM + "\nReports: " + json.dumps([dict(x) for x in rows])}])
    return r.content[0].text

# ---------- Routes ----------
@app.post("/report")
async def report(file: UploadFile = File(...), lat: float = Form(...),
                 lng: float = Form(...), note: str = Form("")):
    data = await file.read()
    a = analyze_image(data, file.content_type or "image/jpeg", note)
    with db() as con:
        con.execute("INSERT INTO reports(lat,lng,note,waste_type,severity,near_drain,summary) VALUES(?,?,?,?,?,?,?)",
                    (lat, lng, note, a.get("waste_type"), int(a.get("severity", 3)),
                     1 if a.get("near_drain") else 0, a.get("summary")))
    return a

@app.get("/reports")
def reports():
    return [dict(r) for r in db().execute("SELECT * FROM reports").fetchall()]

@app.get("/insights")
def insights():
    s = db().execute("SELECT AVG(lat) a, AVG(lng) b, COUNT(*) c FROM reports").fetchone()
    if not s["c"]:
        return {"insight": "No reports yet."}
    q = f"Analyze the waste situation near latitude {s['a']:.5f}, longitude {s['b']:.5f}."
    try:
        agent = create_agent(ChatAnthropic(model=MODEL), tools=[get_area_reports, check_rain_forecast],
                             system_prompt=SYSTEM)
        res = agent.invoke({"messages": [{"role": "user", "content": q}]})
        c = res["messages"][-1].content
        if isinstance(c, list):
            c = " ".join(b.get("text", "") for b in c if isinstance(b, dict))
        return {"insight": c}
    except Exception as e:
        print("agent error:", e)
        return {"insight": fallback_insight()}

@app.post("/seed")
def seed():
    random.seed(1)
    types = ["plastic", "food", "mixed", "construction"]
    with db() as con:
        for _ in range(15):
            con.execute("INSERT INTO reports(lat,lng,note,waste_type,severity,near_drain,summary) VALUES(?,?,?,?,?,?,?)",
                        (12.9716 + random.uniform(-0.002, 0.002), 77.5946 + random.uniform(-0.002, 0.002),
                         "Garbage piling up near drain", random.choice(types), random.randint(3, 5), 1,
                         "Overflowing waste next to the drainage channel"))
    return {"ok": True}

@app.get("/")
def home():
    return FileResponse("static/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")