DB_NAME = 'flaskr'

TABLES = {}
TABLES['user'] = (
    "CREATE TABLE `flaskr`.`user` ( "
    "`id` INT NOT NULL AUTO_INCREMENT , "
    "`username` VARCHAR(32) NOT NULL , "
    "`password` TEXT NOT NULL , "
    "PRIMARY KEY (`id`), "
    "UNIQUE (`username`)"
    ") ENGINE = InnoDB")

TABLES['posts'] = (
    "CREATE TABLE `flaskr`.`post` ("
    " `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    " `author_id` INT NOT NULL,"
    " `created` DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,"
    " `title` TEXT NOT NULL,"
    " `body` TEXT NOT NULL,"
    " FOREIGN KEY (author_id) REFERENCES `flaskr`.`user` (id)"
    ") ENGINE = InnoDB")
