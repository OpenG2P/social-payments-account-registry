ALTER TABLE ONLY dfsp_level_values
    ADD CONSTRAINT dfsp_level_values_pkey PRIMARY KEY (id);

ALTER TABLE ONLY dfsp_levels
    ADD CONSTRAINT dfsp_levels_pkey PRIMARY KEY (id);

ALTER TABLE ONLY dfsp_providers
    ADD CONSTRAINT dfsp_providers_pkey PRIMARY KEY (id);

ALTER TABLE ONLY fa_construct_strategy
    ADD CONSTRAINT fa_construct_strategy_pkey PRIMARY KEY (id);

ALTER TABLE ONLY id_providers
    ADD CONSTRAINT id_providers_pkey PRIMARY KEY (id);

ALTER TABLE ONLY login_providers
    ADD CONSTRAINT login_providers_pkey PRIMARY KEY (id);

ALTER TABLE ONLY dfsp_level_values
    ADD CONSTRAINT dfsp_level_values_dfsp_provider_id_fkey FOREIGN KEY (dfsp_provider_id) REFERENCES dfsp_providers(id);

ALTER TABLE ONLY dfsp_level_values
    ADD CONSTRAINT dfsp_level_values_level_id_fkey FOREIGN KEY (level_id) REFERENCES dfsp_levels(id);

ALTER TABLE ONLY dfsp_level_values
    ADD CONSTRAINT dfsp_level_values_next_level_id_fkey FOREIGN KEY (next_level_id) REFERENCES dfsp_levels(id);

ALTER TABLE ONLY dfsp_level_values
    ADD CONSTRAINT dfsp_level_values_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES dfsp_level_values(id);

ALTER TABLE ONLY dfsp_levels
    ADD CONSTRAINT dfsp_levels_next_level_id_fkey FOREIGN KEY (next_level_id) REFERENCES dfsp_levels(id) NOT VALID;

ALTER TABLE ONLY dfsp_providers
    ADD CONSTRAINT dfsp_providers_strategy_id_fkey FOREIGN KEY (strategy_id) REFERENCES fa_construct_strategy(id);

ALTER TABLE ONLY id_providers
    ADD CONSTRAINT id_providers_strategy_id_fkey FOREIGN KEY (strategy_id) REFERENCES fa_construct_strategy(id);

ALTER TABLE ONLY login_providers
    ADD CONSTRAINT login_providers_id_provider_id_fkey FOREIGN KEY (id_provider_id) REFERENCES id_providers(id);
