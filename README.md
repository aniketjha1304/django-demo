# Django Inquiry Form - Interview Project

A simple Django web application that demonstrates a complete inquiry form system with validation, database operations, and dynamic data display. This project showcases fundamental Django concepts suitable for fresher-level interviews.

## 📋 Project Requirements

Based on the assignment, this application implements:

1. **HTML Form with Validation**:
   - First Name (alphabets only)
   - Last Name (alphabets only) 
   - Phone (numbers only)
   - Email (valid email format)
   - Gender (radio buttons)
   - Marital Status (radio buttons)

2. **Database Features**:
   - Auto-generated unique number: First 2 letters of first name + first letter of last name + random number
   - Example: "Sonia Chandra" → "SOC1234"

3. **Display Logic**:
   - Show records with proper salutation based on gender and marital status
   - Female + Married = "Mrs"
   - Male (any status) = "Mr"
   - Female + Single = "Miss"

## 🚀 Quick Setup Guide

### Prerequisites
- Python 3.8+ installed
- Basic knowledge of Django and HTML

### Installation Steps

1. **Clone the repository**:
```bash
git clone <repository-url>
cd django-demo
```

2. **Create virtual environment**:
```bash
python -m venv .venv
```

3. **Activate virtual environment**:
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

4. **Install dependencies**:
```bash
pip install django
```

5. **Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Start the server**:
```bash
python manage.py runserver
```

7. **Open in browser**:
```
http://127.0.0.1:8000/
```

## 📁 Project Structure

```
django-demo/
├── inquiry_project/          # Main project directory
│   ├── __init__.py
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py
├── inquiry_app/             # Main application
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   │   └── inquiry_app/
│   │       ├── base.html    # Base template
│   │       ├── form.html    # Form page
│   │       └── records.html # Records display
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py             # Form validation
│   ├── models.py            # Database models
│   ├── urls.py              # App URL configuration
│   └── views.py             # Business logic
├── manage.py                # Django management script
└── README.md
```

## 💻 Code Explanation

### 1. Models (models.py)

```python
class InquiryForm(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_CHOICES)
    unique_number = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Key Points**:
- Uses Django's built-in field types for automatic validation
- `EmailField` provides email format validation
- `choices` parameter creates dropdown/radio button options
- `unique=True` ensures no duplicate unique numbers
- `auto_now_add=True` automatically sets creation timestamp

**Unique Number Generation Logic**:
```python
def save(self, *args, **kwargs):
    if not self.unique_number:
        prefix = self.first_name[:2].upper() + self.last_name[:1].upper()
        random_num = random.randint(1000, 9999)
        self.unique_number = f"{prefix}{random_num}"
    super().save(*args, **kwargs)
```

**Salutation Logic**:
```python
def get_salutation(self):
    if self.gender == 'female' and self.marital_status == 'married':
        return 'Mrs'
    elif self.gender == 'male' and self.marital_status == 'married':
        return 'Mr'
    elif self.gender == 'female' and self.marital_status == 'single':
        return 'Miss'
    else:
        return 'Mr'  # Default for single male
```

### 2. Forms (forms.py)

```python
class InquiryFormForm(forms.ModelForm):
    class Meta:
        model = InquiryForm
        fields = ['first_name', 'last_name', 'phone', 'email', 'gender', 'marital_status']
```

**Key Features**:
- `ModelForm` automatically generates form fields from the model
- Custom validation methods for each field
- Bootstrap CSS classes for styling
- Server-side validation with detailed error messages

**Custom Validation Examples**:
```python
def clean_first_name(self):
    first_name = self.cleaned_data.get('first_name')
    if not re.match("^[A-Za-z ]+$", first_name):
        raise forms.ValidationError("First name should contain only characters.")
    return first_name
```

### 3. Views (views.py) - Function-Based Views

```python
def inquiry_form_view(request):
    if request.method == 'POST':
        form = InquiryFormForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inquiry form submitted successfully!')
            return redirect('show_records')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = InquiryFormForm()
    
    return render(request, 'inquiry_app/form.html', {'form': form})
```

**Key Points**:
- Uses function-based views (simpler for beginners)
- Handles both GET (display form) and POST (process form) requests
- Implements PRG pattern (Post-Redirect-Get) to prevent duplicate submissions
- Uses Django's messages framework for user feedback

### 4. URLs Configuration

**Main URLs (inquiry_project/urls.py)**:
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inquiry_app.urls')),
]
```

**App URLs (inquiry_app/urls.py)**:
```python
urlpatterns = [
    path('', views.inquiry_form_view, name='inquiry_form'),
    path('records/', views.show_records_view, name='show_records'),
]
```

### 5. Templates

**Base Template Structure**:
- Uses Bootstrap for responsive design
- Navigation between form and records
- Message display system
- Clean, professional layout

**Form Validation (JavaScript)**:
```javascript
function validateForm() {
    var firstName = document.getElementById('id_first_name').value;
    
    // Validate first name (only characters)
    if (!/^[A-Za-z ]+$/.test(firstName)) {
        alert('First name should contain only characters.');
        return false;
    }
    return true;
}
```

## 🧪 Testing Guide

### Manual Testing Steps

1. **Form Validation Testing**:
   - Enter numbers in name fields → Should show error
   - Enter letters in phone field → Should show error
   - Enter invalid email → Should show error
   - Submit empty form → Should show required field errors

2. **Unique Number Generation**:
   - Submit form with "John Doe" → Should generate "JOD" + 4 digits
   - Submit multiple forms → Each should have unique numbers

3. **Salutation Display**:
   - Female + Married → "Mrs"
   - Male + Any status → "Mr"
   - Female + Single → "Miss"

### Database Testing

Check the SQLite database:
```bash
python manage.py shell
>>> from inquiry_app.models import InquiryForm
>>> InquiryForm.objects.all()
>>> # View all records
```

## 🎯 Interview Question Preparation

### Common Questions & Answers

**Q: "Why did you use function-based views instead of class-based views?"**
A: Function-based views are simpler to understand and debug, especially for beginners. They provide clear control flow and are easier to customize for specific requirements.

**Q: "How does Django handle form validation?"**
A: Django provides multiple layers of validation:
1. Field-level validation (built-in field types)
2. Form-level validation (clean methods)
3. Model-level validation (model constraints)
4. Client-side validation (HTML5 + JavaScript)

**Q: "Explain the unique number generation logic."**
A: The system extracts the first 2 characters of the first name and first character of the last name, converts them to uppercase, and appends a random 4-digit number. This is implemented in the model's save() method to ensure it happens automatically.

**Q: "How do you prevent duplicate form submissions?"**
A: Using the PRG (Post-Redirect-Get) pattern - after a successful POST request, we redirect to another page instead of rendering a template directly.

**Q: "What's the difference between client-side and server-side validation?"**
A: 
- Client-side: Fast feedback, improves user experience, but can be bypassed
- Server-side: Secure, reliable, cannot be bypassed, handles business logic

### Technical Concepts Demonstrated

1. **Django MVT Pattern**: Models, Views, Templates separation
2. **Database Operations**: CRUD operations, model relationships
3. **Form Handling**: Form creation, validation, processing
4. **Template System**: Template inheritance, context variables
5. **URL Routing**: URL patterns, named URLs
6. **Security**: CSRF protection, form validation
7. **User Experience**: Messages framework, responsive design

## 🔧 Customization Options

### Adding New Fields
1. Add field to model
2. Create and run migration
3. Update form class
4. Update templates

### Changing Validation Rules
- Modify `clean_` methods in forms.py
- Update JavaScript validation
- Adjust model field constraints

### Styling Changes
- Modify CSS classes in forms.py widgets
- Update Bootstrap classes in templates
- Add custom CSS files

## 📚 Learning Resources

- [Django Official Documentation](https://docs.djangoproject.com/)
- [Django Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)

## 🐛 Common Issues & Solutions

**Issue**: Server not starting
**Solution**: Check if virtual environment is activated and Django is installed

**Issue**: Template not found
**Solution**: Verify template directory structure and settings.py configuration

**Issue**: Form not saving
**Solution**: Check form validation and model constraints

---

**Created by**: Fresher Developer for Interview Assessment
**Framework**: Django 5.2.4
**Purpose**: Demonstrating fundamental web development concepts