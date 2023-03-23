from django.shortcuts import render
from .forms import MatrixAForm, MatrixBForm
import numpy as np

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
                eigenvalues, eigenvectors = np.linalg.eig(matrix_a)
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

        result = str(result)

    return render(request, 'index.html', {'form_a': form_a, 'form_b': form_b, 'result': result, 'error': error})