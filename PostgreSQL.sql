CREATE DATABASE wiener_daten;

CREATE TABLE einkommen (
    district_code INTEGER,
    ref_year INTEGER,
    inc_tot_value NUMERIC,
    inc_mal_value NUMERIC,
    inc_fem_value NUMERIC
);


CREATE TABLE geburten (
    district_code INTEGER,
    ref_year INTEGER,
    births INTEGER
);
