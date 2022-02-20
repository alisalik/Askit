from rest_framework import serializers
from accounts.models import UserProfile

class UserSerializer(serializers.ModelSerializer):

    #uutoken = serializers.ReadOnlyField()
    class Meta:
        model= UserProfile
        fields=('email','name','password','city','country')
        extra_kwargs={
            'password':
                {
                    'write_only':True,
                    'style':{'input_type':'password'}
                }
        }

    def create(self,validated_data):
        password= validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance

    def update(self,instance,validated_data):
        for att,val in validated_data.items():
            if att=='password':
                instance.set_password(val)
            else:
                setattr(instance,att,val)
        instance.save()
        return instance
