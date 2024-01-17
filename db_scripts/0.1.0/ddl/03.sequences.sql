CREATE SEQUENCE dfsp_level_values_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE dfsp_level_values_id_seq OWNED BY dfsp_level_values.id;

CREATE SEQUENCE dfsp_levels_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE dfsp_levels_id_seq OWNED BY dfsp_levels.id;

CREATE SEQUENCE dfsp_providers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE dfsp_providers_id_seq OWNED BY dfsp_providers.id;

CREATE SEQUENCE fa_construct_strategy_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE fa_construct_strategy_id_seq OWNED BY fa_construct_strategy.id;

CREATE SEQUENCE id_providers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE id_providers_id_seq OWNED BY id_providers.id;

CREATE SEQUENCE login_providers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE login_providers_id_seq OWNED BY login_providers.id;

CREATE SEQUENCE id_fa_mappings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE id_fa_mappings_id_seq OWNED BY id_fa_mappings.id;
