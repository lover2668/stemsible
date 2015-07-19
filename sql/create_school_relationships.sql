set foreign_key_checks = 0;

-- drop table /*! if exists */ school_relationships;

create table school_relationships (
  id                 integer unsigned not null auto_increment primary key,
  code               varchar(20)      not null,
  name               varchar(255)     not null,
  description        varchar(255)     ,
  active             boolean          not null,
  created            datetime         not null ,
  last_updated       timestamp        not null 
        default current_timestamp on update current_timestamp
) 
engine InnoDB default charset=utf8;
;

show warnings;

set foreign_key_checks = 1;

create trigger school_relationsihps_create before insert
   on school_relationships
   for each row set new.created = now();

load data local infile 'data/school_relationships.csv'
into table school_relationships
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;

desc school_relationships;