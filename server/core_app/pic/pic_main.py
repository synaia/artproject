import os
import sys

from fastapi import APIRouter, Depends, HTTPException, Security, Header, status
from fastapi import UploadFile, Response, WebSocket, WebSocketDisconnect
from server.core_app.ext.remove_bg import remove_it
from aiocache import Cache
import asyncio

from server.core_app.dbfs.Query import Query
from server.core_app.websocket.connectionmanager import ConnectionManager, send_periodically

router = APIRouter(prefix='/pic', tags=['pic'])
myvar = Cache(Cache.MEMORY)


@router.on_event("startup")
async def startup_event():
    print('Router: Init startup_event....')
    # query = get_query()
    await myvar.set('sharable', {'image_base64': None})
    await myvar.set('sharable_per_client', list())
    await myvar.set('client_uuid_list', list())
    print()


@router.post("/yup",)
async def uploadfilelocal(file: UploadFile):
    image_base64 = remove_it(file.file._file)
    return image_base64


###################################################
#  Web Socket Part
###################################################

@router.websocket("/ws/{client_uuid}")
async def websocket_endpoint(websocket: WebSocket, client_uuid: str):
    manager = ConnectionManager()
    await manager.connect(websocket, client_uuid, myvar=myvar)
    await websocket.send_json({'Welcome nigga':  client_uuid})
    print('Wating for new events [send_periodically] ....')
    await asyncio.create_task(send_periodically(websocket, manager, client_uuid, 0.9, myvar=myvar))

