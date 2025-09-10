import pytest

# from unittest.mock import patch, MagicMock

from glmpy.nml import nml

# import NMLParam, NMLBlock, NML, NMLRegistry


# Create mock NMLBlock and NML classes for testing
class MockBlock1(nml.NMLBlock):
    nml_name = "mock_nml"
    block_name = "mock_block1"

    def validate(self):
        pass


class MockBlock2(nml.NMLBlock):
    nml_name = "mock_nml"
    block_name = "mock_block2"

    def validate(self):
        pass


class DifferentNMLBlock(nml.NMLBlock):
    nml_name = "different_nml"
    block_name = "different_block"

    def validate(self):
        pass


class MockNML(nml.NML):
    nml_name = "mock_nml"

    def validate(self):
        pass


class DifferentNML(nml.NML):
    nml_name = "different_nml"

    def validate(self):
        pass


class TestNMLRegistry:
    def test_initialization(self):
        """Test basic initialization of NMLRegistry."""
        registry = nml.NMLRegistry("test_registry")
        assert registry._name == "test_registry"
        assert registry.cls_map == {}

    def test_register_block(self):
        """Test registering NMLBlock classes."""
        registry = nml.NMLRegistry("test_registry")

        # Register a block
        decorator = registry.register_block()
        result = decorator(MockBlock1)

        # Check that the decorator returns the class
        assert result is MockBlock1

        # Check that the class was properly registered
        assert "mock_nml" in registry.cls_map
        assert "blocks" in registry.cls_map["mock_nml"]
        assert "mock_block1" in registry.cls_map["mock_nml"]["blocks"]
        assert (
            registry.cls_map["mock_nml"]["blocks"]["mock_block1"] is MockBlock1
        )

        # Register another block in the same NML
        decorator = registry.register_block()
        decorator(MockBlock2)

        assert "mock_block2" in registry.cls_map["mock_nml"]["blocks"]
        assert (
            registry.cls_map["mock_nml"]["blocks"]["mock_block2"] is MockBlock2
        )

        # Register a block in a different NML
        decorator = registry.register_block()
        decorator(DifferentNMLBlock)

        assert "different_nml" in registry.cls_map
        assert "different_block" in registry.cls_map["different_nml"]["blocks"]
        assert (
            registry.cls_map["different_nml"]["blocks"]["different_block"]
            is DifferentNMLBlock
        )

    def test_register_nml(self):
        """Test registering NML classes."""
        registry = nml.NMLRegistry("test_registry")

        # Register an NML
        decorator = registry.register_nml()
        result = decorator(MockNML)

        # Check that the decorator returns the class
        assert result is MockNML

        # Check that the class was properly registered
        assert "mock_nml" in registry.cls_map
        assert "nml" in registry.cls_map["mock_nml"]
        assert registry.cls_map["mock_nml"]["nml"] is MockNML

        # Register an NML with a different name
        decorator = registry.register_nml()
        decorator(DifferentNML)

        assert "different_nml" in registry.cls_map
        assert registry.cls_map["different_nml"]["nml"] is DifferentNML

    def test_get_block_cls(self):
        """Test retrieving registered block classes."""
        registry = nml.NMLRegistry("test_registry")

        # Register blocks first
        decorator = registry.register_block()
        decorator(MockBlock1)
        decorator(MockBlock2)

        # Retrieve the blocks
        block1_cls = registry.get_block_cls("mock_nml", "mock_block1")
        block2_cls = registry.get_block_cls("mock_nml", "mock_block2")

        assert block1_cls is MockBlock1
        assert block2_cls is MockBlock2

        # Test with non-existent block
        with pytest.raises(KeyError):
            registry.get_block_cls("mock_nml", "non_existent_block")

        # Test with non-existent NML
        with pytest.raises(KeyError):
            registry.get_block_cls("non_existent_nml", "mock_block1")

    def test_get_nml_cls(self):
        """Test retrieving registered NML classes."""
        registry = nml.NMLRegistry("test_registry")

        # Register NMLs first
        decorator = registry.register_nml()
        decorator(MockNML)
        decorator(DifferentNML)

        # Retrieve the NMLs
        nml1_cls = registry.get_nml_cls("mock_nml")
        nml2_cls = registry.get_nml_cls("different_nml")

        assert nml1_cls is MockNML
        assert nml2_cls is DifferentNML

        # Test with non-existent NML
        with pytest.raises(KeyError):
            registry.get_nml_cls("non_existent_nml")

        # Test with NML that exists but has no registered class
        registry.cls_map["empty_nml"] = {"blocks": {}, "nml": None}
        with pytest.raises(KeyError):
            registry.get_nml_cls("empty_nml")

    def test_duplicate_block_registration(self):
        """Test that registering duplicate blocks raises an error."""
        registry = nml.NMLRegistry("test_registry")

        # Register a block first
        decorator = registry.register_block()
        decorator(MockBlock1)

        # Try to register another block with the same name
        decorator = registry.register_block()
        with pytest.raises(AssertionError):
            decorator(MockBlock1)  # Same class, same names

        # Create a new class with the same block_name
        class DuplicateBlock(nml.NMLBlock):
            nml_name = "mock_nml"
            block_name = "mock_block1"  # Same as MockBlock1

            def validate(self):
                pass

        # Try to register it
        decorator = registry.register_block()
        with pytest.raises(AssertionError):
            decorator(DuplicateBlock)

    def test_duplicate_nml_registration(self):
        """Test that registering duplicate NMLs raises an error."""
        registry = nml.NMLRegistry("test_registry")

        # Register an NML first
        decorator = registry.register_nml()
        decorator(MockNML)

        # Try to register another NML with the same name
        decorator = registry.register_nml()
        with pytest.raises(AssertionError):
            decorator(MockNML)  # Same class, same name

        # Create a new class with the same nml_name
        class DuplicateNML(nml.NML):
            nml_name = "mock_nml"  # Same as MockNML

            def validate(self):
                pass

        # Try to register it
        decorator = registry.register_nml()
        with pytest.raises(AssertionError):
            decorator(DuplicateNML)

    def test_direct_registration(self):
        """
        Test direct registration methods (`_do_register_block` and 
        `_do_register_nml`).
        """
        registry = nml.NMLRegistry("test_registry")

        # Directly register a block
        registry._do_register_block("direct_nml", "direct_block", MockBlock1)
        assert "direct_nml" in registry.cls_map
        assert "direct_block" in registry.cls_map["direct_nml"]["blocks"]
        assert (
            registry.cls_map["direct_nml"]["blocks"]["direct_block"]
            is MockBlock1
        )

        # Directly register an NML
        registry._do_register_nml("direct_nml", MockNML)
        assert registry.cls_map["direct_nml"]["nml"] is MockNML

        # Try to register duplicate block
        with pytest.raises(AssertionError):
            registry._do_register_block(
                "direct_nml", "direct_block", MockBlock2
            )

        # Try to register duplicate NML
        with pytest.raises(AssertionError):
            registry._do_register_nml("direct_nml", DifferentNML)

    def test_realistic_usage(self):
        """
        Test using the registry in a realistic scenario with decorators.
        """
        registry = nml.NMLRegistry("test_registry")

        # Define new classes using the registry decorators directly
        @registry.register_block()
        class TestBlock1(nml.NMLBlock):
            nml_name = "test_nml"
            block_name = "test_block1"

            def validate(self):
                pass

        @registry.register_block()
        class TestBlock2(nml.NMLBlock):
            nml_name = "test_nml"
            block_name = "test_block2"

            def validate(self):
                pass

        @registry.register_nml()
        class TestNML(nml.NML):
            nml_name = "test_nml"

            def validate(self):
                pass

        # Verify the classes were registered properly
        assert registry.get_block_cls("test_nml", "test_block1") is TestBlock1
        assert registry.get_block_cls("test_nml", "test_block2") is TestBlock2
        assert registry.get_nml_cls("test_nml") is TestNML

        # Create instances and verify they work as expected
        block1 = TestBlock1()
        block2 = TestBlock2()
        test_nml = TestNML()

        assert block1.nml_name == "test_nml"
        assert block1.block_name == "test_block1"
        assert block2.nml_name == "test_nml"
        assert block2.block_name == "test_block2"
        assert test_nml.nml_name == "test_nml"

    def test_global_registry(self):
        """
        Test that the global NML_REGISTER is a valid NMLRegistry
        instance.
        """
        assert isinstance(nml.NML_REGISTER, nml.NMLRegistry)
        assert nml.NML_REGISTER._name == "main"
