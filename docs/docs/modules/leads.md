
# Leads

Import the `ZohoCRMLead` module

```python
from zohocrm import ZohoCRMLead
```

Zoho converts the module's field such that:
* Spaces are replaced with underscores and 
* The capitalization of each word is preserved

For example, the field "First Name" becomes `.First_Name`

For this reason, you can get and set the fields of a `ZohoCRMLead` like this:

```python
lead = ZohoCRMLead(zoho_client)

lead.First_Name = "John"
lead.Last_Name = "Doe"
lead.Email = "email@example.com"
```

## Retrieve a lead

```python
lead_id = 1234023423424
lead = ZohoCRMLead.fetch(
    zoho_client,
    lead_id
)

print(lead.First_Name)
```

## Insert or Update a Lead

If the `lead.id` is set and is not `None`, the module will attempt to update the Lead with that ID. Otherwise it will attempt to insert a new Lead.

```python
owner = {
    'id': 1234234234,
    'name': "<Your user's name>",
    'email': "<Your user's email>"
}
lead = ZohoCRMLead(zoho_client)
lead.First_Name = 'John'
lead.Last_Name = 'Doe'
lead.Title = 'Job title'
lead.Company = 'Programming'
lead.Industry = 'San Francisco'
lead.State = 'CA'
lead.Country = 'United States'
lead.ZIP_Code = '94110'
lead.Website = 'http://example.com'
lead.Owner = owner

# if lead.id is set, .save() will update
# if lead.id is not set, .save() will insert
lead.save()

print(lead.id)
```

Alternately, you can use the `.insert()` or `.update()` methods.

## Delete a Lead

You can delete a lead with or without retrieving it first.

### Deleting a retrieved Lead

If the lead has already  been retrieved, the `.delete()` method will delete the record with the matching `.id`:

```python
lead_id = 1234023423424
lead = ZohoCRMLead.fetch(
    zoho_client,
    lead_id
)

# Delete
lead.delete()
```

### Deleting a Lead by ID

If the lead has not yet been retrieved, the `.delete_id()` requires the `id` of the record and can be called from the static class:

```python
lead_id = 1234023423424
lead = ZohoCRMLead.delete_id(
    zoho_client,
    lead_id
)
```
