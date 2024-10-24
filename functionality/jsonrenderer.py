from rest_framework import renderers
import json


class JsonRenderer(renderers.BaseRenderer):

    charset = "utf-8"
    media_type = "application/json"
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        print(str(data['message']))
        response = ''
        if 'ErrorDetail' in str([data['message']]):
            response = json.dumps(
                    {
                        "message" : data['message'],
                        "status" : data['status']
                    },
                )
        else:
            response = json.dumps(data)
        return response