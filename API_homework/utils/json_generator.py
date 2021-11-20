import json


class RequestsDataGenerator:

    @staticmethod
    def generate_data_for_login(email, password):
        return {
            'email': email,
            'password': password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/'
        }

    @staticmethod
    def generate_json_for_creating_segment(segment_name):
        request_data = {
            "logicType": "or",
            "name": segment_name,
            "pass_condition": 1,
            "relations": [
                {
                    "object_type": "remarketing_player",
                    "params": {
                        "type": "positive",
                        "left": 365,
                        "right": 0
                    }
                }
            ]
        }
        return json.dumps(request_data)

    @staticmethod
    def generate_json_for_deleting_segment(segment_id):
        request_data = [{"source_id": segment_id, "source_type": "segment"}]
        return json.dumps(request_data)

    @staticmethod
    def generate_files_for_sending_picture(picture_name, picture):
        return {
            'file': (picture_name, picture),
            'data': '{"width": 0, "height": 0}'
        }

    @staticmethod
    def generate_json_for_creating_campaign(campaign_name, url_id, picture_id):
        request_data = {
            "name": campaign_name,
            "objective": "traffic",
            "package_id": 961,
            "banners": [{
                "urls": {
                    "primary": {
                        "id": url_id
                    }
                },
                "textblocks": {},
                "content": {
                    "image_240x400": {
                        "id": picture_id
                    }
                },
                "name": ""
            }]
        }
        return json.dumps(request_data)

    @staticmethod
    def generate_json_for_deleting_campaign(campaign_id):
        request_data = [{"id": campaign_id, "status": "deleted"}]
        return json.dumps(request_data)
