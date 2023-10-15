# Django-sales-peach

This is my pet project to create a small working website that just uses OpenAPI to provide suggestions to marketing person on what to send when first reaching out other compananies trying to sell their product.

Following technology stack is used:
* Django for backend and frontend with HTML and Django templates
* MySQL database 
* Support of [Sprite](https://stripe.com/) as a payment system with fully integrated subscriptions
* [Uvicorn](https://www.uvicorn.org/) as an ASGI server for python
* Custom docker files for MySQL and the app itself
* Kubernetes implemetation (aimed to be used Google cloud) that contains NGinx ingress, app & database deployments, configurations and secrets (not checked in obviously)

Note: the application is using submodule using actual OpenAPI implementation. The repository is private, but here is what you would need to implement on the api side:

```
www.example.host/v1/suggestions/get
```
that receives json and returns string with suggestion.

