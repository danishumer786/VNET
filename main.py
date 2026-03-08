from aiohttp import web
import os

# Local: reads file from disk
# Azure: fetches file over HTTP from your laptop's Tailscale IP
FILE_SERVER_URL = os.environ.get("FILE_SERVER_URL", "")
LOCAL_FILE_PATH = r"C:\MyFileServer\shared\test.txt"


async def home(request):
    return web.Response(text="App Service is running!")


async def read_file(request):
    if FILE_SERVER_URL:
        # Azure mode: fetch file over HTTP tunnel
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(FILE_SERVER_URL) as resp:
                content = await resp.text()
        return web.Response(text=content)
    else:
        # Local mode: read directly from disk
        with open(LOCAL_FILE_PATH, "r") as f:
            content = f.read()
        return web.Response(text=content)


app = web.Application()
app.router.add_get("/", home)
app.router.add_get("/read-file", read_file)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    web.run_app(app, host="0.0.0.0", port=port)
