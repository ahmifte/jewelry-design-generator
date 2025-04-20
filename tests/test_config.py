import os
from unittest.mock import patch, mock_open

from python_jewelry_design_gen.utils.config import load_config


class TestConfig:
    def test_load_config_from_env(self):
        """Test loading configuration from environment variables."""
        with patch.dict(os.environ, {
            "MESHY_API_KEY": "test-api-key",
            "MESHY_API_BASE_URL": "https://test-api.example.com",
            "OUTPUT_DIR": "test-output",
            "MODELS_DIR": "test-models-dir",
            "METADATA_DIR": "test-metadata-dir",
        }):
            config = load_config()

            # Verify config values from environment
            assert config.get("meshy_api_key") == "test-api-key"
            assert config.get(
                "meshy_api_base_url") == "https://test-api.example.com"
            assert config.get("output_dir") == "test-output"
            assert config.get("models_dir") == "test-models-dir"
            assert config.get("metadata_dir") == "test-metadata-dir"

    @patch("python_jewelry_design_gen.utils.config.Path.exists")
    @patch("python_jewelry_design_gen.utils.config.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_config_from_file(
            self,
            mock_file,
            mock_json_load,
            mock_exists
    ):
        """Test loading configuration from config file."""
        mock_exists.return_value = True

        # Mock json.load to return test config
        mock_json_load.return_value = {
            "meshy_api_key": "file-api-key",
            "default_material": "silver",
            "default_jewelry_type": "ring",
        }

        with patch.dict(os.environ, {}):
            config = load_config()

            assert config.get("meshy_api_key") == "file-api-key"
            assert config.get("default_material") == "silver"
            assert config.get("default_jewelry_type") == "ring"

    @patch("python_jewelry_design_gen.utils.config.Path.exists")
    @patch("python_jewelry_design_gen.utils.config.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_env_overrides_file(self, mock_file, mock_json_load, mock_exists):
        """Test that environment variables override file config."""
        mock_exists.return_value = True

        mock_json_load.return_value = {
            "meshy_api_key": "env-api-key",
            "default_material": "silver"
        }

        with patch.dict(os.environ, {
            "MESHY_API_KEY": "env-api-key",
        }):
            config = load_config()

            # Verify environment value is used over file value
            assert config.get("meshy_api_key") == "env-api-key"
            assert config.get("default_material") == "silver"
