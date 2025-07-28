from sqlmodel import Field, SQLModel, Column, CheckConstraint, String
from .region import Region


class Country(SQLModel, table=True):
    __tablename__ = 'country'
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, sa_column=Column(
        String(1024), nullable=False))
    population: int = Field(sa_column_args=(
        CheckConstraint("population>=0"),))
    datasource: str = Field(min_length=1, sa_column=Column(
        String(1024), nullable=False))
    region_id: int = Field(foreign_key='region.id')

    def __str__(self):
        return f"Country:{self.name} Population:{self.population}" + \
            f"\n\tDatasource:{self.datasource} RegionID:{self.region_id}"
