### Custom Modules

Zoho CRM provides the ability to create custom modules. This API works within that framework to allow you to create, retrieve, update, and delete custom module records.

Let's say you have a custom module called `Friends` which has the following structure:
* Friend Owner
* First Name
* Last Name
* Email
* Favorite Color

You can create an object that talks to this module by creating a class that extends `ZohoCRMRecord` with a `_module_name` property equal to the [module's API Name](https://www.zoho.com/crm/developer/docs/api/modules-api.html#:~:text=Zoho%20CRM%20generates%20API%20name,%2C%20fields%2C%20and%20related%20lists.).

```python
from zohocrm import ZohoCRMRecord

class ZohoCRMFriend(ZohoCRMRecord):
    """Zoho CRM Custom Module "Friends"."""

    _module_name = 'Friends'
```

Zoho converts the module's field such that:

* Spaces are replaced with underscores and 
* Preserves the capitalization of each word

Therefore, you can add a new `Friend` record by doing the following:

```python
# ZohoCRMFriend has already been defined
# a valid oauth token has been retrieved

friend = ZohoCRMFriend(zoho_client)

friend.First_Name = "John"
friend.Last_Name = "Doe"
friend.Email = "email@example.com"
friend.Favorite_Color = "blue"
friend.Owner = {
    'id': 1234234234,
    'name': "<Your user's name>",
    'email': "<Your user's email>"
}

friend.save()

print(friend.id)
```

Create, Retrieve, Update, and Delete functions are performed just like any other module.

## Create


```python
friend = ZohoCRMFriend(zoho_client)

friend.First_Name = "John"
friend.Last_Name = "Doe"
friend.Email = "email@example.com"
friend.Favorite_Color = "blue"
```

## Insert or Update

If the `.id` is set and is not `None`, the module will attempt to update the Record with that ID. Otherwise it will attempt to insert a new Record.

```python
owner = {
    'id': 1234234234,
    'name': "<Your user's name>",
    'email': "<Your user's email>"
}
friend = ZohoCRMFriend(zoho_client)
friend.First_Name = 'John'
friend.Last_Name = 'Doe'
friend.Email = 'email@example.com'
friend.Favorite_Color = "blue"
friend.Owner = owner

# if friend.id is set, .save() will update
# if friend.id is not set, .save() will insert
friend.save()

print(friend.id)
```

Alternately, you can use the `.insert()` or `.update()` methods.

## Delete

You can delete a Record with or without retrieving it first.

### Deleting a retrieved Record

If the Record has already been retrieved, the `.delete()` method will delete the record with the matching `.id`:

```python
friend_id = 1234023423424
friend = ZohoCRMFriend.fetch(
    zoho_client,
    friend_id
)

# Delete
friend.delete()
```

### Deleting a Record by ID

If the Record has not yet been retrieved, the `.delete_id()` requires the `id` of the record and can be called from the static class:

```python
friend_id = 1234023423424
friend = ZohoCRMFriend.delete_id(
    zoho_client,
    friend_id
)
```

