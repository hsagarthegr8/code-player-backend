from accounts.models import User, Profile

from rest_framework.serializers import ModelSerializer, CharField


class ProfileSerializer(ModelSerializer):
    occupation = CharField(source='get_occupation_display')

    class Meta:
        model = Profile
        exclude = ('user',)
        depth = 1


class UserSerializer(ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'profile')
        extra_kwargs = {
            'password': {'write_only': True, 'style': {
                'input_type': 'password'
            }}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

        return user
