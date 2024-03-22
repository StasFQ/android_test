from abc import ABC, abstractmethod

from sqlalchemy import insert, select, func, update, delete

from database import async_session_maker
from sqlalchemy.exc import SQLAlchemyError


class AbstractRepository(ABC):
    """
    An abstract base class for repository implementations.

    Defines a common interface for repository operations such as adding, finding,
    and deleting records within a database. Implementations of this class are
    expected to provide concrete methods for these operations.
    """

    @abstractmethod
    async def add_one(self, data):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    """
    A concrete repository implementation using SQLAlchemy for database operations.

    This class provides methods for CRUD operations on a specified model using
    SQLAlchemy asynchronous session management.

    Attributes:
        model: The SQLAlchemy model class representing the database table.
    """

    model = None

    async def find_by_id(self, id: int):
        async with async_session_maker() as session:
            try:
                query = (
                    select(self.model)
                    .where(self.model.id == id)
                    .limit(1)
                )
                res = await session.execute(query)
                return res.scalar_one()
            except Exception as e:
                return e

    async def add_one(self, data: dict) -> int:
        """
        Adds a new record to the database based on the provided data dictionary.

        Parameters:
            data (dict): A dictionary containing the data for the new record.

        Returns:
            The ID of the newly created record.

        Raises:
            Exception: If an error occurs during the database operation.
        """

        async with async_session_maker() as session:
            try:
                stmt = insert(self.model).values(**data).returning(self.model.id)
                res = await session.execute(stmt)
                await session.commit()
                record_id = res.fetchone()[0]
                return record_id
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    async def find_all(self):
        """
        Retrieves all records from the database for the associated model.

        Returns:
            A list of model instances representing each record in the database.

        Raises:
            Exception: If an error occurs during the database operation.
        """

        async with async_session_maker() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            res = [row[0] for row in res.all()]
            return res

    async def find_one(self, id):
        """
        Retrieves a single record from the database by its ID.

        Parameters:
            id: The ID of the record to retrieve.

        Returns:
            The model instance representing the found record, or None if no record is found.

        Raises:
            Exception: If an error occurs during the database operation.
        """

        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id==id)
            res = await session.execute(stmt)
            return res.scalar_one()

    async def find_random(self):
        """
        Retrieves a random record from the database for the associated model.

        Returns:
            A model instance representing a randomly selected record.

        Raises:
            Exception: If an error occurs during the database operation.
        """

        async with async_session_maker() as session:
            stmt = select(self.model).order_by(func.random()).limit(1)
            res = await session.execute(stmt)
            return res.scalar_one()

    async def edit_one(self, id, updated_data):
        """
        Updates a record in the database with the provided data dictionary.

        Parameters:
            id: The ID of the record to update.
            updated_data (dict): A dictionary containing the updated data for the record.

        Returns:
            The updated model instance.

        Raises:
            Exception: If an error occurs during the database operation.
        """

        try:
            async with async_session_maker() as session:
                stmt = update(self.model).where(self.model.id == id).values(limit=int(updated_data['limit']), card_number=updated_data['card_number'],
                                                                            title=updated_data['title'], comment=updated_data['comment']).returning(self.model)
                result = await session.execute(stmt)
                await session.commit()
                updated_model = result.scalar_one()
                logger.info(f"Bank card {id} updated successfully")
                return updated_model
        except Exception as e:
            logger.error(f"Failed to update bank card {id}: {e}", exc_info=True)
            await session.rollback()
            raise e


    async def delete_one(self, id):
        """
        Deletes a record from the database by its ID.

        Parameters:
            id: The ID of the record to delete.

        Returns:
            True if the record was successfully deleted, False otherwise.

        Raises:
            Exception: If an error occurs during the database operation.
        """

        try:
            async with async_session_maker() as session:
                stmt = delete(self.model).where(self.model.id == id)
                result = await session.execute(stmt)
                await session.commit()
                if result.rowcount:
                    logger.info(f"Bank card {id} deleted successfully")
                    return True
                logger.warning(f"Bank card {id} not found or already deleted")
                return False
        except Exception as e:
            logger.error(f"Failed to delete bank card {id} due to error: {e}", exc_info=True)
            await session.rollback()
            return False