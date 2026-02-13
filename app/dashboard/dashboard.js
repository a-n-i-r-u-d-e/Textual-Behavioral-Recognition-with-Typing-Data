async function updateMonitor() {
    const res = await fetch("http://127.0.0.1:8000/monitor");
    const data = await res.json();
    document.getElementById("events").innerText = data.total_events;
}

async function updateStats() {
    const res = await fetch("http://127.0.0.1:8000/stats");
    const data = await res.json();
    document.getElementById("keys").innerText = data.key_events;
}

setInterval(updateMonitor, 1000);
setInterval(updateStats, 2000);
