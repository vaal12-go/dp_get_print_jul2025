from sqlmodel import Field, SQLModel, UniqueConstraint, Column, String, CheckConstraint

CONTINENTAL_REGION = 1
STATISTICAL_SUBREGION = 2


class Region(SQLModel, table=True):
    # __table_args__ = (
    #     UniqueConstraint("name", "type",
    #                      name="region_table_name_and_type_must_be_unique"),
    # )
    __tablename__ = 'region'
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, sa_column=Column(
        String(1024), nullable=False))
    type: str = Field(min_length=1, sa_column=Column(
        String(1024), nullable=False))
    datasource: str = Field(min_length=1, sa_column=Column(
        String(1024), nullable=False))
    data_year: int

    def __str__(self):
        return f"Region:{self.name} Type:{self.type} \n\tYear:{self.data_year} Datasource:{self.datasource}"
