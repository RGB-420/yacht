BEGIN;


CREATE TABLE IF NOT EXISTS yacht_db.regattas
(
    id_regatta integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    name text NOT NULL,
    type text,
    id_club integer,
    id_location integer,
    created_at timestamp with time zone DEFAULT NOW(),
    PRIMARY KEY (id_regatta),
    UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS yacht_db.regatta_editions
(
    id_edition integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    id_regatta integer NOT NULL,
    year integer NOT NULL,
    created_at timestamp with time zone DEFAULT NOW(),
    PRIMARY KEY (id_edition),
    UNIQUE (year, id_regatta)
);

CREATE TABLE IF NOT EXISTS yacht_db.owners
(
    id_owner integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    name text NOT NULL,
    created_at timestamp with time zone DEFAULT NOW(),
    PRIMARY KEY (id_owner),
    UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS yacht_db.clubs
(
    id_club integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    name text NOT NULL,
    short_name text,
    estimated_numbers integer,
    id_location integer,
    created_at timestamp with time zone DEFAULT NOW(),
    PRIMARY KEY (id_club),
    UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS yacht_db.locations
(
    id_location integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    city text,
    region text,
    country text,
    PRIMARY KEY (id_location),
    UNIQUE (region, country, city)
);

CREATE TABLE IF NOT EXISTS yacht_db.regatta_links
(
    id_link integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    id_edition integer NOT NULL,
    url text NOT NULL,
    PRIMARY KEY (id_link),
    UNIQUE (id_edition, url)
);

CREATE TABLE IF NOT EXISTS yacht_db.boat_classes
(
    id_class integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    name text NOT NULL,
    manufacturer text,
    category text,
    rating_rule text,
    start_year integer,
    crew_min integer,
    crew_max integer,
    length_m numeric(5, 2),
    created_at timestamp with time zone DEFAULT NOW(),
    PRIMARY KEY (id_class),
    UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS yacht_db.edition_classes
(
    id_edition integer NOT NULL,
    id_class integer NOT NULL,
    PRIMARY KEY (id_edition, id_class)
);

CREATE TABLE IF NOT EXISTS yacht_db.boats
(
    id_boat integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    name text NOT NULL,
    boat_identifier text,
    id_type integer,
    created_at timestamp with time zone DEFAULT NOW(),
    PRIMARY KEY (id_boat),
    UNIQUE (name, boat_identifier)
);

CREATE TABLE IF NOT EXISTS yacht_db.boat_type
(
    id_type integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    name text NOT NULL,
    id_class integer,
    created_at timestamp with time zone DEFAULT NOW(),
    PRIMARY KEY (id_type),
    UNIQUE (name, id_class)
);

CREATE TABLE IF NOT EXISTS yacht_db.boats_owner
(
    id_boat integer NOT NULL,
    id_owner integer NOT NULL,
    PRIMARY KEY (id_boat, id_owner)
);

CREATE TABLE IF NOT EXISTS yacht_db.boat_editions
(
    id_boat integer NOT NULL,
    id_edition integer NOT NULL,
    PRIMARY KEY (id_boat, id_edition)
);

CREATE TABLE IF NOT EXISTS yacht_db.boat_clubs
(
    id_boat integer NOT NULL,
    id_club integer NOT NULL,
    PRIMARY KEY (id_boat, id_club)
);

CREATE TABLE IF NOT EXISTS yacht_raw.raw_regatta_results
(
    id_raw_result integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    source_type text,
    source_page text,
    regatta_name text,
    year integer,
    scraped_at timestamp with time zone DEFAULT NOW(),
    raw_data jsonb,
    PRIMARY KEY (id_raw_result)
);

ALTER TABLE IF EXISTS yacht_db.regattas
    ADD FOREIGN KEY (id_location)
    REFERENCES yacht_db.locations (id_location) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS yacht_db.regattas
    ADD FOREIGN KEY (id_club)
    REFERENCES yacht_db.clubs (id_club) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS yacht_db.regatta_editions
    ADD FOREIGN KEY (id_regatta)
    REFERENCES yacht_db.regattas (id_regatta) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS yacht_db.clubs
    ADD FOREIGN KEY (id_location)
    REFERENCES yacht_db.locations (id_location) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS yacht_db.regatta_links
    ADD FOREIGN KEY (id_edition)
    REFERENCES yacht_db.regatta_editions (id_edition) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS yacht_db.edition_classes
    ADD FOREIGN KEY (id_class)
    REFERENCES yacht_db.boat_classes (id_class) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS yacht_db.edition_classes
    ADD FOREIGN KEY (id_edition)
    REFERENCES yacht_db.regatta_editions (id_edition) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS yacht_db.boats
    ADD FOREIGN KEY (id_type)
    REFERENCES yacht_db.boat_type (id_type) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS yacht_db.boat_type
    ADD FOREIGN KEY (id_class)
    REFERENCES yacht_db.boat_classes (id_class) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS yacht_db.boats_owner
    ADD FOREIGN KEY (id_boat)
    REFERENCES yacht_db.boats (id_boat) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS yacht_db.boats_owner
    ADD FOREIGN KEY (id_owner)
    REFERENCES yacht_db.owners (id_owner) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS yacht_db.boat_editions
    ADD FOREIGN KEY (id_boat)
    REFERENCES yacht_db.boats (id_boat) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS yacht_db.boat_editions
    ADD FOREIGN KEY (id_edition)
    REFERENCES yacht_db.regatta_editions (id_edition) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS yacht_db.boat_clubs
    ADD FOREIGN KEY (id_boat)
    REFERENCES yacht_db.boats (id_boat) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS yacht_db.boat_clubs
    ADD FOREIGN KEY (id_club)
    REFERENCES yacht_db.clubs (id_club) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;