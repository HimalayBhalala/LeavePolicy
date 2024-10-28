from rest_framework.renderers import JSONRenderer
import json 
class NewJSONRenderer(JSONRenderer):
    
    charset = 'utf-8'
 
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'ErrorDetail' in str(data):
            response = json.dumps({
                "message" : str(data['message']),
                "status" : str(data['status'])
                })
        else:
            response = json.dumps(str(data))
 
        if 'non_field_errors' in data:
            response['non_field_errors'] = data['non_field_errors']
        
        return response