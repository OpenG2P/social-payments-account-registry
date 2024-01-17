CREATE TABLE fa_construct_strategy (
    id integer NOT NULL,
    strategy character varying NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    active boolean NOT NULL
);

CREATE TABLE dfsp_providers (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying,
    code character varying(20) NOT NULL,
    strategy_id integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    active boolean NOT NULL
);

CREATE TABLE id_providers (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying,
    code character varying(20) NOT NULL,
    strategy_id integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    active boolean NOT NULL
);

CREATE TABLE login_providers (
    id integer NOT NULL,
    name character varying NOT NULL,
    type public.loginprovidertypes NOT NULL,
    description character varying,
    login_button_text character varying,
    login_button_image_url character varying,
    authorization_parameters json NOT NULL,
    id_provider_id integer,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    active boolean NOT NULL
);

CREATE TABLE dfsp_levels (
    id integer NOT NULL,
    name character varying NOT NULL,
    code character varying(20) NOT NULL,
    level integer NOT NULL,
    next_level_id integer,
    validation_regex character varying,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    active boolean NOT NULL
);

CREATE TABLE dfsp_level_values (
    id integer NOT NULL,
    name character varying NOT NULL,
    code character varying(20) NOT NULL,
    parent_id integer,
    level_id integer NOT NULL,
    next_level_id integer,
    dfsp_provider_id integer,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    active boolean NOT NULL
);

CREATE TABLE id_fa_mappings (
    id integer NOT NULL,
    name character varying,
    id_value character varying NOT NULL,
    fa_value character varying NOT NULL,
    phone character varying,
    additional_info json,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    active boolean NOT NULL
);
