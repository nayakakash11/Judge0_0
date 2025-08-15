from django.shortcuts import render
from django.http import HttpResponse
from compiler.forms import CodeSubmissionForm
from django.conf import settings
import os
import uuid
import subprocess
from pathlib import Path


def submit(request):
    if request.method == "POST":
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save()
            print(submission.language)
            print(submission.code)
            output = run_code(
                submission.language, submission.code, submission.input_data
            )
            submission.output_data = output
            submission.save()
            return render(request, "result.html", {"submission": submission})
    else:
        form = CodeSubmissionForm()
    return render(request, "index.html", {"form": form})


def run_code(language, code, input_data):

    unique = str(uuid.uuid4())
    base_path = Path(settings.BASE_DIR)
    code_path = base_path / "codes"
    input_path = base_path / "inputs"
    output_path = base_path / "outputs"

    # Ensure directories exist
    for path in [code_path, input_path, output_path]:
        path.mkdir(exist_ok=True)

    code_file = code_path / f"{unique}.{language}"
    input_file = input_path / f"{unique}.txt"
    output_file = output_path / f"{unique}.txt"

    code_file.write_text(code)
    input_file.write_text(input_data)

    docker_command = [
        "docker", "run", "--rm",
        "-v", f"{code_path}:/app/codes",
        "-v", f"{input_path}:/app/inputs",
        "-v", f"{output_path}:/app/outputs",
        "code-runner", 
        "bash", "-c"
    ]

    if language == "cpp":
        run_cmd = f"""
        g++ /app/codes/{code_file.name} -o /app/codes/{unique} && \
        /app/codes/{unique} < /app/inputs/{input_file.name} > /app/outputs/{output_file.name}
        """
    elif language == "py":
        run_cmd = f"""
        python3 /app/codes/{code_file.name} < /app/inputs/{input_file.name} > /app/outputs/{output_file.name}
        """
    elif language == "c":
        run_cmd = f"""
        gcc /app/codes/{code_file.name} -o /app/codes/{unique} && \
        /app/codes/{unique} < /app/inputs/{input_file.name} > /app/outputs/{output_file.name}
        """
    elif language == "java":
        run_cmd = f"""
        javac /app/codes/{code_file.name} && \
        java -cp /app/codes {code_file.stem} < /app/inputs/{input_file.name} > /app/outputs/{output_file.name}
        """
    else:
        return "Unsupported language"

    full_command = docker_command + [run_cmd]

    result = subprocess.run(full_command, capture_output=True, text=True)
    stderr_output = result.stderr
    
    return {
        "output_file": output_file,
        "stderr": stderr_output
    }

