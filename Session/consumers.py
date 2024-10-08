from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
import jwt
from .models import Session
from StakeHolders.models import Teacher
from Session.serializers import SessionSerializerHistory

class AttendanceSessionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.access_token = self.scope['query_string'].decode('utf-8')  
        try:         
            self.session_id = self.scope["url_route"]["kwargs"]["session_id"]            
            self.room_group_name = f"{self.session_id}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)            
            self.decodedToken = jwt.decode(self.access_token, options={"verify_signature": False})            
            if await self.authenticate_user():                
                await self.accept()
            else:                
                raise Exception(4401)
        except Exception as e:
            print(e)
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
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)       

    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)        
        if 'action' in text_data:
            if text_data['action'] == 'end_session':
                end_status,data = await self.end_session()
                if end_status and data:
                    await self.send(json.dumps({'message':{
                        'action':'session_ended',
                        'data':data
                    }}))
                else:
                    await self.send(json.dumps({'message':{
                        'action':'session_already_ended'
                    }}))
    
    @database_sync_to_async
    def end_session(self):
        session_obj = Session.objects.filter(session_id=self.session_id).first()
        if session_obj and session_obj.active in ['pre','ongoing']:
            session_obj.active = 'post'
            if session_obj.lecture.is_proxy: 
                session_obj.lecture.is_active = False
                session_obj.lecture.save()
            session_serialized = SessionSerializerHistory(session_obj)
            session_obj.save()         
            return True,session_serialized.data
        else:
            return False,None
        
    async def attendance_marked(self,event):
        message = event['message']
        data = {'action':'attendance_marked','data':message}
        await self.send(text_data=json.dumps({"message": data}))