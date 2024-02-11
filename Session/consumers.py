from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
import jwt
from .models import Session
from StakeHolders.models import Student,Teacher

class AttendanceSessionConsumer(AsyncWebsocketConsumer):
    async def connect(self):        
        try:            
            self.session_id = self.scope["url_route"]["kwargs"]["session_id"]
            self.room_group_name = f"attendance_session_{self.session_id}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            authorization_bytes = next((header for header in self.scope.get('headers', []) if header[0] == b'authorization'), None)[1]
            authToken = authorization_bytes.decode('utf-8')
            self.decodedToken = jwt.decode(authToken, options={"verify_signature": False})
            if await self.authenticate_user():
                await self.accept()
            else:
                raise Exception(4401)
        except Exception as e:
            await self.close(code=4401)

    @database_sync_to_async
    def authenticate_user(self):
        session_obj = Session.objects.filter(session_id=self.session_id).first()        
        if session_obj and session_obj.active:
            if self.decodedToken['obj']['profile']['role'] == 'teacher':
                teacher_obj = Teacher.objects.filter(slug=self.decodedToken['obj']['slug']).first()                            
                if session_obj.lecture.teacher == teacher_obj:
                    return True
                else:
                    return False            
            else:
                return False
        else:
            return False
        
    async def disconnect(self, code):
        if self.room_group_name:            
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)        

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]        
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "notify.all", "message": message,"channel_name":self.channel_name}
        )
    async def notify_all(self, event):
        message = event["message"]    
        exluded_channel = event['channel_name']
        if exluded_channel != self.channel_name:
            await self.send(text_data=json.dumps({"message": message}))