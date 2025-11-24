class MessageStatusGenerator:
    @staticmethod
    def build_status_error(msg: str = '') -> dict:
        return {'status': 1, 'msg': msg, 'flash': 'error'}

    @staticmethod
    def build_status_success(msg: str = '') -> dict:
        return {'status': 0, 'msg': msg, 'flash': 'Sucesso!'}
    
    @staticmethod
    def build_admin_status_success(msg: str = '') -> dict:
        return {'status': 0, 'msg': msg, 'flash': 'success'}