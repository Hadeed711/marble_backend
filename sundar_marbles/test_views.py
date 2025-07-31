from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

def test_basic(request):
    """Test basic Django functionality"""
    return JsonResponse({
        'status': 'success',
        'message': 'Django is working!',
        'debug': True
    })

def test_database(request):
    """Test database connection"""
    try:
        user_count = User.objects.count()
        return JsonResponse({
            'status': 'success',
            'message': 'Database connection working!',
            'user_count': user_count
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

@csrf_exempt
def test_login(request):
    """Test login functionality"""
    if request.method == 'POST':
        try:
            from django.contrib.auth import authenticate
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(username=username, password=password)
            if user:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Authentication successful!',
                    'user': user.username
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid credentials'
                })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return HttpResponse('''
    <form method="post">
        <input type="text" name="username" placeholder="Username" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit">Test Login</button>
    </form>
    <script>
        document.querySelector('form').onsubmit = function(e) {
            e.preventDefault();
            const username = document.querySelector('input[name="username"]').value;
            const password = document.querySelector('input[name="password"]').value;
            fetch('/test/login/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, password})
            }).then(r => r.json()).then(data => alert(JSON.stringify(data)));
        }
    </script>
    ''')
