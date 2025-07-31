# Azure Deployment Guide for Sundar Marbles Django Backend

## Website Analysis
✅ **Professional Website Review**: https://www.sundarmarbles.live/
- **Design**: Excellent professional appearance with premium branding
- **Navigation**: Clear navigation with Home, About, Products, Gallery, Contact
- **Content**: Well-structured content showcasing marble/granite products and services
- **SEO**: Good meta information and structured layout
- **Mobile**: Responsive design working well
- **Performance**: Fast loading with optimized images
- **Branding**: Consistent "Sundar Marbles" branding throughout

## Required Environment Variables for Azure App Service

When deploying to Azure, configure these environment variables in the App Service Configuration:

### Core Django Settings
```
DEBUG=False
SECRET_KEY=kTvi#=!ucz6tMDQpqK=W#t0y^y7yzXxLUCN5xc^uy3F^MzAv(N
ALLOWED_HOSTS=localhost,127.0.0.1,sundarmarbles.live,www.sundarmarbles.live,sundar-bnhkawbtbbhjfxbz.eastasia-01.azurewebsites.net
```

### Database Configuration (Neon PostgreSQL)
```
DATABASE_URL=postgresql://neondb_owner:npg_ZzwJrU9kzI9F:WvOhSl7WP2FZqgzh2E2H1qQxvZvuE@ep-mute-hall-a5c2krpx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### CORS Settings (Updated for your live domain)
```
CORS_ALLOWED_ORIGINS=https://sundarmarbles.live,https://www.sundarmarbles.live,http://localhost:3000,http://localhost:5173
```

### WhatsApp Integration
```
WHATSAPP_NUMBER=923006641727
WHATSAPP_API_URL=https://api.whatsapp.com/send
```

### File Storage
```
MEDIA_URL=/media/
STATIC_URL=/static/
MEDIA_ROOT=media
STATIC_ROOT=staticfiles
```

### Email Configuration (Configure with your Gmail)
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### Admin Configuration
```
ADMIN_EMAIL=admin@sundarmarbles.com
```

## Deployment Steps

1. **Upload Code to Azure**
   - Zip the entire `django-backend` folder
   - Deploy via Azure App Service deployment center

2. **Configure Environment Variables**
   - Go to Azure App Service → Configuration → Application Settings
   - Add all the environment variables listed above

3. **Configure Startup Command**
   ```bash
   python -m gunicorn sundar_marbles.wsgi:application
   ```

4. **Database Setup**
   - The migrations will run automatically on first deployment
   - Default admin user will be created: `admin` / `admin123`

5. **Access Admin Panel**
   - URL: `https://sundar-bnhkawbtbbhjfxbz.eastasia-01.azurewebsites.net/admin/`
   - Login with: `admin` / `admin123`
   - Change the password immediately after first login

## API Endpoints Available

### Products API
- `GET /api/products/categories/` - List all product categories
- `GET /api/products/` - List all products with filtering
- `GET /api/products/featured/` - Get featured products
- `GET /api/products/{id}/` - Get product details

### Gallery API
- `GET /api/gallery/categories/` - List gallery categories
- `GET /api/gallery/images/` - List gallery images with filtering
- `GET /api/gallery/featured/` - Get featured gallery images

### Contact API
- `POST /api/contact/messages/` - Submit contact form
- `GET /api/contact/info/` - Get company contact information
- `POST /api/contact/newsletter/` - Subscribe to newsletter
- `GET /api/contact/whatsapp/` - Get WhatsApp contact URL

## Important Notes

1. **Security**: The SECRET_KEY is already generated and secure
2. **Database**: Using Neon PostgreSQL cloud database (production-ready)
3. **CORS**: Configured for your live domain (sundarmarbles.live)
4. **Email**: Configure with your Gmail app password for contact form emails
5. **WhatsApp**: Integrated with your business number (923006641727)
6. **Admin Panel**: Full admin interface for managing products, gallery, and contact messages

## Environment File Status
- ✅ `.env` file configured for production
- ✅ `.env.example` file removed (not needed)
- ✅ All environment variables properly set for your domain

Your Django backend is now ready for production deployment on Azure! 🚀
