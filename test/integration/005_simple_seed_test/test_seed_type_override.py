from test.integration.base import DBTIntegrationTest, use_profile


class TestSimpleSeedColumnOverride(DBTIntegrationTest):

    @property
    def schema(self):
        return "simple_seed_005"

    @property
    def project_config(self):
        return {
            "data-paths": ['data-config'],
            "macro-paths": ['macros'],
            "seeds": {
                "test": {
                    "enabled": False,
                    "seed_enabled": {
                        "enabled": True,
                        "column_types": self.seed_types()
                    },
                }
            }
        }


class TestSimpleSeedColumnOverridePostgres(TestSimpleSeedColumnOverride):
    @property
    def models(self):
        return "models-pg"

    @property
    def profile_config(self):
        return self.postgres_profile()

    def seed_types(self):
        return {
            "id": "text",
            "birthday": "date",
        }

    @use_profile('postgres')
    def test_simple_seed_with_column_override_postgres(self):
        results = self.run_dbt(["seed"])
        self.assertEqual(len(results),  1)
        results = self.run_dbt(["test"])
        self.assertEqual(len(results),  2)


class TestSimpleSeedColumnOverrideRedshift(TestSimpleSeedColumnOverride):
    @property
    def models(self):
        return "models-rs"

    @property
    def profile_config(self):
        return self.redshift_profile()

    def seed_types(self):
        return {
            "id": "text",
            "birthday": "date",
        }

    @use_profile('redshift')
    def test_simple_seed_with_column_override_redshift(self):
        results = self.run_dbt(["seed"])
        self.assertEqual(len(results),  1)
        results = self.run_dbt(["test"])
        self.assertEqual(len(results),  2)


class TestSimpleSeedColumnOverrideSnowflake(TestSimpleSeedColumnOverride):
    @property
    def models(self):
        return "models-snowflake"

    def seed_types(self):
        return {
            "id": "FLOAT",
            "birthday": "TEXT",
        }

    @property
    def profile_config(self):
        return self.snowflake_profile()

    @use_profile('snowflake')
    def test_simple_seed_with_column_override_snowflake(self):
        results = self.run_dbt(["seed"])
        self.assertEqual(len(results),  1)
        results = self.run_dbt(["test"])
        self.assertEqual(len(results),  2)


class TestSimpleSeedColumnOverrideBQ(TestSimpleSeedColumnOverride):
    @property
    def models(self):
        return "models-bq"

    def seed_types(self):
        return {
            "id": "FLOAT64",
            "birthday": "STRING",
        }

    @property
    def profile_config(self):
        return self.bigquery_profile()

    @use_profile('bigquery')
    def test_simple_seed_with_column_override_bigquery(self):
        results = self.run_dbt(["seed"])
        self.assertEqual(len(results),  1)
        results = self.run_dbt(["test"])
        self.assertEqual(len(results),  2)
