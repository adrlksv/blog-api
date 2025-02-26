from src.dao.base import BaseDAO
from src.users.models import User


class UsersDAO(BaseDAO):
    model = User
