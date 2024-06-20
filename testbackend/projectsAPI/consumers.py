from json import dumps

from channels.generic.websocket import AsyncWebsocketConsumer


class AIConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.project_id = self.scope["url_route"]["kwargs"]["pk"]
        self.project_group_name = f"project_id_{self.project_id}"

        await self.channel_layer.group_add(
            self.project_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.project_group_name,
            self.channel_name,
        )

    async def send_status_image(self, event):
        await self.send(
            text_data=dumps(
                {
                    "status": event["status"],
                    "filename": event["filename"],
                },
            ),
        )


__all__ = ()
