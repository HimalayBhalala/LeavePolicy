from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from rest_framework.exceptions import ErrorDetail

class LeaveJsonRenderer(JSONRenderer):

    charset = 'utf-8'

    def format_errors(self, data):
        if isinstance(data, dict):
            return {key: self.format_errors(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.format_errors(item) for item in data]
        elif isinstance(data, ErrorDetail):
            return str(data)
        return data

    def render(self, data, accepted_media_type=None, renderer_context=None):
        
        if 'ErrorDetail' in str(data):
            formatted_data = {
                "info": self.format_errors(data),
                "status": renderer_context.get('response').status_code
            }

        elif data['status'] == 400:
            formatted_data = {
                "error":{
                    "message":data['message'],
                },
                "status":data['status']
            }

        else:
            formatted_data = {
                "info":{
                "message": data['message'],
                "data":data['data'],
                },
                "status": data['status']
            }

        return super().render(formatted_data, accepted_media_type, renderer_context)
