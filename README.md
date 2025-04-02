# backend
This is the backend service of Lumora
uvicorn src.app.main:app --reload 
uvicorn src.app.main:app --host=0.0.0.0 --port=8000

netstat -ano | findstr :8000
  TCP    127.0.0.1:8000         0.0.0.0:0              LISTENING       15808
  TCP    127.0.0.1:8000         0.0.0.0:0              LISTENING       39088
  TCP    127.0.0.1:8000         127.0.0.1:53118        ESTABLISHED     15808
  TCP    127.0.0.1:53118        127.0.0.1:8000         ESTABLISHED     13572
PS C:\Users\Taiwo> taskkill /PID 15808 /F
SUCCESS: The process with PID 15808 has been terminated.
PS C:\Users\Taiwo> taskkill /PID 39088 /F
SUCCESS: The process with PID 39088 has been terminated.
PS C:\Users\Taiwo> taskkill /PID 13572 /F
SUCCESS: The process with PID 13572 has been terminated.