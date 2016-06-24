


## EU LIST

Date and Datetime always on [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format.

Date: YYYY-MM-DD 
DateTime: YYYY-MM-DDTHH:MM:SS

| XS | SQLite | SQLAlchemy |
| -- | ---    | --- |
| DateType |  VARCHAR(10) | db.Date() |
| DateTimeType | VARCHAR(19) | db.DateTime() |
| BooleanType | INT | db.Boolean() |
| LanguageCodeType | VARCHAR(6) | db.String(6) |
| Iso2CodeType | VARCHAR(2) | db.String(2) |
| DefaultCodeType | VARCHAR(32) |db.String(32) |
| DefaultDescriptionType | VARCHAR(256) | db.String(256) |
| LargeDescriptionType | VARCHAR(2048) | db.String(2048) |
| DefaultUrlType | VARCHAR(512) | db.String(512) |
| UnlimitedTextType | TEXT | db.Text() |

func def_desc_type():
	return db.String(256)

func large_desc_type():
	return db.String(2048)

func url_type():
	return db.String(512)




class Countries(db.Model):
	id = db.Column(db.String(3), primary_key=True) # iso3
	iso2 = db.Column(db.String(2), nullable=False)
	description = db.Column(def_desc_type(), nullable=False)

class Sanctioners(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	




### Lists to include on de Db
Lists(id, description, url, last_download)

### Countries
Countries( iso2 VARCHAR(2) PRIMARY KEY,

	, iso3, description)

### An entity can be a person, organization, ...
Entity_type(id char(3), description CHAR())

