# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import datastore_pb2 as datastore__pb2


class DatastoreStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.put = channel.unary_unary(
        '/Datastore/put',
        request_serializer=datastore__pb2.Request.SerializeToString,
        response_deserializer=datastore__pb2.Response.FromString,
        )
    self.delete = channel.unary_unary(
        '/Datastore/delete',
        request_serializer=datastore__pb2.Request.SerializeToString,
        response_deserializer=datastore__pb2.Response.FromString,
        )
    self.connect_server = channel.unary_stream(
        '/Datastore/connect_server',
        request_serializer=datastore__pb2.RequestSequence.SerializeToString,
        response_deserializer=datastore__pb2.Response.FromString,
        )


class DatastoreServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def put(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def delete(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def connect_server(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_DatastoreServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'put': grpc.unary_unary_rpc_method_handler(
          servicer.put,
          request_deserializer=datastore__pb2.Request.FromString,
          response_serializer=datastore__pb2.Response.SerializeToString,
      ),
      'delete': grpc.unary_unary_rpc_method_handler(
          servicer.delete,
          request_deserializer=datastore__pb2.Request.FromString,
          response_serializer=datastore__pb2.Response.SerializeToString,
      ),
      'connect_server': grpc.unary_stream_rpc_method_handler(
          servicer.connect_server,
          request_deserializer=datastore__pb2.RequestSequence.FromString,
          response_serializer=datastore__pb2.Response.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Datastore', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
