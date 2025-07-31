from django.http import JsonResponse
from django.db import connection
from django.contrib.auth import get_user_model
import traceback


def debug_database(request):
    """Debug endpoint to test database connectivity"""
    result = {
        'database_connection': False,
        'tables_exist': False,
        'users_count': 0,
        'superuser_exists': False,
        'errors': []
    }
    
    try:
        # Test basic database connection
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            result['database_connection'] = True
            
        # Test if Django tables exist
        cursor.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='auth_user')")
        result['tables_exist'] = cursor.fetchone()[0]
        
        if result['tables_exist']:
            # Count users
            User = get_user_model()
            result['users_count'] = User.objects.count()
            result['superuser_exists'] = User.objects.filter(is_superuser=True).exists()
            
            # List all users
            users = list(User.objects.values('username', 'email', 'is_superuser', 'is_staff'))
            result['users'] = users
            
    except Exception as e:
        result['errors'].append({
            'error': str(e),
            'traceback': traceback.format_exc()
        })
    
    return JsonResponse(result, indent=2)


def force_create_superuser(request):
    """Force create superuser regardless of existing state"""
    result = {'success': False, 'message': '', 'errors': []}
    
    try:
        User = get_user_model()
        
        # Delete all existing admin users
        deleted_count = User.objects.filter(username='admin').delete()[0]
        result['deleted_users'] = deleted_count
        
        # Create new superuser
        user = User.objects.create_superuser(
            username='admin',
            email='admin@sundarmarbles.com',
            password='admin123456'
        )
        
        result['success'] = True
        result['message'] = f'Superuser created successfully: {user.username}'
        result['user_id'] = user.id
        
    except Exception as e:
        result['errors'].append({
            'error': str(e),
            'traceback': traceback.format_exc()
        })
    
    return JsonResponse(result, indent=2)
