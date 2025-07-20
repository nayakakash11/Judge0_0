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
    project_path = Path(settings.BASE_DIR)
    directories = ["codes", "inputs", "outputs"]

    for directory in directories:
        dir_path = project_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)

    unique = str(uuid.uuid4())

    code_file_name = f"{unique}.{language}"
    input_file_name = f"{unique}.txt"
    output_file_name = f"{unique}.txt"

    code_file_path = project_path / "codes" / code_file_name
    input_file_path = project_path / "inputs" / input_file_name
    output_file_path = project_path / "outputs" / output_file_name

    # Save code and input to files
    code_file_path.write_text(code)
    input_file_path.write_text(input_data)
    output_file_path.touch()  # Create empty file

    error_data = ""

    if language == "cpp":
        executable_path = project_path / "codes" / unique
        compile_result = subprocess.run(
            ["clang++", str(code_file_path), "-o", str(executable_path)],
            capture_output=True,
            text=True
        )

        if compile_result.returncode != 0:
            error_data = compile_result.stderr
        else:
            with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
                result = subprocess.run(
                    [str(executable_path)],
                    stdin=input_file,
                    stdout=output_file,
                    stderr=subprocess.PIPE,
                    text=True
                )
                error_data = result.stderr

    elif language == "py":
        with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
            result = subprocess.run(
                ["python3", str(code_file_path)],
                stdin=input_file,
                stdout=output_file,
                stderr=subprocess.PIPE,
                text=True
            )
            error_data = result.stderr

    output_data = output_file_path.read_text()

    if error_data:
        output_data += "\n--- Error ---\n" + error_data

    return output_data