import os
import aiohttp
from aiohttp import web

LOCAL_FILE_PATH = r"C:\MyFileServer\shared\test.txt"

async def home(request):
    return web.Response(text="App Service is running!")

async def read_file(request):
    try:
        file_server_url = os.environ.get("FILE_SERVER_URL")
        if file_server_url:
            async with aiohttp.ClientSession() as session:
                async with session.get(file_server_url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    text = await resp.text()
                    return web.Response(text=text)
        else:
            with open(LOCAL_FILE_PATH, "r") as f:
                return web.Response(text=f.read())
    except Exception as e:
        return web.Response(text=f"Error: {str(e)}", status=500)

app = web.Application()
app.router.add_get("/", home)
app.router.add_get("/read-file", read_file)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8080)