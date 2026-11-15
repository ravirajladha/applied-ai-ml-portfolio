"""Run after starting server.py in a separate terminal."""
import sys
import uuid
import grpc
import user_pb2 as pb
import user_pb2_grpc as rpc


def show(user):
    print(f"  ID={user.id}, name={user.name}, email={user.email}")


def main(target="127.0.0.1:50051"):
    with grpc.insecure_channel(target) as channel:
        try:
            grpc.channel_ready_future(channel).result(timeout=5)
        except grpc.FutureTimeoutError:
            print("Cannot connect. Start server.py and check the address/port.")
            return 1
        stub = rpc.UserServiceStub(channel)
        try:
            print("1. Retrieve user 1")
            show(stub.GetUser(pb.GetUserRequest(id=1), timeout=5))

            print("\n2. Create a user")
            # Unique email allows this demo to be rerun without restarting.
            created = stub.CreateUser(pb.CreateUserRequest(
                name="Kavya", email=f"kavya.{uuid.uuid4().hex}@example.com"), timeout=5)
            show(created)

            print("\n3. Read back the new user")
            show(stub.GetUser(pb.GetUserRequest(id=created.id), timeout=5))

            print("\n4. List all users")
            for user in stub.ListUsers(pb.ListUsersRequest(), timeout=5).users:
                show(user)

            print("\n5. Request missing user 999999")
            try:
                stub.GetUser(pb.GetUserRequest(id=999999), timeout=5)
            except grpc.RpcError as error:
                print(f"  Expected error: {error.code().name}: {error.details()}")
                if error.code() != grpc.StatusCode.NOT_FOUND:
                    raise
            return 0
        except grpc.RpcError as error:
            print(f"RPC failed: {error.code().name}: {error.details()}")
            return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1:50051"))
