
# Module Support

So far this package supports the following Record API actions:

| Module          | Create | Retrieve | Update | Delete |
|-----------------|--------|----------|--------|--------|
| Contacts        | x      | x        | x      | x      |
| Leads           | x      | x        | x      | x      |
| Vendors         | x      | x        | x      | x      |
| Accounts        | x      | x        | x      | x      |
| Deals           | x      | x        | x      | x      |
| Vendors         | x      | x        | x      | x      |
| Campaign        | x      | x        | x      | x      |
| Tasks           | x      | x        | x      | x      |
| Cases           | x      | x        | x      | x      |
| Calls           | x      | x        | x      | x      |
| Solutions       | x      | x        | x      | x      |
| Products        | x      | x        | x      | x      |
| Vendors         | x      | x        | x      | x      |
| Price Books     | x      | x        | x      | x      |
| Quotes          | x      | x        | x      | x      |
| Sales Orders    | x      | x        | x      | x      |
| Purchase Orders | x      | x        | x      | x      |
| Invoices        | x      | x        | x      | x      |
| Custom          | x      | x        | x      | x      |
| Notes           | x      | x        | x      | x      |
| Activities      | x      | x        | x      | x      |


All modules are extended from the same common interface. The difference is in what fields are returned from Zoho. So the same functions are available for each module.

Each module provides the same methods:

* Static `.fetch(zoho_client: ZohoCRMRestClient, record_id: int)` returns an instance of the module
* `.save()` inserts a Record if the `.id` property is set to an `int` and updates utherwise.
* `.insert()` inserts a Record
* `.update()` updates an existing record. An `.id` must be set
* `delete()` deletes a Record. An `.id` must be set
* Static `.delete_id(zoho_client: ZohoCRMRestClient, record_id: int)` deletes a Record matching the `record_id`.

Zoho returns different fields depending on the module. Zoho converts the module's field such that:

* Spaces are replaced with underscores and 
* Preserves the capitalization of each word

For example the Contact "First Name" field becomes `ZohoCRMContact.First_Name` property in the module.

These fields are populated when data is retrieved from the Zoho API. They are not defined in the Python code.

Each Zoho Record has a unique ID, which is stored as an `.id` property when retrieved in the module. This `.id` is used to `.update()` or `.delete()`
