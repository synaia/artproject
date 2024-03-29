# import os
# from typing import List
# import uvicorn
#
# from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect
# from fastapi.responses import HTMLResponse
# from fastapi.middleware.cors import CORSMiddleware
# from aiocache import Cache
# import asyncio
#
# from server.core_app.websocket.connectionmanager import ConnectionManager, send_periodically
#
# router = APIRouter(prefix='/products', tags=['products'])
# myvar = Cache(Cache.MEMORY)
#
#
# @router.on_event("startup")
# async def startup_event():
#     print('startup ws module ...... ')
#     # await myvar.set('sharable', 'Wilton')
#     # await myvar.set('sharable_per_client', list())
#     # await myvar.set('client_id_list', list())
#
#
# html = """
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#     </head>
#     <body>
#         <h1>WebSocket Chat</h1>
#         <h2>Your ID: <span id="ws-id"></span></h2>
#         <form action="" onsubmit="sendMessage(event)">
#             <input type="text" id="messageText" autocomplete="off"/>
#             <button>Send</button>
#         </form>
#         <ul id='messages'>
#         </ul>
#         <script>
#             var client_id = Date.now()
#             document.querySelector("#ws-id").textContent = client_id;
#             var ws = new WebSocket(`wss://localhost:8001/ws/${client_id}`);
#             ws.onmessage = function(event) {
#                 var messages = document.getElementById('messages')
#                 var message = document.createElement('li')
#                 var content = document.createTextNode(event.data)
#                 message.appendChild(content)
#                 messages.appendChild(message)
#             };
#             function sendMessage(event) {
#                 var input = document.getElementById("messageText")
#                 ws.send(input.value)
#                 input.value = ''
#                 event.preventDefault()
#             }
#         </script>
#     </body>
# </html>
# """
#
# manager = ConnectionManager()
#
#
# @app.get("/")
# async def get():
#     return HTMLResponse(html)
#
#
# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     await manager.connect(websocket, client_id)
#     await websocket.send_json({'Welcome nigga':  client_id})
#     await asyncio.create_task(send_periodically(websocket, manager, client_id, 0.9))
#
#     # try:
#     #     while True:
#     #         data = await websocket.receive_text()
#     #         await manager.send_personal_message(f"You wrote: {data}", websocket)
#     #         await manager.broadcast(f"Client #{client_id} says: {data}, CacheVar: {await myvar.get('sharable')}")
#     # except WebSocketDisconnect:
#     #     manager.disconnect(websocket)
#     #     await manager.broadcast(f"Client #{client_id} left the chat")
#
#
# async def send_periodically(websocket, manager, client_id,  timer):
#     try:
#         while True:
#             sharable_per_client = await myvar.get('sharable_per_client')
#             sharable = [value for value in sharable_per_client if value['client_id'] == client_id]
#             if len(sharable) > 0:    # some info for sent to client_id ?
#                 await manager.send_personal_message(sharable[0], websocket)
#                 # purge sharable client_id recently sent.
#                 sharable_per_client_copy = [value for value in sharable_per_client if value['client_id'] != client_id]
#                 await myvar.set('sharable_per_client', sharable_per_client_copy)
#             await asyncio.sleep(timer)
#     except WebSocketDisconnect:
#         await manager.disconnect(websocket, client_id)
#         # await manager.broadcast(f"Client #{client_id} left the chat")
#
#
# @app.websocket("/ws2/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     await manager.connect(websocket)
#     data = await websocket.receive_text()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.send_personal_message(f"You wrote: {data}", websocket)
#             await manager.broadcast(f"Client #{client_id} says: {data}, CacheVar: {await myvar.get('sharable')}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Client #{client_id} left the chat")
#
#
# @app.post("/newval")
# async def change_value(newval: str):
#     sample_product = {
#         "id": 9,
#         "name": "Iron Whey Arnold - 5lb (copia)",
#         "cost": 0,
#         "price": newval,
#         "quantity": 1,
#         "quantity_for_sale": 1,
#         "price_for_sale": newval,
#         "margin": 3100,
#         "code": " ",
#         "img_path": " ",
#         "date_create": "2017-02-27T23:27:52",
#         "active": 0,
#         "image_raw": None
#     }
#     await myvar.set('sharable', sample_product)
#     client_id_list = await myvar.get('client_id_list')
#     sharable_per_client = await myvar.get('sharable_per_client')
#     for id in client_id_list:
#         sharable_per_client.append({'client_id': id, 'sharable': sample_product})
#         await myvar.set('sharable_per_client', sharable_per_client)
#
#     return {'message': await myvar.get('sharable')}
#
#
# # debug mode :-)
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8001, ssl_keyfile=key_pem, ssl_certfile=public_pem)
