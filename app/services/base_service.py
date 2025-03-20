from typing import Any, Generic, TypeVar
from uuid import UUID

from core.exceptions import NotFoundException
from models import Base
from pydantic import BaseModel
from repositories import BaseRepository

ModelType = TypeVar("ModelType", bound=Base)


class BaseService(Generic[ModelType]):
    """Base class for data controllers."""

    def __init__(self, model: type[ModelType], repository: BaseRepository):
        self.model_class = model
        self.repository = repository

    def get_by_id(self, id_: int, join_: set[str] | None = None) -> ModelType:
        """
        Returns the model instance matching the id.

        :param id_: The id to match.
        :param join_: The joins to make.
        :return: The model instance.
        """

        db_obj = self.repository.get_by(field="id", value=id_, join_=join_, unique=True)
        if not db_obj:
            raise NotFoundException(
                f"{self.model_class.__tablename__.title()} with id: {id} does not exist"
            )

        return db_obj

    def get_by_uuid(self, uuid: UUID, join_: set[str] | None = None) -> ModelType:
        """
        Returns the model instance matching the uuid.

        :param uuid: The uuid to match.
        :param join_: The joins to make.
        :return: The model instance.
        """

        db_obj = self.repository.get_by(
            field="uuid", value=uuid, join_=join_, unique=True
        )
        if not db_obj:
            raise NotFoundException(
                f"{self.model_class.__tablename__.title()} with id: {uuid} does not exist"
            )
        return db_obj

    def get_all(
        self, skip: int = 0, limit: int = 100, join_: set[str] | None = None
    ) -> list[ModelType]:
        """
        Returns a list of records based on pagination params.

        :param skip: The number of records to skip.
        :param limit: The number of records to return.
        :param join_: The joins to make.
        :return: A list of records.
        """

        response = self.repository.get_all(skip, limit, join_)
        return response

    def create(self, attributes: dict[str, Any]) -> ModelType | None:
        """
        Creates a new Object in the DB.

        :param attributes: The attributes to create the object with.
        :return: The created object.
        """
        session = self.repository.session
        try:
            with session.begin():
                create_object = self.repository.create(attributes)
                return create_object
        except Exception as e:
            session.rollback()
            raise e

    def delete(self, model: ModelType) -> bool:
        """
        Deletes the Object from the DB.

        :param model: The model to delete.
        :return: True if the object was deleted, False otherwise.
        """
        delete_obj = self.repository.delete(model)
        return delete_obj

    @staticmethod
    def extract_attributes_from_schema(
        schema: BaseModel, excludes: set = None
    ) -> dict[str, Any]:
        """
        Extracts the attributes from the schema.

        :param schema: The schema to extract the attributes from.
        :param excludes: The attributes to exclude.
        :return: The attributes.
        """

        return schema.model_dump(exclude=excludes, exclude_unset=True)

    def update(self, model: ModelType, attributes: dict[str, Any]) -> ModelType:
        """
        Updates the Object in the DB.

        :param
        model: The model to update.
        attributes: The attributes to update the object with.
        :return: The updated object.
        """
        
        update_object = self.repository.update(model, attributes)
        return update_object