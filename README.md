# Author: Emiliano Mazzurque 

* email: emazzurque@gmail.com

# how to run 

create venv (optional)

#### Requirements Setup
```
pip install - r requirements.txt
```

# or run with docker 
```
docker-compose up --build
```


### Running migrations
```
python manage.py makemigrations
```

```
python manage.py migrate
```

### Create superuser
```
python manage.py createsuperuser
```

### TEST 
```
pytest test/
```

### Considerations

The service run in localhost:8000/graphql/ 

GraphQl provide docs of the service in Documentation Explorer

It is proposed for future reports of non-staff visitors. generate a task with Celery for the massive creation (bulk_create) of the records of the table Visitors, it will be done with the required regularity according to the number of visits.





# Documentation of the system to manage products
## General description
This service provides functionality to manage the following Django models:

### MyUser: A custom user model that represents a registered user in the system.
### Brand: A model that represents a brand.
### Product – A model that represents a product with SKU, name, price, and brand.
### Visitor: A model that represents a visitor to the website.

The service allows you to perform CRUD (create, read, update, and delete) operations on these models, as well as offers additional functionality such as searching and filtering data.

### Models

## MyUser

### Attributes:

* password (str): The user's password, hashed for security.
* is_active (bool): Indicates whether the user account is active.
* username (str): The unique username of the user.
* email (str): The user's unique email address.
* first_name (str): The first name of the user.
* last_name (str): The last name of the user.
* is_team (bool): Indicates if the user belongs to a team.
* is_staff (bool): Indicates whether the user has access to the administration site.
* has_perm (bool): Indicates if the user has any permissions.

## Brand
### Attributes:

* name (str): The brand name.
* description (str): An optional description of the brand.

#Methods:

* str() -> str: Returns the brand name as a string.


## Product
### Attributes:

* sku (UUIDField): The SKU (stock keeping unit) of the product.
* name (str): The name of the product.
* price (Decimal): The price of the product.
* brand (ForeignKey): A foreign key to the product brand.

# methods:

* str() -> str: Returns the name of the product as a string.


## Visitor

### Attributes:

* accept_language (str): The "Accept-Language" HTTP header of the visitor's browser.
* user_agent (str): The "User-Agent" HTTP header of the visitor's browser.
* ip_address (str): The IP address of the visitor.
* created_at (date): The date the visitor record was created.
# methods:

* str() -> str: Returns the visitor record creation date as a string.


### Functionalities of the service

The service provides the following functionalities to manage the models described above:

* Create, read, update and delete model records.
* Search and filter records by different attributes.
* Data validation before creating or updating records.
* Restriction of access to certain functionalities only to users with certain permissions.
* Record of actions performed in the system.


### CreateUserMutation:


### Input fields:
* username (string, required)
* last_name (string, required)
* email (string, required)
* password (string, required)
### Output fields:

* success (boolean)
* user (UserNode)
* message (string)

# Description: 
This endpoint allows clients to create new user records. Clients can pass the required input fields as arguments. If the mutation succeeds, the response will include the newly created user record along with a success field set to True. If the mutation fails, the success field will be False, and the message field will provide information about the error.


## DeleteUserMutation:

### Input fields:

* user_id (ID, required)
### Output fields:

* success (boolean)
* user (UserNode)
* message (string)

## Description: 

This endpoint allows authenticated clients to delete a user record. Clients can pass the user_id field as an argument. If the mutation succeeds, the response will include the deleted user record along with a success field set to True. If the mutation fails, the success field will be False, and the message field will provide information about the error.


## UpdateUserMutation:

### Input fields:
* user_id (ID, required)
* username (string, optional)
* last_name (string, optional)
* email (string, optional)
* password (string, optional)

### Output fields:

* success (boolean)
* user (UserNode)
* message (string)
# Description: 

This endpoint allows authenticated clients to update a user record. Clients can pass the user_id field as an argument, along with any optional fields to update. If the mutation succeeds, the response will include the updated user record along with a success field set to True. If the mutation fails, the success field will be False, and the message field will provide information about the error.


### PRoduct 

## CreateProductMutation:

# Description: 
GraphQL mutation that allows clients to create a new product with the specified name, price, and brand_id.


### Input arguments:
* name: String. Required.
* price: Decimal. Required.
* brand_id: ID. Required.

### Output fields:

* success: Boolean. Indicates whether the mutation was successful or not.
* product: ProductNode. Represents the newly created product.
* message: String. Provides additional information about the success or failure of the mutation.

## DeleteProductMutation:
# Description: 
GraphQL mutation that allows clients to delete a product by its ID.

### Input arguments:

 * product_id: ID. Required.
 
 ### Output fields:

 * success: Boolean. Indicates whether the mutation was successful or not.
 * product: ProductNode. Represents the deleted product.
 * message: String. Provides additional information about the success or failure of the mutation.


## UpdateProductMutation:

# Description: 

GraphQL mutation that allows clients to update a product by its ID with the specified parameters.
### Input arguments:
 * product_id: ID. Required.
 * sku: String. Optional.
 * name: String. Optional.
 * price: Decimal. Optional.
 * brand: String. Optional.

### Output fields:

* success: Boolean. Indicates whether the mutation was successful or not.
* product: ProductNode. Represents the updated product.
* message: String. Provides additional information about the success or failure of the mutation.
ProductQuery:
Description: GraphQL query that allows clients to retrieve product information.
### Output fields:
product: ProductNodeConnection. Represents a connection to a list of products.
### Input arguments:

* id: Int. Optional. If provided, retrieves the product with the specified ID.

## Additional information: 

Filters out products that have been marked as deleted. If the user is not authenticated, the query logs the request date.


### METHOD VISIT
## Method: get_data(info)

# Description
This method is used to obtain information about a visit, including the accept language, user agent, IP address, created at, and visit ID. It returns a string representation of a dictionary containing this information.

# Parameters
* info: An object containing information about the request.
# Returns
A string representation of a dictionary containing information about the visit.

# example to save: 
'{"accept_language": "en-US,en;q=0.9", "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36", "ip_address": "127.0.0.1", "created_at": "2023-04-11 10:00:00.000000", "visit_id": "123e4567-e89b-12d3-a456-426655440000"}'


## Method: save_date(info)

# Description

This method saves the visit information obtained from the get_data method into a Redis database. If an error occurs, the method prints the error message to the console.

# Parameters

* info: An object containing information about the request.

# Returns

* None

## Method: send_email(subject, body, recipient)

# Description

This method sends an email using the Amazon SES (Simple Email Service) API. It takes in the subject, body, and recipient email address as parameters.

# Parameters

* subject: A string representing the subject of the email.
* body: A string representing the body of the email.
* recipient: A string representing the email address of the recipient.

# Returns

* A dictionary containing the response from Amazon SES.

