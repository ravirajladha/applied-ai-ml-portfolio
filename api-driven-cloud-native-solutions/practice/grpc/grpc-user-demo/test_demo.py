import subprocess
import sys
from pathlib import Path
import grpc
import user_pb2 as pb
import user_pb2_grpc as rpc
from server import build_server

server, port = build_server('127.0.0.1:0')
server.start()
try:
    with grpc.insecure_channel(f'127.0.0.1:{port}') as channel:
        grpc.channel_ready_future(channel).result(timeout=5)
        stub = rpc.UserServiceStub(channel)
        assert stub.GetUser(pb.GetUserRequest(id=1), timeout=5).name == 'Arun'
        created = stub.CreateUser(pb.CreateUserRequest(name='Test User',email='test@example.com'),timeout=5)
        assert created.id == 3
        assert stub.GetUser(pb.GetUserRequest(id=3),timeout=5).email == 'test@example.com'
        assert len(stub.ListUsers(pb.ListUsersRequest(),timeout=5).users) == 3
        def expect(code, call):
            try: call()
            except grpc.RpcError as e: assert e.code() == code
            else: raise AssertionError(f'Expected {code}')
        expect(grpc.StatusCode.NOT_FOUND,lambda:stub.GetUser(pb.GetUserRequest(id=999),timeout=5))
        expect(grpc.StatusCode.INVALID_ARGUMENT,lambda:stub.GetUser(pb.GetUserRequest(id=0),timeout=5))
        expect(grpc.StatusCode.INVALID_ARGUMENT,lambda:stub.CreateUser(pb.CreateUserRequest(name=' ',email='x@example.com'),timeout=5))
        expect(grpc.StatusCode.INVALID_ARGUMENT,lambda:stub.CreateUser(pb.CreateUserRequest(name='Test',email='invalid'),timeout=5))
        expect(grpc.StatusCode.ALREADY_EXISTS,lambda:stub.CreateUser(pb.CreateUserRequest(name='Again',email='TEST@example.com'),timeout=5))
    # Actual client in another process, using the live gRPC network service.
    subprocess.run([sys.executable,'client.py',f'127.0.0.1:{port}'],check=True,cwd=Path(__file__).parent,timeout=15)
finally:
    server.stop(grace=0).wait()
print('PASS: live gRPC calls, create/read/list, errors, duplicate email and separate-process client')
