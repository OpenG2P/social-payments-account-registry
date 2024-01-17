CREATE INDEX ix_id_fa_mappings_fa_value ON id_fa_mappings USING btree (fa_value);

CREATE UNIQUE INDEX ix_id_fa_mappings_id_value ON id_fa_mappings USING btree (id_value);
