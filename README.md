## weFloat - Backend Capstone
weFloat is a Python/Django application which allows users to create and share their favorite floats in Tennessee. 



## Setup

1. Clone the template repository.
2. Activate the Pipenv environment with pipenv shell.
4. Install the dependencies using pipenv install.
6. Open the project in Visual Studio Code.
7. Ensure that the correct interpreter is selected.
8. Run python manage.py runserver


## Users
- The ideal user for this application are Kayakers or anyone looking to for new floats. 

## Features
- Create, Read, Update, and Delete floats
- Create, Read, Update, and Delete comments on floats
- Create, Read, Update, and Delete user profiles
- Create, Read, Update, and Delete tags 
- Create, Read, Update, and Delete floatTags (many-to-many relationship)
  
## Links
- ERD - https://dbdiagram.io/d/weFloat-ERD-6785b5e36b7fa355c3c612f9
- Project Board - https://github.com/users/Jayoussef28/projects/4
API Documentation -
Postman Loom - 
Test Loom - 

## Code Snippet
class Float(models.Model):

    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    description = models.CharField(max_length=500)
    distance = models.CharField(max_length=10) 
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE,null=False)
    image = models.TextField(default="https://i.pinimg.com/564x/42/23/7b/42237b9fd34b36ad15aca8788f6c9339.jpg")
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, null=False)
    created_on = models.DateField(auto_now_add=True)
    





## Contributors
- Jordan Youssef (https://github.com/Jayoussef28)
