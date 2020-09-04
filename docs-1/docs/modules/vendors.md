
# Vendors

Import the `ZohoCRMVendor` module

```python
from zohocrm import ZohoCRMVendor
```

Zoho converts the module's field such that:
* Spaces are replaced with underscores and 
* The capitalization of each word is preserved

For example, the field "First Name" becomes `.Name`

For this reason, you can get and set the fields of a `ZohoCRMVendor` like this:

```python
vendor = ZohoCRMVendor(zoho_client)

vendor.Name = "ACME Inc."
vendor.Email = "email@example.com"
```

## Retrieve a vendor

```python
vendor_id = 1234023423424
vendor = ZohoCRMVendor.fetch(
    zoho_client,
    vendor_id
)

print(vendor.Name)
```

## Insert or Update a Vendor

If the `vendor.id` is set and is not `None`, the module will attempt to update the Vendor with that ID. Otherwise it will attempt to insert a new Vendor.

```python
owner = {
    'id': 1234234234,
    'name': "<Your user's name>",
    'email': "<Your user's email>"
}
vendor = ZohoCRMVendor(zoho_client)
vendor.Name = 'ACME Inc.'
vendor.State = 'CA'
vendor.Country = 'United States'
vendor.ZIP_Code = '94110'
vendor.Website = 'http://example.com'
vendor.Owner = owner

# if vendor.id is set, .save() will update
# if vendor.id is not set, .save() will insert
vendor.save()

print(vendor.id)
```

Alternately, you can use the `.insert()` or `.update()` methods.

## Delete a Vendor

You can delete a vendor with or without retrieving it first.

### Deleting a retrieved Vendor

If the vendor has already  been retrieved, the `.delete()` method will delete the record with the matching `.id`:

```python
vendor_id = 1234023423424
vendor = ZohoCRMVendor.fetch(
    zoho_client,
    vendor_id
)

# Delete
vendor.delete()
```

### Deleting a Vendor by ID

If the vendor has not yet been retrieved, the `.delete_id()` requires the `id` of the record and can be called from the static class:

```python
vendor_id = 1234023423424
vendor = ZohoCRMVendor.delete_id(
    zoho_client,
    vendor_id
)
```
