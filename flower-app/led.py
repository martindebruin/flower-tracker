import os
import asyncio

async def _send_to_matrix(message: str):
    from aioesphomeapi import APIClient
    host = os.getenv('ESP32_HOST')
    key = os.getenv('ESP32_KEY')
    client = APIClient(host, 6053, "", noise_psk=key)
    await client.connect(login=True)
    _, services = await client.list_entities_services()
    svc = next(s for s in services if s.name == "set_text")
    res = client.execute_service(svc, {"msg": message})
    if asyncio.iscoroutine(res):
        await res
    await asyncio.sleep(0.3)
    await client.disconnect()

def notify_if_dry(tradescantia: str, african_milk_bush: str, spansk_timjan: str, palettbladen: str):
    messages = []
    if tradescantia == "dry":
        messages.append("VATTNA TRADESCANTIA")
    if african_milk_bush == "dry":
        messages.append("VATTNA AFRICAN MILK BUSH")
    if spansk_timjan == "dry":
        messages.append("VATTNA SPANSK TIMJAN")
    if palettbladen == "dry":
        messages.append("VATTNA PALETTBLADEN")
    combined = "  ".join(messages) if messages else "JUST YOLO IT"
    asyncio.run(_send_to_matrix(combined))
