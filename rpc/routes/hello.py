from rpc import api
from rpc.rpc_resource import RpcResource
from rpc.models.hello import HelloModel


@api.route('/hello/')
class Hello(RpcResource):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.model = HelloModel()

    def hello(self):
        return self.model.hello()
