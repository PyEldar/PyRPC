
import types
import collections

from flask import request
from flask_restplus import Resource
from jsonrpcserver import Methods

from rpc import api, call
import rpcconfig


class RpcResource(Resource):
    """Base class for request handling."""

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.model = None
        self.methods = Methods()
        for name in self._rpc_methods():
            self.methods.add(method=getattr(self, name), name=name)

    @classmethod
    def _rpc_methods(cls):
        """Find all user-defined public methods."""
        ret = []
        my_methods = set(dir(cls)) - set(dir(Resource))
        for name in my_methods:
            if not name.startswith('_') and isinstance(
                getattr(cls, name), (
                    collections.Callable,
                    types.FunctionType,
                    staticmethod,
                    classmethod
                )
                ) and name.lower() not in ("post", "route", "mediatypes"):
                ret.append(name)
        return ret

    @api.expect(call)
    def post(self):
        """Accept http POST request and resolve it with dispatcher."""
        json_data = request.get_json()
        response = self.methods.dispatch(json_data, debug=rpcconfig.DEBUG)
        return response, response.http_status
