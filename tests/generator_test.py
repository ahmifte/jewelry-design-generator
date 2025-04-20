from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from python_jewelry_design_gen.generators.meshy_generator import JewelryGenerationError
from python_jewelry_design_gen.generators.meshy_generator import MeshyJewelryGenerator
from python_jewelry_design_gen.models.jewelry_design import ChainStyle
from python_jewelry_design_gen.models.jewelry_design import JewelryDesign
from python_jewelry_design_gen.models.jewelry_design import JewelryType
from python_jewelry_design_gen.models.jewelry_design import Material

GENERATOR_MODULE = 'python_jewelry_design_gen.generators.meshy_generator'


class TestMeshyJewelryGenerator:

    @pytest.fixture
    def batch_size(self):
        return 3

    @pytest.fixture
    def mock_api(self):
        """Create a mock Meshy API client."""
        mock = MagicMock()
        mock.create_text_to_3d_preview.return_value = 'preview-task-123'
        mock.create_text_to_3d_refine.return_value = 'refine-task-456'
        mock.wait_for_task_completion.return_value = {
            'model_urls': {
                'glb': 'https://example.com/model.glb',
                'fbx': 'https://example.com/model.fbx',
            },
            'texture_urls': [
                {
                    'base_color': 'https://example.com/texture_0.png',
                    'normal': 'https://example.com/texture_0_normal.png',
                },
            ],
            'thumbnail_url': 'https://example.com/thumbnail.png',
        }

        mock.download_3d_model.return_value = {
            'glb': '/path/to/model.glb',
            'fbx': '/path/to/model.fbx',
            'thumbnail': '/path/to/thumbnail.png',
        }
        return mock

    @pytest.fixture
    def generator(self, mock_api, batch_size):
        """Create a generator with mocked API."""
        config_path = f'{GENERATOR_MODULE}.load_config'
        with patch(config_path) as mock_config:
            mock_config.return_value = {
                'default_material': 'gold',
                'default_jewelry_type': 'chain',
                'default_chain_style': 'cuban',
                'models_dir': 'output/models',
                'metadata_dir': 'output/metadata',
                'default_batch_size': batch_size,
            }
            return MeshyJewelryGenerator(api_client=mock_api)

    @patch(f'{GENERATOR_MODULE}.save_design_metadata')
    @patch(f'{GENERATOR_MODULE}.Path.mkdir')
    def test_generate_design(
        self, mock_mkdir, mock_save_metadata, generator, mock_api,
    ):
        """Test generating a single design."""
        design = generator.generate_design(
            material=Material.GOLD,
            jewelry_type=JewelryType.RING,
            formats=['glb', 'fbx'],
        )

        assert design is not None
        assert design.material == Material.GOLD
        assert design.jewelry_type == JewelryType.RING
        assert 'glb' in design.model_urls
        assert 'fbx' in design.model_urls
        assert design.thumbnail_url is not None

        mock_api.create_text_to_3d_preview.assert_called_once()
        mock_api.create_text_to_3d_refine.assert_called_once()
        mock_api.wait_for_task_completion.assert_called()
        mock_api.download_3d_model.assert_called_once()

        mock_save_metadata.assert_called_once_with(
            design.id,
            design.to_dict(),
            generator.config.get('metadata_dir', 'output/metadata'),
        )

        mock_mkdir.assert_called()

    @patch(f'{GENERATOR_MODULE}.save_design_metadata')
    @patch(f'{GENERATOR_MODULE}.Path.mkdir')
    @patch('concurrent.futures.ThreadPoolExecutor')
    def test_generate_batch(
        self, mock_executor, mock_mkdir, mock_save_metadata,
        generator, batch_size,
    ):
        """Test generating a batch of designs."""

        mock_future = MagicMock()
        mock_future.result.return_value = JewelryDesign(
            material=Material.SILVER,
            jewelry_type=JewelryType.CHAIN,
            chain_style=ChainStyle.CUBAN,
        )

        mock_executor_instance = MagicMock()
        mock_executor.return_value.__enter__.return_value = (
            mock_executor_instance
        )

        mock_executor_instance.submit.return_value = mock_future

        mock_futures = [mock_future] * batch_size

        as_completed_path = 'concurrent.futures.as_completed'
        with patch(as_completed_path, return_value=mock_futures):
            designs = generator.generate_batch(
                batch_size=batch_size,
                material=Material.SILVER,
                jewelry_type=JewelryType.CHAIN,
                max_workers=2,
            )

            # Verify the designs
            assert len(designs) == batch_size
            for design in designs:
                assert design.material == Material.SILVER
                assert design.jewelry_type == JewelryType.CHAIN

            mock_executor.assert_called_once_with(max_workers=2)

    @patch('python_jewelry_design_gen.generators.meshy_api.MeshyAPI')
    def test_api_error_handling(self, mock_api_class):

        # Mock the API to raise an error
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.create_text_to_3d_preview.side_effect = Exception('API Error')

        generator = MeshyJewelryGenerator(api_client=mock_api)

        # Verify error is proprly propagated
        with pytest.raises(JewelryGenerationError):
            generator.generate_design(
                material=Material.GOLD,
                jewelry_type=JewelryType.RING,
            )
