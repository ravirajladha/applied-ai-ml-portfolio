import sys
import grpc

import student_pb2
import student_pb2_grpc


def get_student(student_id: int):
    print(f"[CLIENT] Connecting to localhost:50051")

    # For a local classroom demo we use an insecure channel.
    # Production systems should use TLS credentials.
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = student_pb2_grpc.StudentServiceStub(channel)

        request = student_pb2.StudentRequest(id=student_id)
        print(f"[CLIENT] Sending request: {request}")

        try:
            response = stub.GetStudent(request, timeout=5)
        except grpc.RpcError as exc:
            print(f"[CLIENT] RPC failed: {exc.code().name} - {exc.details()}")
            return

        print("\n[CLIENT] Response received")
        print(f"  ID      : {response.id}")
        print(f"  Name    : {response.name}")
        print(f"  Program : {response.program}")
        print(f"  Status  : {response.status}")


def main():
    if len(sys.argv) > 1:
        student_id = int(sys.argv[1])
    else:
        student_id = int(input("Enter student ID (101, 102, 103): "))

    get_student(student_id)


if __name__ == "__main__":
    main()
