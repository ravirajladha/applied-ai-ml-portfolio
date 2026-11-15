Python gRPC Student Service Demo
================================

FILES
-----
student.proto      - gRPC service contract
server.py          - Python gRPC server implementation
client.py          - Python gRPC client implementation
requirements.txt   - Python packages
generate_stubs.bat - Windows code-generation helper
generate_stubs.sh  - macOS/Linux code-generation helper

SETUP
-----
1. Create and activate a virtual environment.
2. Install dependencies:
   python -m pip install -r requirements.txt
3. Generate Python code from student.proto:
   python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. student.proto

This creates:
   student_pb2.py
   student_pb2.pyi
   student_pb2_grpc.py

RUN
---
Terminal 1:
   python server.py

Terminal 2:
   python client.py 101

Try:
   python client.py 102
   python client.py 999

The 999 request demonstrates the gRPC NOT_FOUND status.
