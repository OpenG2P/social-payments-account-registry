ALTER TABLE ONLY dfsp_level_values ALTER COLUMN id SET DEFAULT nextval('dfsp_level_values_id_seq'::regclass);

ALTER TABLE ONLY dfsp_levels ALTER COLUMN id SET DEFAULT nextval('dfsp_levels_id_seq'::regclass);

ALTER TABLE ONLY dfsp_providers ALTER COLUMN id SET DEFAULT nextval('dfsp_providers_id_seq'::regclass);

ALTER TABLE ONLY fa_construct_strategy ALTER COLUMN id SET DEFAULT nextval('fa_construct_strategy_id_seq'::regclass);

ALTER TABLE ONLY id_providers ALTER COLUMN id SET DEFAULT nextval('id_providers_id_seq'::regclass);

ALTER TABLE ONLY login_providers ALTER COLUMN id SET DEFAULT nextval('login_providers_id_seq'::regclass);
