from test.integration.base import DBTIntegrationTest, use_profile


class BaseTestSimpleCopy(DBTIntegrationTest):
    @property
    def schema(self):
        return "simple_copy_001"

    @staticmethod
    def dir(path):
        return path.lstrip('/')

    @property
    def models(self):
        return self.dir("models")


class TestSimpleCopy(BaseTestSimpleCopy):

    @use_profile("postgres")
    def test__postgres__simple_copy(self):
        self.use_default_project({"data-paths": [self.dir("seed-initial")]})

        results = self.run_dbt(["seed"])
        self.assertEqual(len(results),  1)
        results = self.run_dbt()
        self.assertEqual(len(results),  7)

        self.assertManyTablesEqual(["seed", "view_model", "incremental", "materialized", "get_and_ref"])

        self.use_default_project({"data-paths": [self.dir("seed-update")]})
        results = self.run_dbt(["seed"])
        self.assertEqual(len(results),  1)
        results = self.run_dbt()
        self.assertEqual(len(results),  7)

        self.assertManyTablesEqual(["seed", "view_model", "incremental", "materialized", "get_and_ref"])

    @use_profile("postgres")
    def test__postgres__dbt_doesnt_run_empty_models(self):
        self.use_default_project({"data-paths": [self.dir("seed-initial")]})

        results = self.run_dbt(["seed"])
        self.assertEqual(len(results),  1)
        results = self.run_dbt()
        self.assertEqual(len(results),  7)

        models = self.get_models_in_schema()

        self.assertFalse("empty" in models.keys())
        self.assertFalse("disabled" in models.keys())

    @use_profile("presto")
    def test__presto__simple_copy(self):
        self.use_default_project({"data-paths": [self.dir("seed-initial")]})

        results = self.run_dbt(["seed"])
        self.assertEqual(len(results),  1)
        results = self.run_dbt(expect_pass=False)
        self.assertEqual(len(results),  7)
        for result in results:
            if 'incremental' in result.node.name:
                self.assertIn('not implemented for presto', result.error)

        self.assertManyTablesEqual(["seed", "view_model", "materialized"])

    @use_profile("snowflake")
    def test__snowflake__simple_copy(self):
        self.use_default_project({"data-paths": [self.dir("seed-initial")]})

        results = self.run_dbt(["seed"])
        self.assertEqual(len(results),  1)
        results = self.run_dbt()
        self.assertEqual(len(results),  7)

        self.assertManyTablesEqual(["SEED", "VIEW_MODEL", "INCREMENTAL", "MATERIALIZED", "GET_AND_REF"])

        self.use_default_project({"data-paths": [self.dir("seed-update")]})
        results = self.run_dbt(["seed"])
        self.assertEqual(len(results),  1)
        results = self.run_dbt()
        self.assertEqual(len(results),  7)

        self.assertManyTablesEqual(["SEED", "VIEW_MODEL", "INCREMENTAL", "MATERIALIZED", "GET_AND_REF"])

        self.use_default_project({
            "test-paths": [self.dir("tests")],
            "data-paths": [self.dir("seed-update")],
        })
        self.run_dbt(['test'])

    @use_profile("snowflake")
    def test__snowflake__simple_copy__quoting_off(self):
        self.use_default_project({
            "data-paths": [self.dir("seed-initial")],
            "quoting": {"identifier": False},
        })

        results = self.run_dbt(["seed"])
        self.assertEqual(len(results),  1)
        results = self.run_dbt()
        self.assertEqual(len(results),  7)

        self.assertManyTablesEqual(["SEED", "VIEW_MODEL", "INCREMENTAL", "MATERIALIZED", "GET_AND_REF"])

        self.use_default_project({
            "data-paths": [self.dir("seed-update")],
            "quoting": {"identifier": False},
        })
        results = self.run_dbt(["seed"])
        self.assertEqual(len(results),  1)
        results = self.run_dbt()
        self.assertEqual(len(results),  7)

        self.assertManyTablesEqual(["SEED", "VIEW_MODEL", "INCREMENTAL", "MATERIALIZED", "GET_AND_REF"])

        self.use_default_project({
            "test-paths": [self.dir("tests")],
            "data-paths": [self.dir("seed-update")],
            "quoting": {"identifier": False},
        })
        self.run_dbt(['test'])

    @use_profile("snowflake")
    def test__snowflake__seed__quoting_switch(self):
        self.use_default_project({
            "data-paths": [self.dir("seed-initial")],
            "quoting": {"identifier": False},
        })

        results = self.run_dbt(["seed"])
        self.assertEqual(len(results),  1)

        self.use_default_project({
            "data-paths": [self.dir("seed-update")],
            "quoting": {"identifier": True},
        })
        results = self.run_dbt(["seed"], expect_pass=False)

        self.use_default_project({
            "test-paths": [self.dir("tests")],
            "data-paths": [self.dir("seed-initial")],
        })
        self.run_dbt(['test'])

    @use_profile("bigquery")
    def test__bigquery__simple_copy(self):
        self.use_default_project({"data-paths": [self.dir("seed-initial")]})

        results = self.run_dbt(["seed"])
        self.assertEqual(len(results),  1)
        results = self.run_dbt()
        self.assertEqual(len(results),  7)

        self.assertTablesEqual("seed", "view_model")
        self.assertTablesEqual("seed", "incremental")
        self.assertTablesEqual("seed", "materialized")
        self.assertTablesEqual("seed", "get_and_ref")

        self.use_default_project({"data-paths": [self.dir("seed-update")]})

        results = self.run_dbt(["seed"])
        self.assertEqual(len(results),  1)
        results = self.run_dbt()
        self.assertEqual(len(results),  7)

        self.assertTablesEqual("seed", "view_model")
        self.assertTablesEqual("seed", "incremental")
        self.assertTablesEqual("seed", "materialized")
        self.assertTablesEqual("seed", "get_and_ref")


class TestSimpleCopyQuotingIdentifierOn(BaseTestSimpleCopy):
    @property
    def project_config(self):
        return {
            'quoting': {
                'identifier': True,
            },
        }

    @use_profile("snowflake")
    def test__snowflake__simple_copy__quoting_on(self):
        self.use_default_project({
            "data-paths": [self.dir("seed-initial")],
        })

        results = self.run_dbt(["seed"])
        self.assertEqual(len(results),  1)
        results = self.run_dbt()
        self.assertEqual(len(results),  7)

        self.assertManyTablesEqual(["seed", "view_model", "incremental", "materialized", "get_and_ref"])

        self.use_default_project({
            "data-paths": [self.dir("seed-update")],
        })
        results = self.run_dbt(["seed"])
        self.assertEqual(len(results),  1)
        results = self.run_dbt()
        self.assertEqual(len(results),  7)

        self.assertManyTablesEqual(["seed", "view_model", "incremental", "materialized", "get_and_ref"])

        # can't run the test as this one's identifiers will be the wrong case


class BaseLowercasedSchemaTest(BaseTestSimpleCopy):
    def unique_schema(self):
        # bypass the forced uppercasing that unique_schema() does on snowflake
        schema = super(BaseLowercasedSchemaTest, self).unique_schema()
        return schema.lower()


class TestSnowflakeSimpleLowercasedSchemaCopy(BaseLowercasedSchemaTest):
    @use_profile('snowflake')
    def test__snowflake__simple_copy(self):
        self.use_default_project({"data-paths": [self.dir("seed-initial")]})

        results = self.run_dbt(["seed"])
        self.assertEqual(len(results),  1)
        results = self.run_dbt()
        self.assertEqual(len(results),  7)

        self.assertManyTablesEqual(["SEED", "VIEW_MODEL", "INCREMENTAL", "MATERIALIZED", "GET_AND_REF"])

        self.use_default_project({"data-paths": [self.dir("seed-update")]})

        results = self.run_dbt(["seed"])
        self.assertEqual(len(results),  1)
        results = self.run_dbt()
        self.assertEqual(len(results),  7)

        self.assertManyTablesEqual(["SEED", "VIEW_MODEL", "INCREMENTAL", "MATERIALIZED", "GET_AND_REF"])

        self.use_default_project({
            "test-paths": [self.dir("tests")],
            "data-paths": [self.dir("seed-update")],
        })
        self.run_dbt(['test'])


class TestSnowflakeSimpleLowercasedSchemaQuoted(BaseLowercasedSchemaTest):
    @property
    def project_config(self):
        return {
            'quoting': {'identifier': False, 'schema': True}
        }

    @use_profile("snowflake")
    def test__snowflake__seed__quoting_switch_schema(self):
        self.use_default_project({
            "data-paths": [self.dir("seed-initial")],
        })

        results = self.run_dbt(["seed"])
        self.assertEqual(len(results),  1)

        self.use_default_project({
            "data-paths": [self.dir("seed-update")],
            "quoting": {"identifier": False, "schema": False},
        })
        results = self.run_dbt(["seed"], expect_pass=False)


class TestSnowflakeIncrementalOverwrite(BaseTestSimpleCopy):
    @property
    def models(self):
        return self.dir("models-snowflake")

    @use_profile("snowflake")
    def test__snowflake__incremental_overwrite(self):
        results = self.run_dbt(["run"])
        self.assertEqual(len(results),  1)

        results = self.run_dbt(["run"], expect_pass=False)
        self.assertEqual(len(results),  1)

        # Setting the incremental_strategy should make this succeed
        self.use_default_project({
            "models": {"incremental_strategy": "delete+insert"}
        })

        results = self.run_dbt(["run"])
        self.assertEqual(len(results),  1)


