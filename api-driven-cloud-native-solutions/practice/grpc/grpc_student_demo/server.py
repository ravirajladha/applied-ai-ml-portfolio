from concurrent import futures
import grpc

import student_pb2
import student_pb2_grpc


# Simple in-memory data store for the classroom demo
STUDENTS = {
    101: {"name": "Asha", "program": "M.Tech Software Systems", "status": "ACTIVE"},
    102: {"name": "Ravi", "program": "M.Tech Data Science", "status": "ACTIVE"},
    103: {"name": "Meera", "program": "M.Tech AI & ML", "status": "ACTIVE"},
}


class StudentService(student_pb2_grpc.StudentServiceServicer):
    def GetStudent(self, request, context):
        print(f"[SERVER] Request received for student id={request.id}")

        student = STUDENTS.get(request.id)
        if student is None:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"Student with id {request.id} was not found",
            )

        response = student_pb2.StudentResponse(
            id=request.id,
            name=student["name"],
            program=student["program"],
            status=student["status"],
        )

        print(f"[SERVER] Sending response: {response}")
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    student_pb2_grpc.add_StudentServiceServicer_to_server(StudentService(), server)

    port = "50051"
    server.add_insecure_port(f"[::]:{port}")
    server.start()

    print(f"[SERVER] gRPC Student Service is running on localhost:{port}")
    print("[SERVER] Press Ctrl+C to stop the server.")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")
        server.stop(0)


if __name__ == "__main__":
    serve()
