# Python gRPC User Service Classroom Demo

Python 3.10+; tested on Python 3.12. No database, API key or paid account.
Implements GetUser, CreateUser and ListUsers as unary RPCs. ListUsers returns
one response containing a repeated field; this is not server streaming.
All users are fictional. State is stored in memory and resets on server restart.

## 1. Install (Windows Command Prompt)
Extract the archive. Open Command Prompt in the folder containing user.proto.
```
py -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```
PowerShell activation: `.\.venv\Scripts\Activate.ps1`. If blocked, use
`.\.venv\Scripts\python.exe` instead of python without changing execution policy.
macOS/Linux: `python3 -m venv .venv`, then `source .venv/bin/activate`, then
`python -m pip install -r requirements.txt`.

## 2. Generate Python messages and interfaces
```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user.proto
```
- user_pb2.py contains generated Protocol Buffer message classes.
- user_pb2_grpc.py contains the client stub, server base class and registration code.
Generated files are included but regenerate them during teaching. Do not edit
these files manually. Re-run the generator after changing user.proto. Matching
pinned dependencies avoid generated-code/runtime compatibility mismatches.

## 3. Start server in terminal 1
```
python server.py
```
Expected: `User gRPC server listening on 127.0.0.1:50051`
Keep this terminal open. Ctrl+C stops the server.

## 4. Run client in terminal 2
Open another terminal in the same folder and activate the SAME environment:
```
.venv\Scripts\activate.bat
python client.py
```
The client gets user 1, creates Kavya, reads the created user, lists users, then
requests a missing ID to demonstrate NOT_FOUND. Creation uses a unique demo
email each run, so repeated client runs add records without duplicate errors.
The client uses five-second deadlines and a connection timeout.

## Contract and request flow
user.proto is the shared contract. The compiler produces message and service
interfaces. The server implements the generated servicer; the client calls the
stub. gRPC serializes Protocol Buffer messages, carries them over HTTP/2 and
returns a typed response. The stub makes a remote call look like a Python method
call, but network failures and deadlines still matter.

Numbers such as `string name = 2` are Protocol Buffer field identifiers, not
values. Keep identifiers stable; do not reuse old field numbers after deletion.
The proto `package users` namespaces the service; it does not create a Python
package directory in this flat example.

## 60-second teaching cues (one minute per step)
1. Contract: 'Both programs must agree on methods and message shapes. That is
   what user.proto defines.' Show GetUserRequest and User.
2. Generation: 'The compiler creates message classes and communication glue.
   We still implement the business logic ourselves.' Run protoc.
3. Server: 'The server registers our implementation and listens on port 50051.'
   Start server.py; point to GetUser and the sample records.
4. Client: 'The channel connects us; the stub exposes remote methods. Calling
   GetUser sends a real request to another process.' Run client.py.
5. State: 'CreateUser returns an assigned ID. A subsequent GetUser retrieves
   that same user.' Observe create/readback/list output.
6. Error: 'A missing user produces gRPC NOT_FOUND. It is a gRPC status, not an
   HTTP 404 response.' Point to the caught RpcError.

## Student exercises
- Change the initial user's name, restart server and rerun client.
- Call GetUser with ID 0: expect INVALID_ARGUMENT.
- Create two users with the same email: expect ALREADY_EXISTS.
- Add a new field to User, regenerate files, update server and display it.
- Stop server and rerun client to see the connection-timeout message.

## Test
```
python test_demo.py
```
Starts a temporary server on a free local port, verifies live calls and errors,
then launches the actual client in a second process. Does not require server.py
to be running and leaves the classroom server/state untouched.

## Troubleshooting and scope
- Missing user_pb2: run the protoc command from this folder.
- Cannot connect: start server first; check both programs use the same port.
- Port occupied: stop the old demo server, or change the address in server.py
  and pass the matching target to `python client.py 127.0.0.1:50052`.
- No browser page appears: this is a gRPC service, not an HTTP/JSON web page.
- This uses insecure local loopback transport for teaching, not TLS/authentication.
  Keep it local. Production services need persistence, TLS and access controls.
- Email validation is intentionally basic classroom validation.

Official references:
https://grpc.io/docs/languages/python/basics/
https://grpc.io/docs/languages/python/quickstart/
