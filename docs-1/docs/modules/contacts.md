
# Contacts

Import the `ZohoCRMContact` module

```python
from zohocrm import ZohoCRMContact
```

Zoho converts the module's field such that:
* Spaces are replaced with underscores and 
* The capitalization of each word is preserved

For example, the field "First Name" becomes `.First_Name`

For this reason, you can get and set the fields of a `ZohoCRMContact` like this:

```python
contact = ZohoCRMContact(zoho_client)

contact.First_Name = "John"
contact.Last_Name = "Doe"
contact.Email = "email@example.com"
```

## Retrieve a contact

```python
contact_id = 1234023423424
contact = ZohoCRMContact.fetch(
    zoho_client,
    contact_id
)

print(lead.First_Name)
```

## Insert or Update a Contact

If the `contact.id` is set and is not `None`, the module will attempt to update the `contact` Record with that ID. Otherwise it will attempt to insert a new Record.

```python
owner = {
    'id': 1234234234,
    'name': "<Your user's name>",
    'email': "<Your user's email>"
}
contact = ZohoCRMContact(zoho_client)
contact.First_Name = 'John'
contact.Last_Name = 'Doe'
contact.Title = 'Job title'
contact.Company = 'Programming'
contact.Industry = 'San Francisco'
contact.State = 'CA'
contact.Country = 'United States'
contact.ZIP_Code = '94110'
contact.Website = 'http://example.com'
contact.Owner = owner

# if contact.id is set, .save() will update
# if contact.id is not set, .save() will insert
contact.save()

print(contact.id)
```

Alternately, you can use the `.insert()` or `.update()` methods.

## Delete a Contact

You can delete a contact with or without retrieving it first.

### Deleting a retrieved Contact

If the contact has already  been retrieved, the `.delete()` method will delete the record with the matching `.id`:

```python
contact_id = 1234023423424
contact = ZohoCRMContact.fetch(
    zoho_client,
    contact_id
)

# Delete
contact.delete()
```

### Deleting a Contact by ID

If the contact has not yet been retrieved, the `.delete_id()` requires the `id` of the record and can be called from the static class:

```python
contact_id = 1234023423424
contact = ZohoCRMContact.delete_id(
    zoho_client,
    contact_id
)
```
