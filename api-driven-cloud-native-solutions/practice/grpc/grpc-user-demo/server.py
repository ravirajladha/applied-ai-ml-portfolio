"""Local classroom server; data resets when restarted."""
from concurrent import futures
from threading import Lock
import logging
import grpc
import user_pb2 as pb
import user_pb2_grpc as rpc


class UserService(rpc.UserServiceServicer):
    def __init__(self):
        self.users = {
            1: pb.User(id=1, name="Arun", email="arun@example.com"),
            2: pb.User(id=2, name="Meera", email="meera@example.com"),
        }
        self.next_id = 3
        self.lock = Lock()

    def GetUser(self, request, context):
        if request.id <= 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "ID must be positive")
        with self.lock:
            user = self.users.get(request.id)
        if user is None:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")
        logging.info("GetUser id=%s", request.id)
        return user

    def CreateUser(self, request, context):
        name = request.name.strip()
        email = request.email.strip().lower()
        # Deliberately basic classroom validation, not full email verification.
        if not name or len(name) > 100:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Name must be 1-100 characters")
        if len(email) > 254 or email.count("@") != 1 or any(c.isspace() for c in email):
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Provide a valid email format")
        local, domain = email.split("@")
        if not local or not domain or "." not in domain or domain.startswith(".") or domain.endswith("."):
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Provide a valid email format")
        with self.lock:
            if any(u.email.lower() == email for u in self.users.values()):
                context.abort(grpc.StatusCode.ALREADY_EXISTS, "Email already registered")
            user = pb.User(id=self.next_id, name=name, email=email)
            self.users[user.id] = user
            self.next_id += 1
        logging.info("CreateUser id=%s", user.id)
        return user

    def ListUsers(self, request, context):
        with self.lock:
            result = pb.ListUsersResponse(users=list(self.users.values()))
        logging.info("ListUsers count=%s", len(result.users))
        return result


def build_server(address="127.0.0.1:50051"):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    rpc.add_UserServiceServicer_to_server(UserService(), server)
    port = server.add_insecure_port(address)
    if port == 0:
        raise RuntimeError(f"Could not bind to {address}")
    return server, port


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    server, port = build_server()
    server.start()
    print(f"User gRPC server listening on 127.0.0.1:{port}", flush=True)
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(grace=2).wait()
