from django.contrib.auth.models import User;
from datacenter.models import UserProfile;
# Creating Django Admin ------------------------------------------------
user,status = User.objects.get_or_create(username='admin@mobisir.net');
user.email = 'admin@mobisir.net';
user.first_name = 'Admin';
user.last_name = 'NF';
user.is_active = True;
user.is_superuser = True;
user.is_staff = True;
user.set_password('nftp@123#');
user.save();
user_profile = UserProfile.objects.get(user=user);
user_profile.is_admin = False;
user_profile.first_name = user.first_name;
user_profile.last_name = user.last_name;
user_profile.email = user.email;
user_profile.save();

# Creating NF Admin ---------------------------------------------------
user,status = User.objects.get_or_create(username='nfadmin@mobisir.net');
user.email = 'nfadmin@mobisir.net';
user.first_name = 'NorthFacing';
user.last_name = 'Admin';
user.is_active = True;
user.is_superuser = False;
user.is_staff = True;
user.set_password('nfadmin@123#');
user.save();
user_profile = UserProfile.objects.get(user=user);
user_profile.is_admin = True;
user_profile.first_name = user.first_name;
user_profile.last_name = user.last_name;
user_profile.email = user.email;
user_profile.save();
exit();
