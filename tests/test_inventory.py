import json
import pytest
import inventory as inv


@pytest.fixture(autouse=True)
def patch_inventory_file(tmp_path, monkeypatch):
    tmp_file = tmp_path / "inventory.json"
    monkeypatch.setattr(inv, "INVENTORY_FILE", tmp_file)
    return tmp_file


def test_load_inventory_missing_file():
    assert inv.load_inventory() == {}


def test_add_and_load_item():
    inv.add_item("milk", "1L")
    assert inv.load_inventory() == {"milk": "1L"}


def test_add_item_normalizes_to_lowercase():
    inv.add_item("Milk", "1L")
    assert "milk" in inv.load_inventory()


def test_remove_existing_item():
    inv.add_item("milk", "1L")
    removed = inv.remove_item("milk")
    assert removed is True
    assert inv.load_inventory() == {}


def test_remove_missing_item():
    removed = inv.remove_item("unicorn")
    assert removed is False


def test_add_multiple_items():
    inv.add_item("eggs", "6")
    inv.add_item("butter", "250g")
    loaded = inv.load_inventory()
    assert loaded["eggs"] == "6"
    assert loaded["butter"] == "250g"


def test_overwrite_existing_item():
    inv.add_item("eggs", "6")
    inv.add_item("eggs", "12")
    assert inv.load_inventory()["eggs"] == "12"


def test_save_and_reload(patch_inventory_file):
    inv.save_inventory({"pasta": "500g"})
    with patch_inventory_file.open() as f:
        data = json.load(f)
    assert data == {"pasta": "500g"}
