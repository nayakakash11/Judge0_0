import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Problem
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Problem
from compiler.forms import CodeSubmissionForm
from pathlib import Path
from django.conf import settings
from compiler.views import run_code
from compiler.models import CodeSubmission
from .utils.gemini import review_code
from django.views.decorators.csrf import csrf_exempt

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('problem_list')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('problem_list')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'problem_list.html', {'problems': problems})

@login_required
def code_editor(request):
    output = None
    error = None
    code = ""
    input_data = ""
    language = "py"
    if request.method == "POST":
        code = request.POST.get("code", "")
        input_data = request.POST.get("input_data", "")
        language = request.POST.get("language", "py")
        from compiler.views import run_code
        result = run_code(language, code, input_data)
        if result.get("stderr"):
            error = result["stderr"]
        else:
            try:
                output = result["output_file"].read_text()
            except Exception as e:
                error = str(e)
    return render(request, "code_editor.html", {
        "output": output,
        "error": error,
        "code": code,
        "input_data": input_data,
        "language": language,
    })

@login_required
def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    output_data = None
    result_message = None
    submission = None
    show_review = False
    ai_review = None

    # If it's a GET request with an 'ai_review' trigger
    if request.method == "GET" and "ai_review" in request.GET:
        submission_id = request.GET.get("submission_id")
        try:
            submission = CodeSubmission.objects.get(id=submission_id)
            if submission.verdict in ["Accepted", "Wrong Answer"]:
                show_review = True
                ai_review = review_code(
                    code=submission.code,
                    language=submission.language,
                    verdict=submission.verdict,
                    problem_title=problem.title,
                    problem_statement=problem.statement,
                )
                result_message = f"💬 Review for {submission.verdict} code:"
            else:
                result_message = "⚠️ Review available only for Accepted or Wrong Answer verdicts."
        except CodeSubmission.DoesNotExist:
            result_message = "⚠️ Submission not found."

        form = CodeSubmissionForm(initial={
            "code": submission.code if submission else "",
            "language": submission.language if submission else "python",
        })

    # POST request for new submission
    elif request.method == "POST":
        form = CodeSubmissionForm(request.POST)
        custom_input = request.POST.get("custom_input", "")
        if form.is_valid():
            submission = form.save(commit=False)
            submission.problem = problem

            # If user clicked "Run Code" (custom input)
            if "run_code" in request.POST:
                if not custom_input.strip():
                    result_message = "⚠️ Please provide custom input to run your code."
                else:
                    result = run_code(submission.language, submission.code, custom_input)
                    if result["stderr"]:
                        result_message = f"⚠️ Error during code execution: {result['stderr']}"
                        output_data = ""
                    else:
                        try:
                            output_data = result["output_file"].read_text().strip()
                            result_message = "✅ Code executed with your custom input."
                        except Exception as e:
                            result_message = f"⚠️ Exception occurred: {str(e)}"
            # If user clicked "Submit" (official test cases)
            elif "submit_code" in request.POST:
                input_file_path = f'testcases/{pk}/input.txt'
                expected_output_path = f'testcases/{pk}/expected_output.txt'

                if not os.path.exists(input_file_path) or not os.path.exists(expected_output_path):
                    result_message = "❌ Test cases not found for this problem."
                else:
                    try:
                        with open(input_file_path, 'r') as f:
                            input_data = f.read()
                            if not input_data.endswith('\n'):
                                input_data += '\n'

                        result = run_code(submission.language, submission.code, input_data)

                        if result["stderr"]:
                            verdict = "Runtime Error"
                            result_message = f"⚠️ Error during code execution: {result['stderr']}"
                            output_data = ""
                        else:
                            output_data = result["output_file"].read_text().strip()
                            expected_output = Path(expected_output_path).read_text().strip()

                            submission.output_data = output_data

                            if output_data == expected_output:
                                verdict = "Accepted"
                                result_message = "✅ Your code passed all the test cases!"
                                show_review = True
                            else:
                                verdict = "Wrong Answer"
                                result_message = (
                                    "❌ Your code failed some test cases.\n\n"
                                    f"Expected Output:\n{expected_output}\n\n"
                                    f"Your Output:\n{output_data}"
                                )
                                show_review = True

                        submission.verdict = verdict
                        submission.save()

                    except Exception as e:
                        result_message = f"⚠️ Exception occurred: {str(e)}"
    else:
        form = CodeSubmissionForm()

    return render(
        request,
        "problem_detail.html",
        {
            "problem": problem,
            "form": form,
            "output_data": output_data,
            "result_message": result_message,
            "submission_id": submission.id if submission else None,
            "verdict": submission.verdict if submission else None,
            "show_review": show_review,
            "ai_review": ai_review,
        }
    )
