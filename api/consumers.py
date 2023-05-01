from channels.generic.websocket import AsyncWebsocketConsumer
import json

class chatRoomConsumer(AsyncWebsocketConsumer):
    # connect room
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'] # collect room name from url
        self.room_group_name = 'api_%s' % self.room_name # put room_name into group
        await self.channel_layer.group_add(
             self.room_group_name,
             self.channel_name
        )
    # send message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
             'type':'tester_message',
             'tester':'hello',   
            }
        )
    
    async def tester_message(self,event):
        tester = event['tester']
        
        await self.send(text_data=json.dumps({
            'tester': tester,
        }))
    
    # end connection
    async def disconnect(self, close_code):
         await self.channel_layer.group_discord(
             self.room_group_name,
             self.channel_name
        )