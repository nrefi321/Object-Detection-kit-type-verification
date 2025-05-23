from fastapi import FastAPI, Request
import threading
import uvicorn

from main_AI import AIProcess

app = FastAPI()
ai = AIProcess(use_mqtt=True)

@app.post("/saveimgpath")
async def save_img_path(request: Request):
    data = await request.json()
    file_path = data.get("path")
    if file_path:
        ai.onSaveImgPath(file_path)
        return {"status": "received", "path": file_path}
    return {"status": "error", "message": "No 'path' field in JSON"}

# Run ai.aiProc in a background thread
def start_ai():
    try:
        ai.aiProc()
    except KeyboardInterrupt:
        print('Interrupted by user')
        ai.disconnectMQTT()
    except Exception as e:
        print(f'Error: {e}')
        ai.disconnectMQTT()
    finally:
        print('End of program')


threading.Thread(target=start_ai, daemon=True).start()

if __name__ == "__main__":
    uvicorn.run("apiServer:app", host="0.0.0.0", port=8888, reload=False)
