from sqlalchemy.orm import Session

from app.db.schema import User

class UserService:
    def __init__(self, session: Session):
        self._db = session

    def list_users(self) -> list[User]:
        return self._db.query(User).all()
    
    def get_user(self, user_id: int) -> User | None:
        return self._db.query(User).filter(User.id == user_id).first()
    
    def create_user(self, username: str) -> User:
        new_user = User(name=username)
        self._db.add(new_user)
        self._db.commit()
        self._db.refresh(new_user)
        return new_user
    
    def update_user(self, user_id: int, username: str | None = None) -> User | None:
        user = self.get_user(user_id)
        if not user:
            return None
        if username:
            user.name = username
        self._db.commit()
        self._db.refresh(user)
        return user
    
    def delete_user(self, user_id: int) -> bool:
        user = self.get_user(user_id)
        if not user:
            return False
        self._db.delete(user)
        self._db.commit()
        return True