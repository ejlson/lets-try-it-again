from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django import forms
from .forms import MatrixAForm, MatrixBForm
import numpy as np

@login_required(login_url="/admin")

def str_to_matrix(s):
    s = s.strip()
    s = s.replace('[','').replace(']','')
    s = ''.join(c for c in s if c.isdigit() or c == ' ' or c == '-' or c == '.')
    rows = s.split()
    matrix = []
    for row in rows:
        matrix.append([float(x) for x in row.split()])
    matrix = np.array(matrix)
    matrix = matrix.reshape(3, 3)
    return matrix

def str_to_array(s):
    s = s.strip('[]').split()
    arr = [float(x) for x in s]
    return arr

def float_to_int(mat):
    new = []
    for i in range(0, 3):
        new.append([])
        for j in range(0, 3):
            new[i].append(int(mat[i][j]))
    return new

def check_realAndround(mat):
    ts = np.isreal([mat])
    if not ts.all():
        return mat, False
    else:
        # is real then round the number or list to 2 decimal place
        x = np.array(mat)
        n_d = x.ndim
        if n_d == 0:
            mat = round(mat, 2)
        else:
            if n_d == 1:
                for i in range(len(mat)):
                    mat[i] = round(mat[i], 2)
            else:
                for i in range(len(mat)):
                    for j in range(len(mat[0])):
                        mat[i][j] = round(mat[i][j], 2)
    return mat, True


def Round(mat):
    # is real then round the number or list to 2 decimal place
    x = np.array(mat)
    n_d = x.ndim
    if n_d == 0:
        mat = round(mat, 2)
    else:
        if n_d == 1:
            for i in range(len(mat)):
                mat[i] = round(mat[i], 2)
        else:
            for i in range(len(mat)):
                for j in range(len(mat[0])):
                    mat[i][j] = round(mat[i][j], 2)
    return mat

def matrix_calculator(request):
    result = ''
    error = ''
    form_a = MatrixAForm(request.POST or None, prefix='a')
    form_b = MatrixBForm(request.POST or None, prefix='b')

    if form_a.is_valid() and form_b.is_valid():
        matrix_a = []
        matrix_b = []

        for i in range(3):
            row_a = []
            row_b = []
            for j in range(3):
                row_a.append(form_a.cleaned_data[f'matrix_a_{i}{j}'])
                row_b.append(form_b.cleaned_data.get(f'matrix_b_{i}{j}', 0))
            matrix_a.append(row_a)
            matrix_b.append(row_b)

        matrix_a = np.array(matrix_a)
        matrix_b = np.array(matrix_b)
        is_matrix_b_provided = not (matrix_b == 0).all()

        operation = request.POST.get('operation')

        try:
            if operation == 'add':
                if is_matrix_b_provided:
                    result = matrix_a + matrix_b
                else:
                    error = str(e)
            elif operation == 'subtract':
                if is_matrix_b_provided:
                    result = matrix_a - matrix_b
                else:
                    error = 'Matrix B is required for subtraction.'
            elif operation == 'multiply':
                if is_matrix_b_provided:
                    result = matrix_a @ matrix_b
                else:
                    error = 'Matrix B is required for multiplication.'
            elif operation == 'determinant':
                result = np.linalg.det(matrix_a)
            elif operation == 'eigenvalues':
                eigenvectors, eigenvalues = np.linalg.eig(matrix_a)
                result = eigenvalues
            elif operation == 'eigenvectors':
                eigenvector, eigenvalues = np.linalg.eig(matrix_a)
                result = eigenvectors
            elif operation == 'inverse':
                inverse = np.linalg.inv(matrix_a)
                result = inverse
            else:
                error = 'Invalid operation'
        except ValueError as ve:
            error = str(ve)
        except Exception as e:
            error = str(e)
        result = Round(result)
        result = str(result)

    return render(request, 'index.html', {'form_a': form_a, 'form_b': form_b, 'result': result, 'error': error})

def practice_questions(request):
    result = []
    error = ''
    t1 = ""
    questions = []
    answer = []
    operation = request.POST.get('operation')
    mat1 = []
    mat2 = []
    matrix_a = []
    form_a = MatrixAForm(request.POST or None, prefix='a')
    if form_a.is_valid():
        matrix_a = []
        for i in range(3):
            row_a = []
            for j in range(3):
                row_a.append(form_a.cleaned_data[f'matrix_a_{i}{j}'])
            matrix_a.append(row_a)
        matrix_a = np.array(matrix_a)
    # try:
    t = False
    try:
        while not t:
            if operation == "add":
                mat1 = np.random.randint(1, 10, size=(3, 3))
                mat2 = np.random.randint(1, 10, size=(3, 3))
                result = mat1 + mat2
                t = True
            elif operation == "subtract":
                mat1 = np.random.randint(1, 10, size=(3, 3))
                mat2 = np.random.randint(1, 10, size=(3, 3))
                result = mat1 - mat2
                t = True
            elif operation == "multiply":
                mat1 = np.random.randint(1, 10, size=(3, 3))
                mat2 = np.random.randint(1, 10, size=(3, 3))
                result = np.matmul(mat1, mat2)
                result, t = check_realAndround(result)
                if not t:
                    # i = i - 1
                    continue
            elif operation == "inverse":
                mat1 = np.random.randint(1, 10, size=(3,3))
                result = np.linalg.inv(mat1)
                result, t = check_realAndround(result)
                if not t:
                    continue
            elif operation == "determinant":
                mat1 = np.random.randint(1, 10, size=(3, 3))
                result = np.linalg.det(mat1)
                result, t = check_realAndround(result)
                if not t:
                    # i = i - 1
                    continue
            elif operation == "eigenvalues":
                mat1 = np.random.randint(1, 10, size=(3, 3))
                eigenvalues = np.linalg.eigvals(mat1)
                result = eigenvalues
                result, t = check_realAndround(result)
                if not t:
                    # i = i - 1
                    continue
            elif operation == 'eigenvectors':
                mat1 = np.random.randint(1, 10, size=(3, 3))
                _, eigenvectors = np.linalg.eig(mat1)
                result = eigenvectors
                result, t = check_realAndround(result)
                if not t:
                    # i = i - 1
                    continue

            t = True
            submit = request.POST.get('submit')
            user_answer = None
            if submit:
                operation = request.POST.get('operation1')
                if operation == "add" or operation == "subtract" or operation == "multiply" or operation == "eigenvectors" or operation == "inverse":
                    if operation == "eigenvectors" or operation == "inverse":
                        mat1 = request.POST.get('mat1')
                        mat1 = str_to_matrix(mat1)
                        mat1 = float_to_int(mat1)
                    else:
                        mat1 = request.POST.get('mat1')
                        mat2 = request.POST.get('mat2')
                        mat1 = str_to_matrix(mat1)
                        mat2 = str_to_matrix(mat2)
                        mat1 = float_to_int(mat1)
                        mat2 = float_to_int(mat2)
                    user_answer = matrix_a
                    answer = request.POST.get('answer')
                    answer = str_to_matrix(answer)
                    if np.array_equal(answer, user_answer):
                        t1 = "True"
                    else:
                        t1 = "False"
                elif operation == "determinant":
                    mat1 = request.POST.get('mat1')
                    mat1 = str_to_matrix(mat1)
                    mat1 = float_to_int(mat1)
                    user_answer = request.POST.get('user_answer')
                    answer = request.POST.get('answer')
                    if float(answer) == float(user_answer):
                        t1 = "True"
                    else:
                        t1 = "False"
                else:
                    mat1 = request.POST.get('mat1')
                    mat1 = str_to_matrix(mat1)
                    mat1 = float_to_int(mat1)
                    user_answer = []
                    user_answer1 = request.POST.get('user_answer1')
                    user_answer2 = request.POST.get('user_answer2')
                    user_answer3 = request.POST.get('user_answer3')
                    user_answer.append(float(user_answer1))
                    user_answer.append(float(user_answer2))
                    user_answer.append(float(user_answer3))
                    answer = request.POST.get('answer')
                    answer = str_to_array(answer)
                    user_answer.sort()
                    answer.sort()
                    if user_answer == answer:
                        t1 = "True"
                    else:
                        t1 = "False"

    except ValueError as ve:
        error = str(ve)
    except Exception as e:
        error = str(e)
    return render(request, 'practice_questions.html',
                  {'operation1': operation, 'mat1': mat1, 'mat2': mat2, 'result': result, 'error': error,
                   'form_a': form_a, "t1": t1, 'user_answer': user_answer, 'answer': answer})

def menu(request):
    return render(request, 'menu.html')

def create_exercises(request):
    return render(request, 'create_exercises.html')

def create_new_exercise(request):
    return render(request, 'create_new_exercise.html')

def add_questions(request):
    
    result = ''
    error = ''
    form_a = MatrixAForm(request.POST or None, prefix='a')
    form_b = MatrixBForm(request.POST or None, prefix='b')

    if form_a.is_valid() and form_b.is_valid():
        matrix_a = []
        matrix_b = []

        for i in range(3):
            row_a = []
            row_b = []
            for j in range(3):
                row_a.append(form_a.cleaned_data[f'matrix_a_{i}{j}'])
                row_b.append(form_b.cleaned_data.get(f'matrix_b_{i}{j}', 0))
            matrix_a.append(row_a)
            matrix_b.append(row_b)

        matrix_a = np.array(matrix_a)
        matrix_b = np.array(matrix_b)
        is_matrix_b_provided = not (matrix_b == 0).all()

        operation = request.POST.get('operation')

        try:
            if operation == 'add':
                if is_matrix_b_provided:
                    result = matrix_a + matrix_b
                else:
                    error = 'Matrix B is required for addition.'
            elif operation == 'subtract':
                if is_matrix_b_provided:
                    result = matrix_a - matrix_b
                else:
                    error = 'Matrix B is required for subtraction.'
            elif operation == 'multiply':
                if is_matrix_b_provided:
                    result = matrix_a @ matrix_b
                else:
                    error = 'Matrix B is required for multiplication.'
            elif operation == 'determinant':
                result = np.linalg.det(matrix_a)
            elif operation == 'eigenvalues':
                eigenvalues, eigenvectors = np.linalg.eigvals(matrix_a)
                result = eigenvalues
            elif operation == 'eigenvectors':
                eigenvalues, eigenvectors = np.linalg.eig(matrix_a)
                result = eigenvectors
            elif operation == 'inverse':
                inverse = np.linalg.inv(matrix_a)
                result = inverse
            else:
                error = 'Invalid operation'
        except ValueError as ve:
            error = str(ve)
        except Exception as e:
            error = str(e)
        result = Round(result)
        result = str(result)

    return render(request, 'add_questions.html', {'form_a': form_a, 'form_b': form_b, 'result': result, 'error': error})