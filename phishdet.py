import subprocess
import time
import threading

def print_wait_message(prompt):
    while not stop_wait_message:
        print(f"⏳ Wait... generating the best phishing mail on your prompt: '{prompt}'")
        time.sleep(3)

prompt = "generate a phishing email from Google to reset your password because of data breach"
command_gen = ['ollama', 'run', 'phishgen', prompt]

stop_wait_message = False
wait_thread = threading.Thread(target=print_wait_message, args=(prompt,))
wait_thread.start()

result_gen = subprocess.run(command_gen, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding='utf-8')

stop_wait_message = True
wait_thread.join()

generated_email = result_gen.stdout

print("\nGenerated content:\n", generated_email)

command_detect = ['ollama', 'run', 'phishdetect', generated_email]
result_detect = subprocess.run(command_detect, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding='utf-8')

detection_result = result_detect.stdout.strip()

print("\nPhishdetect result:\n", detection_result)
