from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    
    def create_user(self,email,password=None,**kwargs):
        email = self.normalize_email(email)
        
        if not email:
            raise ValueError("Email address must be required")
        
        user = self.model(
            email=email,
            **kwargs
        )
        
        user.set_password(password)
        
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self,email,password=None,**kwargs):
        user = self.create_user(
            email=email,
            password=password,
            **kwargs
        )

        user.is_staff=True
        user.is_active=True
        user.is_superuser=True
        
        user.save(using=self._db)
        
        return user